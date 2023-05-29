import os
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from typing import List, Union
from urllib.request import urlopen

import yt_dlp

import config
from model import Video, Subscription, VideoStatus


def download_video(download_path: str, video: Video, dry_run: bool) -> Union[tuple[bool, str], bool]:
    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s')
    }
    should_download = not dry_run
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video.url, download=should_download)
            video_title = ydl.prepare_filename(info_dict)
            file_path = os.path.join(os.getcwd(), video_title)
            return True, file_path
    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")
        return False


def obtain_subscription_videos(subscription: Subscription) -> List[Video]:
    response = urlopen(subscription.rss_feed_url)
    xml_content = response.read()
    root = ElementTree.fromstring(xml_content)
    entries = root.findall(f".//{config.entry}")

    video_list = []

    for entry in entries:
        video = Video(
            url=entry.find(config.entry_link).get('href'),
            status=VideoStatus.PENDING,
            download_attempts=0,
            subscription=subscription,
            title=entry.findtext(config.entry_title),
            created_at=datetime.strptime(entry.find(config.entry_published).text,
                                         config.iso_8601_tz)
        )
        video_list.append(video)

    return video_list


class Fetcher:
    pass
