import os
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from typing import List

import yt_dlp

from model import Video, Subscription, VideoStatus


# import yt_dlp

# from urllib.request import urlopen

def download_video(download_path: str, video: Video) -> str:
    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s')
    }
    url = video.url
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = ydl.prepare_filename(info_dict)
            file_path = os.path.join(os.getcwd(), video_title)
            return True, file_path
    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")
        return False


def obtain_subscription_videos(subscription: Subscription) -> List[Video]:
    #
    #     # url = "https://www.youtube.com/feeds/videos.xml?channel_id=UC-UZjHl2kZ-6XKBLgbFgGAQ"
    #     #
    #     # response = urlopen(url)
    #     # xml_content = response.read()

    file_path = os.path.expanduser("~/tmp/output.xml")
    with open(file_path, "rb") as f:
        xml_content = f.read()

    root = ElementTree.fromstring(xml_content)
    entries = root.findall(".//{http://www.w3.org/2005/Atom}entry")

    video_list = []

    for entry in entries:
        video = Video(
            url=entry.find("{http://www.w3.org/2005/Atom}link[@rel='alternate']").get('href'),
            status=VideoStatus.PENDING,
            download_attempts=0,
            subscription=subscription,
            title=entry.findtext("{http://www.w3.org/2005/Atom}title"),
            created_at=datetime.strptime(entry.find("{http://www.w3.org/2005/Atom}published").text,
                                         "%Y-%m-%dT%H:%M:%S%z")
        )
        video_list.append(video)

    return video_list


class Fetcher:
    pass
