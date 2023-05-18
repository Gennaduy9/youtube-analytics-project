import json
import os

from googleapiclient.discovery import build



class Channel:
    """Класс для ютуб-канала"""


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        channel_data = self.print_info()
        self.title = channel_data['items'][0]['snippet']['title']
        self.description = channel_data['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/UCMCgOm8GZkHp8zJ6l7_hIuA'
        self.subscriberCount = int(channel_data['items'][0]['statistics']['subscriberCount'])
        self.video_count = channel_data['items'][0]['statistics']['videoCount']
        self.view_count = channel_data['items'][0]['statistics']['viewCount']


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key: str = os.getenv('API_KEY1')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, file):
        data = self.print_info()
        with open(file, 'w') as outfile:
            json.dump(data, outfile)

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscriberCount + other.subscriberCount

    def __sub__(self, other):
        return self.subscriberCount - other.subscriberCount

    def __gt__(self, other):
        return self.subscriberCount > other.subscriberCount

    def __ge__(self, other):
        return self.subscriberCount >= other.subscriberCount

    def __lt__(self, other):
        return self.subscriberCount < other.subscriberCount

    def __le__(self, other):
        return self.subscriberCount <= other.subscriberCount

    def __eq__(self, other):
        return self.subscriberCount == other.subscriberCount
