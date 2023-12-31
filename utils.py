from datetime import datetime
from dataclasses import dataclass
import json

from tqdm import tqdm

from vk import VkRequests
from yandex_disk import YandexDiskRequests


@dataclass
class VkUtils(VkRequests):
    def get_photo_max_size(self) -> any:
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
    name_directory: str = ''

    def __post_init__(self):
        select_type_directory = str(input('Введите "n" - для создания директории, "y" - для выбора директории: '))
        if select_type_directory == 'n':
            self.name_directory = str(input('Введите название создаваемой директории: '))
            self.name_directory = self.create_directory(self.name_directory)
        elif select_type_directory == 'y':
            self.name_directory = str(input('Введите название существующей директории: '))
        else:
            raise Exception('Введено некорректное значение')

    def get_photo_directory(self, name_directory: str) -> list:
        photo_json = self.get_info_directory(name_directory)
        name_photos_in_directory = [photo.get('name') for photo in photo_json.get('_embedded').get('items')]
        return name_photos_in_directory

    def upload_photo(self, photos: list, name_photos_in_directory: list, name_directory: str) -> list:
        photo_info = []
        for photo in tqdm(photos, desc='Process uploading photos:'):
            name = str(photo[1])
            prefix = datetime.fromtimestamp(photo[0]).strftime('%Y-%m-%d_%H-%M-%S')
            add_name = name + '_' + prefix
            link = photo[3]
            size = photo[2]
            if name in name_photos_in_directory and add_name in name_photos_in_directory:
                continue
            elif name not in name_photos_in_directory:
                self.upload(link, name, name_directory)
                photo_info.append({'file_name': name, 'size': size})
            elif name in name_photos_in_directory:
                self.upload(link, add_name, name_directory)
                photo_info.append({'file_name': add_name, 'size': size})
        if len(photo_info) == 0:
            print('No photos for uploading')
        return photo_info


@dataclass
class SaveJson:
    add_data: list

    def save_json(self) -> None:
        try:
            data = json.loads(open('data.json').read())
            data.extend(self.add_data)
            with open('data.json', 'w') as file:
                json.dump(data, file)
        except FileNotFoundError:
            data = self.add_data
            with open('data.json', 'w') as file:
                json.dump(data, file)
        return
