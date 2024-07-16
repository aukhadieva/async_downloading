"""Запуск выполнения асинхронной функции main."""
import asyncio

from fetch_url import main

if __name__ == '__main__':
    urls = [
        'https://gitea.radium.group/radium/project-configuration.git/archive/master.zip',
        'https://gitea.radium.group/radium/project-configuration.git/archive/master.tar.gz',
        'https://gitea.radium.group/radium/project-configuration.git/archive/master.bundle',
    ]
    asyncio.run(main(urls))
