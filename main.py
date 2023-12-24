from utils import VkUtils, YandexUtils, SaveJson


def run():
    vk_utils = VkUtils()
    yandex_utils = YandexUtils()
    photos = list(vk_utils.get_photo_max_size())
    photo_upload = yandex_utils.upload_photo(photos)
    save_json = SaveJson(photo_upload)
    save_json.save_json()


if __name__ == '__main__':
    run()
