import json

from plexapi.server import PlexServer
from plexapi.video import Movie

# Set up connection to Plex server
plex = PlexServer('<YOUR_PLEX_URL>', '<YOUR_PLEX_TOKEN>', timeout=1800)

# Load JSON metadata file from yt-dlp
with open("<PATH_TO_YT-DLP_JSON_FILE>") as f:
    json_data = json.load(f)

# Extract relevant metadata from JSON file
title = json_data['title']
summary = json_data['description']
duration = json_data['duration']
year = json_data['upload_date'].split('-')[0]
thumb_url = json_data['thumbnails'][0]['url']
media_url = json_data['url']

# Upload metadata to Plex server as a new movie
movie = Movie(
    parent=None,
    title=title,
    summary=summary,
    duration=duration,
    year=year,
    thumb=thumb_url,
    art=thumb_url
)

plex.library.section("<PLEX_SECTION_NAME>").addItems([movie], scan=False)
