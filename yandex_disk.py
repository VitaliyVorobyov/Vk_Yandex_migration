from dataclasses import dataclass

import requests

from settings import settings


@dataclass
class YandexDiskRequests:
    token: str = settings.yandex_disk.token
    url: str = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'OAuth {token}'
    }

    def create_directory(self) -> dict:
        params: dict = {'path': 'vk_photo'}
        response = requests.put(self.url, headers=self.headers, params=params).json()
        return response

    def get_info_directory(self) -> dict:
        params: dict = {'path': 'vk_photo'}
        response = requests.get(self.url, headers=self.headers, params=params).json()
        return response

    def upload(self, url_photo: str, filename: str) -> dict:
        method: str = '/upload'
        params: dict = {'path': f'vk_photo/{filename}', 'url': url_photo}
        response = requests.post(self.url+method, headers=self.headers, params=params).json()
        return response
