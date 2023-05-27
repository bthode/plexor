import time
import random
# import yt_dlp


def fetch_video_url(video):
    print(f' Downloading video {video.title} at {video.url}')
    time.sleep(.5)
    if random.random() < 0.5:
        return True
    else:
        return False



    # ydl_opts = {
    #     'outtmpl': '%(title)s.%(ext)s',
    # }
    # try:
    #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #         ydl.download([video.url])
    #     return True
    # except Exception as e:
    #     print(f"An error occurred while downloading the video: {e}")
    #     return False


class Fetcher:
    pass
