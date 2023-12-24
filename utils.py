from datetime import datetime
from dataclasses import dataclass
import json

from vk import VkRequests
from yandex_disk import YandexDiskRequests


@dataclass
class VkUtils(VkRequests):

    def get_photo_max_size(self):
        photos = self.get_photo_profile().get('response').get('items')
        for info in photos:
            max_size = max(info.get('sizes'), key=lambda el: el['height'])
            date = info.get('date')
            like_count = info.get('likes').get('count')
            url = max_size.get('url')
            size = max_size.get('type')
            yield date, like_count, size, url


@dataclass
class YandexUtils(YandexDiskRequests):
    def get_name_photo(self):
        photo_json = self.get_info_directory()
        for photo in photo_json.get('_embedded').get('items'):
            yield photo.get('name')

    def upload_photo(self, photos: list) -> any:
        directory = list(self.get_name_photo())
        photo_info = []
        for photo in photos:
            name = str(photo[1])
            prefix = datetime.fromtimestamp(photo[0]).strftime('%Y-%m-%d_%H-%M-%S')
            add_name = name + '_' + prefix
            link = photo[3]
            size = photo[2]
            if name in directory and add_name in directory:
                continue
            elif name not in directory:
                self.upload(link, name)
                photo_info.append({'file_name': name, 'size': size})
            elif name in directory:
                self.upload(link, add_name)
                photo_info.append({'file_name': add_name, 'size': size})
        return photo_info


@dataclass
class SaveJson:
    add_data: dict

    def save_json(self):
        try:
            data = json.loads(open('data.json').read())
            data.extend(self.add_data)
            with open('data.json', 'w') as file:
                json.dump(data, file)
        except FileNotFoundError:
            data = self.add_data
            with open('data.json', 'w') as file:
                json.dump(data, file)
