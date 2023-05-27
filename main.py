import os
import xml.etree.ElementTree as ET
from datetime import datetime

import datetime as datetime

import fetcher
# from urllib.request import urlopen

from model import Video, VideoStatus, Subscription, Policy, Retention
from subscription_manager import SubscriptionManager

CHANNEL_URL = './/{http://www.w3.org/2005/Atom}link[@rel="alternate"]'

CHANNEL_NAME = '{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name'

ATOM_LINK_REL_ALTERNATE_ = "{http://www.w3.org/2005/Atom}link[@rel='alternate']"

ORG_ATOM_TITLE = "{http://www.w3.org/2005/Atom}title"

# cat output.xml| xq '.feed.entry[].title'

if __name__ == '__main__':
    manager = SubscriptionManager()
    manager.recreate_database()

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

for video in manager.all_pending_videos():
    manager.set_video_status(video, VideoStatus.IN_PROGRESS)
    success = fetcher.fetch_video_url(video)
    if success:
        # update the video status to COMPLETE
        video.status = VideoStatus.COMPLETE
        manager.set_video_status(video, VideoStatus.COMPLETE)
    else:
        manager.set_video_status(video, VideoStatus.FAILED)
