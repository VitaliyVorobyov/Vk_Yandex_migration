from tqdm import tqdm

from utils import VkUtils, YandexUtils, SaveJson


def run():
    photo = list(VkUtils().get_photo_max_size())

    try:
        photo_upload = YandexUtils().upload_photo(photo)
    except AttributeError:
        YandexUtils().create_directory()
        photo_upload = YandexUtils().upload_photo(photo)

    SaveJson(photo_upload).save_json()


if __name__ == '__main__':
    for i in tqdm(range(1), desc='Program process:'):
        run()
