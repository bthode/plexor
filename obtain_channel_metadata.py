import urllib
from urllib.request import urlopen

from bs4 import BeautifulSoup

from model import Subscription


def fetch_rss_feed(subscription: Subscription) -> str:
    url = subscription.url
    req = urllib.request.urlopen(url)
    soup = BeautifulSoup(req.read(), 'html.parser')
    return soup.select_one('link[type="application/rss+xml"][title="RSS"]')['href']


# Don't fetch the file twice
def fetch_channel_title(subscription: Subscription) -> str:
    url = subscription.url
    req = urllib.request.urlopen(url)
    soup = BeautifulSoup(req.read(), 'html.parser')
    return soup.title.string
