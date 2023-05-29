import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id: str):
        self.video_id = video_id
        video_data = self.video_response()
        try:
            self.video_title: str = video_data['items'][0]['snippet']['title']
            self.video_url: str = f"https://www.youtube.com/watch?v={video_id}"
            self.view_count: int = video_data['items'][0]['statistics']['viewCount']
            self.like_count: int = video_data['items'][0]['statistics']['likeCount']
        except IndexError:
            self.video_title = None
            self.like_count = None
        finally:
            print('Все работает! Ошибок нет.')

    def video_response(self):
        api_key: str = os.getenv('API_KEY1')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                     id=self.video_id
                                     ).execute()

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, pl_id: str):
        super().__init__(video_id)
        self.pl_id = pl_id