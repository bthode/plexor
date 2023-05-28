import random


# import yt_dlp


def fetch_video_url(download_path, video):
    print(f' Downloading video {video.title} to {download_path}/{video.title}')
    if random.random() < 0.5:
        saved_path = "/path/filename"
        return True, saved_path
    else:
        return False, None

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
