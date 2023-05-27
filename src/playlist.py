import datetime
import os
import isodate
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('API_KEY1')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                               part='contentDetails, snippet',
                                                                 maxResults=50,
                                                                 ).execute()
        self.title = self.playlist_title()['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb"

    def playlist_title(self):
        playlist_videos = self.youtube.playlists().list(id=self.playlist_id,
                                                   part='snippet',
                                                   maxResults=50,
                                                   ).execute()
        return playlist_videos

    @property
    def total_duration(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response_st = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)).execute()
        duration = datetime.timedelta(0)
        for video in video_response_st['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response_st = self.youtube.videos().list(part='statistics',
                                                       id=','.join(video_ids)).execute()
        likeCount = 0
        likeCount_id = ''
        for video in video_response_st['items']:
            likeCount_item = int(video['statistics']['likeCount'])
            if likeCount_item > likeCount:
                likeCount_id = video['id']
        return f"https://youtu.be/{likeCount_id}"
