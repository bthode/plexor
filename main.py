import datetime as datetime
import os
import xml.etree.ElementTree as ET

import fetcher
from model import Video, VideoStatus, Subscription, Policy, Retention
from subscription_manager import SubscriptionManager

# from urllib.request import urlopen

CHANNEL_URL = './/{http://www.w3.org/2005/Atom}link[@rel="alternate"]'

CHANNEL_NAME = '{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name'

ATOM_LINK_REL_ALTERNATE_ = "{http://www.w3.org/2005/Atom}link[@rel='alternate']"

ORG_ATOM_TITLE = "{http://www.w3.org/2005/Atom}title"

# cat output.xml| xq '.feed.entry[].title'

if __name__ == '__main__':
    manager = SubscriptionManager()
    manager.recreate_database()

    manager.add_setting("download_location", "~/tmp", "String")
    download_path = manager.get_download_location()
    # OBTAIN SUBSCRIPTION DATA

    # url = "https://www.youtube.com/feeds/videos.xml?channel_id=UC-UZjHl2kZ-6XKBLgbFgGAQ"
    #
    # response = urlopen(url)
    # xml_content = response.read()

    file_path = os.path.expanduser("~/tmp/output.xml")
    with open(file_path, "rb") as f:
        xml_content = f.read()

    root = ET.fromstring(xml_content)

    subscription = Subscription(
        title="Convert Go Blue",
        url="https://www.youtube.com/channel/UC-UZjHl2kZ-6XKBLgbFgGAQ",
        policy=Policy(
            type=Retention.DATE_BASED,
            days_to_retain=7
        )

        # title=root.find(CHANNEL_NAME).text,
        # rss_feed_url=root.find(CHANNEL_URL).get('href'),
        # last_queried=datetime.datetime.utcnow()
    )

    manager.add_subscription(subscription)
    manager.update_subscription_rss_feed()

    entries = root.findall(".//{http://www.w3.org/2005/Atom}entry")

    # Flow...
    # Read the subscription table, update rss path values as needed
    # For each subscription, fetch the video entries.
    # Add only the missing videos into our table
    # Then, for each subscription,
    # For each video that has not been downloaded, falls within the time window, and doesn't exceed the retry count,
    # Download
    # For each successful video downloaded,
    # Add the video to Plex

for entry in entries:
    title = entry.findtext("{http://www.w3.org/2005/Atom}title"),
    link = entry.find("{http://www.w3.org/2005/Atom}link[@rel='alternate']").get('href'),
    entry_id = entry.find("{http://www.w3.org/2005/Atom}id").text.split(":")[-1],
    video_id = entry.find("{http://www.youtube.com/xml/schemas/2015}videoId").text,
    channel_id = entry.find("{http://www.youtube.com/xml/schemas/2015}channelId").text,
    author = entry.find("{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name").text,
    published = entry.find("{http://www.w3.org/2005/Atom}published").text,
    updated = entry.find("{http://www.w3.org/2005/Atom}updated").text,
    thumbnail = entry.find(".//{http://search.yahoo.com/mrss/}thumbnail").attrib.get("url"),
    description = entry.find(".//{http://search.yahoo.com/mrss/}description").text.strip()

    # TODO: We need to set videos with some sort of status that they are too old to begin with
    video = Video(
        # Create a new Video
        url=entry.find("{http://www.w3.org/2005/Atom}link[@rel='alternate']").get('href'),
        status=VideoStatus.PENDING,
        download_attempts=0,
        subscription=subscription,
        title=entry.findtext("{http://www.w3.org/2005/Atom}title"),
        created_at=datetime.datetime.strptime(entry.find("{http://www.w3.org/2005/Atom}published").text,
                                              "%Y-%m-%dT%H:%M:%S%z")
    )
    manager.add_video(video)

for subscription in manager.get_all_subscriptions():
    for video in manager.all_pending_videos_per_policy(subscription, subscription.policy):
        print(f"--> Video: ID={video.id} Title={video.title} Status={video.status}")
        manager.set_video_status(video, VideoStatus.IN_PROGRESS)
        success, filepath = fetcher.fetch_video_url(download_path, video)
        manager.set_video_saved_path(video, filepath)

        if success:
            # update the video status to COMPLETE
            video.status = VideoStatus.COMPLETE
            manager.set_video_status(video, VideoStatus.COMPLETE)
        else:
            manager.set_video_status(video, VideoStatus.FAILED)

all_subs = manager.get_all_subscriptions()
manager.set_video_datetime_to_past()
manager.get_videos_to_be_deleted(all_subs)

# Deleting file None

# We need to only delete when we get the value back...
# No, just don't try deletintg videos that we couldn't download successfully...
