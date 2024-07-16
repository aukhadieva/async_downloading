"""Функции для асинхронной загрузки содержимого URL."""
import asyncio
import hashlib
import os
import tempfile
from pathlib import Path
from typing import List

import aiohttp

TEMPORARY_FOLDER = tempfile.mkdtemp()
TEMPORARY_DIR = Path(TEMPORARY_FOLDER)
LOADED_FILE_PATH = os.path.join(TEMPORARY_DIR, 'loaded_file')
FOLDERS_HASH = hashlib.sha256()
HASH_PATH = os.path.join(TEMPORARY_DIR, 'hash')


async def fetch_url(url: str) -> bytes:
    """
    Асинхронная функция для загрузки содержимого URL.

    Сохраняет данные во временную папку.
    Подсчитывает sha256 хэши от каждого файла.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                response_data = await response.content.read()

                with open(LOADED_FILE_PATH, 'wb') as file_for_download:
                    file_for_download.write(response_data)

                with open(LOADED_FILE_PATH, 'rb') as hash_file:
                    FOLDERS_HASH.update(hash_file.read())

                with open(HASH_PATH, 'w') as new_file:
                    new_file.write(FOLDERS_HASH.hexdigest())

                print(LOADED_FILE_PATH)
                return response_data

    except aiohttp.ClientError as error:
        raise aiohttp.ClientError(error)


async def main(urls: List[str]) -> None:
    """Основная функция для запуска."""
    tasks = [fetch_url(url) for url in urls]
    await asyncio.gather(*tasks)
