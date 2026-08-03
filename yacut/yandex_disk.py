import asyncio
import aiohttp

from urllib import parse

from . import app


API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
DISK_INFO_URL = f'{API_HOST}{API_VERSION}/disk'

DISK_TOKEN = app.config['DISK_TOKEN']
AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}

REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


async def async_upload_files(files):
    if files is not None:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for file in files:
                tasks.append(
                    asyncio.ensure_future(
                        upload_file_and_get_url(session, file)
                    )
                )
            links = await asyncio.gather(*tasks)
        return links


async def upload_file_and_get_url(session, file):
    yandex_args = {
        'path': f'app:/{file.filename}',
        'overwrite': 'true',
    }

    async with session.get(
        headers=AUTH_HEADERS,
        params=yandex_args,
        url=REQUEST_UPLOAD_URL,
    ) as response:
        data = await response.json()
        upload_link = data['href']

    file_data = file.read()

    async with session.put(
        url=upload_link,
        data=file_data,
    ) as response:
        location = response.headers['Location']
        location = parse.unquote(location)
        location = location.replace('/disk', '')

    async with session.get(
        headers=AUTH_HEADERS,
        url=DOWNLOAD_LINK_URL,
        params={'path': f'{location}'}
    ) as response:
        data = await response.json()
        download_link = data['href']
        return download_link
