from utils import VkUtils, YandexUtils, SaveJson


def run():
    vk_utils = VkUtils()
    yandex_utils = YandexUtils()
    name_directory = yandex_utils.name_directory
    photos = list(vk_utils.get_photo_max_size())
    name_photos_in_directory = yandex_utils.get_photo_directory(name_directory)
    photo_upload = yandex_utils.upload_photo(photos, name_photos_in_directory, name_directory)
    save_json = SaveJson(photo_upload)
    save_json.save_json()


if __name__ == '__main__':
    run()
