from dataclasses import dataclass

import requests

from settings import settings


@dataclass
class VkRequests:
    owner_id: str = str(input('Введите id профиля ВК: '))
    url: str = 'https://api.vk.com/method'
    token: str = settings.vk_photo.token
    vk_api_version: str = '5.199'

    def get_photo_profile(self) -> dict:
        album_id: str = 'profile'
        method: str = '/photos.get'
        params: dict = {'access_token': self.token,
                        'v': self.vk_api_version,
                        'owner_id': self.owner_id,
                        'album_id': album_id,
                        'extended': '1'}
        response = requests.post(url=self.url+method, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"{response.status_code} - {response.json().get('error')}")
