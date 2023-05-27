from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import obtain_feed_url
from model import Base, VideoStatus
from model import Video, Subscription


class SubscriptionManager:
    def __init__(self) -> None:
        """Initialize the SubscriptionManager with a database engine."""
        self.subscriptions = set()

        # Create an engine to connect to the database
        self.engine = create_engine('sqlite:///database.db')

        # Create a session
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.Base = Base

    def add_subscription(self, subscription: Subscription) -> None:
        self.session.add(subscription)
        self.session.commit()
        print(f"Adding Subscription for {subscription.title}")
        pass

    def subscription_with_missing_rss_feed_url(self) -> List[Subscription]:
        return self.session.query(Subscription).filter(Subscription.rss_feed_url.is_(None)).all()
        pass

    def update_subscription_rss_feed(self):
        subscriptions = self.subscription_with_missing_rss_feed_url()
        for subscription in subscriptions:
            if not subscription:
                return None
            subscription.rss_feed_url = obtain_feed_url.fetch_rssfeed(subscription)
            self.session.commit()
            print(f"Updating subscription RSS URL for channel {subscription.title}")

    def all_pending_videos(self) -> List[Video]:
        return self.session.query(Video).filter_by(status=VideoStatus.PENDING).all()
        pass

    def add_video(self, video: Video):
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
        print(f"Setting video {video.title} to {status}")

    def parse_xml(self):
        pass
