import os
import requests
import random
from environs import Env


API_VERSION = 5.131


def get_image_by_url(photo_url):
    response = requests.get(photo_url)
    response.raise_for_status()

    return response.content


def get_random_comic_number():
    last_comic_url = 'https://xkcd.com/614/info.0.json'

    response = requests.get(last_comic_url)
    response.raise_for_status()
    number_of_comics = response.json()['num']
    random_comic_number = random.randint(1,number_of_comics)

    return random_comic_number


def get_comic_data(comic_number):
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def save_image_to_disk(image):
    with open('comic.png', 'wb') as file:
        file.write(image)


def get_upload_url_vk(group_id, token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'group_id': group_id,
        'access_token': token,
        'v': API_VERSION,
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.json()['response']['upload_url']


def post_image_to_vk(group_id, token, url):
    with open('comic.png', 'rb') as file:
        files = {'photo': file}
        response = requests.post(url, files=files)
        response.raise_for_status()
    
    return response.json()


def save_image_to_vk(group_id, token, upload_image_data):
    payload = {
        'group_id': group_id,
        'photo': upload_image_data['photo'],
        'server': upload_image_data['server'],
        'hash': upload_image_data['hash'],
        'access_token': token,
        'v': API_VERSION,
    }

    url = 'https://api.vk.com/method/photos.saveWallPhoto'

    response = requests.post(url, data=payload)
    response.raise_for_status()

    return response.json()['response'][0]


def post_image_to_wall(group_id, token, data, text):
    payload = {
        'group_id': group_id,
        'owner_id': -group_id,
        'from_group': 1,
        'attachments': f'photo{data["owner_id"]}_{data["id"]}',
        'message': text,
        'access_token': token,
        'v': API_VERSION,
    }

    url = 'https://api.vk.com/method/wall.post'

    response = requests.post(url, data=payload)
    response.raise_for_status()

    return response.json()


def main():
    env = Env()
    env.read_env()
    token = env.str('VK_ACCSESS_TOKEN')
    group_id = env.int('VK_GROUP_ID')

    random_comic_number = get_random_comic_number()
    comic_response_data = get_comic_data(random_comic_number)
    comic_text = comic_response_data['alt']
    image = get_image_by_url(comic_response_data['img'])
    save_image_to_disk(image)

    upload_url = get_upload_url_vk(group_id, token)
    upload_image_data = post_image_to_vk(group_id, token, upload_url)
    save_image_data = save_image_to_vk(group_id, token, upload_image_data)

    post_image_to_wall(group_id, token, data=save_image_data, text=comic_text)

    os.remove('./comic.png')


if __name__ == '__main__':
    main()