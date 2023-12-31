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

    def create_directory(self, name_directory: str) -> str:
        params: dict = {'path': name_directory}
        response = requests.put(self.url, headers=self.headers, params=params)
        if response.status_code == 409:
            name_directory = str(input('Директория с таким названием уже существует. Введите другое название: '))
            return self.create_directory(name_directory)
        elif response.status_code == 200 or 201:
            return name_directory
        else:
            raise Exception(f"{response.status_code} - {response.json().get('message')}")

    def get_info_directory(self, name_directory: str) -> dict:
        params: dict = {'path': name_directory}
        response = requests.get(self.url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            self.create_directory(name_directory)
            return response.json()
        else:
            raise Exception(f"{response.status_code} - {response.json().get('message')}")

    def upload(self, url_photo: str, filename: str, name_directory: str) -> None:
        method: str = '/upload'
        params: dict = {'path': f'{name_directory}/{filename}', 'url': url_photo}
        response = requests.post(self.url+method, headers=self.headers, params=params)
        if response.status_code == 200 or 202:
            return
        else:
            raise Exception(f"{response.status_code} - {response.json().get('message')}")
