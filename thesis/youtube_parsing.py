import sys

import django
from googleapiclient.discovery import  build

sys.path.append('/Users/alexandrurustin/Desktop/thesis/thesis/thesis')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thesis.settings")
django.setup()

from funfly.models import Youtube

DEVELOPER_KEY = "AIzaSyB1dJ9YC6wkueu8q3M9d4HpRUP_BKIS9Oo"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults = 20,
        order=u'relevance'
    ).execute()


    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                       search_result["id"]["videoId"]))
            youtube_id = search_result["id"]["videoId"]
            youtube_title = search_result["snippet"]["title"]
            youtube_url = 'https://www.youtube.com/embeded/' + youtube_id
            youtube_item = Youtube.objects.get_or_create(identifier=youtube_id, title=youtube_title, url=youtube_url)


        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                         search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                          search_result["id"]["playlistId"]))

    print "Videos:\n", "\n".join(videos), "\n"
    print "Channels:\n", "\n".join(channels), "\n"
    print "Playlists:\n", "\n".join(playlists), "\n"


    return videos

if __name__ == '__main__':
    youtube_search('funny')