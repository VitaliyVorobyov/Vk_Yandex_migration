import os
from dataclasses import dataclass

from environs import Env


@dataclass
class VkPhoto:
    token: str


@dataclass
class YandexDisk:
    token: str


@dataclass
class Settings:
    vk_photo: VkPhoto
    yandex_disk: YandexDisk


def get_settings(path: str) -> Settings:
    env = Env()
    env.read_env(path)
    token = input("Введите токен Яндекс.Диска: ")
    os.environ["YANDEX_TOKEN"] = token

    try:
        vk_photo_token = env.str('VK_TOKEN')
        yandex_disk_token = env.str('YANDEX_TOKEN')
    except Exception as e:
        raise ValueError("Ошибка при чтении переменных окружения: " + str(e))

    return Settings(
        vk_photo=VkPhoto(
            token=vk_photo_token
        ),
        yandex_disk=YandexDisk(
            token=yandex_disk_token
        )
    )


settings = get_settings('.env')
