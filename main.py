import os
import requests
import random

from pathlib import Path
from environs import Env


API_VERSION = 5.131


class VkError(Exception):
    def __init__(self, error_code, error_message):
        super().__init__(f'Error code: {error_code}, Error message: {error_message}')
        self.error_code = error_code
        self.error_message = error_message


def save_comic_image_to_disk(image):
    with open('comic.png', 'wb') as file:
        file.write(image)


def check_vk_response(answer):
    if 'error' in answer:
        error_code = answer['error']['error_code']
        error_message = answer['error']['error_msg']
        raise VkError(error_code, error_message)


def get_random_comic():
    last_comic_url = 'https://xkcd.com/info.0.json'

    response = requests.get(last_comic_url)
    response.raise_for_status()
    number_of_comics = response.json()['num']
    random_comic_number = random.randint(1,number_of_comics)

    comic_url = f'https://xkcd.com/{random_comic_number}/info.0.json'
    response = requests.get(comic_url)
    response.raise_for_status()    

    random_comic_text = response.json()['alt']
    random_comic_image_url = response.json()['img']

    response = requests.get(random_comic_image_url)
    response.raise_for_status()

    return response.content, random_comic_text


def get_upload_url_vk(group_id, token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'group_id': group_id,
        'access_token': token,
        'v': API_VERSION,
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    response_params = response.json()

    check_vk_response(response_params)

    return response_params['response']['upload_url']


def upload_image_to_vk(group_id, token, url):
    with open('comic.png', 'rb') as file:
        files = {'photo': file}
        response = requests.post(url, files=files)
    
    response.raise_for_status()

    response_params = response.json()

    check_vk_response(response_params)
    
    return response_params['photo'], response_params['server'], response_params['hash']


def save_image_to_vk(group_id, token, vk_photo, vk_server, vk_hash):
    payload = {
        'group_id': group_id,
        'photo': vk_photo,
        'server': vk_server,
        'hash': vk_hash,
        'access_token': token,
        'v': API_VERSION,
    }

    url = 'https://api.vk.com/method/photos.saveWallPhoto'

    response = requests.post(url, data=payload)
    response.raise_for_status()

    response_params = response.json()

    check_vk_response(response_params)

    return response_params['response'][0]['owner_id'], response_params['response'][0]['id']


def post_image_to_wall(group_id, token, owner_id, media_id, text):
    payload = {
        'group_id': group_id,
        'owner_id': -group_id,
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': text,
        'access_token': token,
        'v': API_VERSION,
    }

    url = 'https://api.vk.com/method/wall.post'

    response = requests.post(url, data=payload)
    response.raise_for_status()

    response_params = response.json()

    check_vk_response(response_params)

    return response_params


def main():
    env = Env()
    env.read_env()
    token = env.str('VK_ACCSESS_TOKEN')
    group_id = env.int('VK_GROUP_ID')

    try:
        image, comic_text = get_random_comic()
        save_comic_image_to_disk(image)
        
        upload_url = get_upload_url_vk(group_id, token)
        vk_photo, vk_server, vk_hash = upload_image_to_vk(group_id, token, upload_url)
        owner_id, media_id = save_image_to_vk(group_id, token, vk_photo, vk_server, vk_hash)

        post_image_to_wall(group_id, token, owner_id, media_id, text=comic_text)

    finally:
        os.remove(Path.cwd() / 'comic.png')


if __name__ == '__main__':
    main()
