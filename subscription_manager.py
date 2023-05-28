from datetime import datetime, timedelta
from typing import List

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

import obtain_channel_metadata
from model import Base, VideoStatus, Setting, Policy, Retention
from model import Video, Subscription


class SubscriptionManager:
    def delete_by_date(self, videos: List[Video], policy: Policy):
        for video in videos:
            if video.created_at < datetime.now() - timedelta(days=policy.days_to_retain):
                self.set_video_status(video, VideoStatus.DELETED)
                video.delete_video_file()

    retention = {
        Retention.DATE_BASED: delete_by_date,
    }

    def __init__(self, database_file) -> None:
        """Initialize the SubscriptionManager with a database engine."""
        self.subscriptions = set()

        # Create an engine to connect to the database
        self.engine = create_engine('sqlite:///' + database_file)

        # Create a session
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.Base = Base

    def add_subscription(self, subscription: Subscription) -> None:
        self.session.add(subscription)
        self.session.commit()
        print(f"Adding Subscription for {subscription.url}")
        pass

    def subscription_with_missing_metadata(self) -> List[Subscription]:
        return self.session.query(Subscription).filter(
            or_(Subscription.rss_feed_url == '', Subscription.rss_feed_url.is_(None), Subscription.title == '',
                Subscription.title.is_(None))).all()
        pass

    def update_subscription_metadata(self):
        subscriptions = self.subscription_with_missing_metadata()
        for subscription in subscriptions:
            if not subscription:
                return None
            subscription.rss_feed_url = obtain_channel_metadata.fetch_rss_feed(subscription)
            subscription.title = obtain_channel_metadata.fetch_channel_title(subscription)
            self.session.commit()
            print(f"Updating subscription RSS URL for channel {subscription.title}")

    # We should get failed videos, but respect the failed download count limit
    def all_pending_videos_per_policy(self, subscription: Subscription) -> List[Video]:
        policy = self.get_policy_for_subscription(subscription)
        limit_date = datetime.now() - timedelta(days=policy.days_to_retain)
        return self.session.query(Video) \
            .filter(subscription.id == subscription.id) \
            .filter(Video.created_at < limit_date) \
            .filter(Video.status == VideoStatus.PENDING) \
            .all()

    def exclude_videos_per_policy(self, subscription: Subscription):
        policy = self.get_policy_for_subscription(subscription)
        limit_date = datetime.now() - timedelta(days=policy.days_to_retain)
        to_exclude = self.session.query(Video) \
            .filter(subscription.id == subscription.id) \
            .filter(Video.created_at > limit_date) \
            .all()
        for video in to_exclude:
            self.set_video_status(video, VideoStatus.EXCLUDED)

    def add_videos(self, video_list: List[Video]) -> None:
        for vidio in video_list:
            self.add_video(vidio)

    def add_video(self, video: Video):
        video_exists = self.session.query(Video).filter_by(url=video.url).count() > 0

        if not video_exists:
            self.session.add(video)
            self.session.commit()
            print(f"Adding Video: {video.title}")

    def recreate_database(self):
        Base.metadata.reflect(self.engine)
        Base.metadata.drop_all(self.engine, checkfirst=True)
        Base.metadata.create_all(self.engine)

    def set_video_status(self, video: Video, status: VideoStatus) -> None:
        video.status = status
        self.session.commit()
        print(f"Setting video {video.title} to {status.name}")

    def parse_xml(self):
        pass

    def add_setting(self, key: str, value, datatype):
        setting = Setting(key=key, value=value, value_type=datatype)
        self.session.add(setting)
        self.session.commit()

    def get_download_location(self):
        setting = self.session.query(Setting).filter_by(key="download_location").first()
        if setting is not None:
            return setting.value
        else:
            return None

    def get_all_subscriptions(self):
        return self.session.query(Subscription).all()

    # session.query(Subscription).filter_by(id=<subscription_id>).first()
    def get_policy_for_subscription(self, subscription: Subscription) -> Policy:
        return self.session.query(Policy).filter_by(id=subscription.id).first()

    def get_downloaded_videos_for_subscription(self, subscription: Subscription) -> List[Video]:
        return self.session.query(Video) \
            .filter_by(subscription_id=subscription.id) \
            .filter_by(status=VideoStatus.COMPLETE) \
            .all()

    def get_videos_to_be_deleted(self, subscription: List[Subscription]):
        for s in subscription:
            policy = self.get_policy_for_subscription(s)
            videos = self.get_downloaded_videos_for_subscription(s)
            retention_strategy = self.retention.get(Retention.DATE_BASED)
            if retention_strategy:
                retention_strategy(
                    self=self,
                    videos=videos,
                    policy=policy
                )

    def set_video_datetime_to_past(self):
        video = self.session.query(Video).first()
        video.created_at = datetime.now() - timedelta(days=30)  # Magic Number
        self.session.commit()

    def set_video_saved_path(self, video: Video, path: str) -> None:
        video.saved_path = path
        self.session.commit()
