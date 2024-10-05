import requests

from pprint import pprint

from tqdm import tqdm

token =  #тут нужно ввести токен вк

#1. Достаем 5 фотографий с вк.
class VKConnector:
    def __init__(self, access_token, version='5.199'):
        self.version = version
        self.access_token = access_token
        self.base_url = 'https://api.vk.com/method/'
        self.params = {
            'access_token': self.access_token,
            'v': self.version
        }

    def photos_get(self, user_id, album_id='profile', count=5):
        url = f'{self.base_url}photos.get'
        params = {
            **self.params,
            'owner_id': user_id,
            'album_id': album_id,
            'extended': 1,
            'count': count
        }
        response = requests.get(url, params=params)
        return response.json()

vk = VKConnector(token)
friends = vk.photos_get(id) #тут нужно ввести айди вк

#2. Большого размера.
def list_for_foto(friends):
    big_foto = {}
    for item in friends['items']:
        for size in item['sizes']:
            if size['type'] == 'y':
                big_foto[item['id']] = {'user_likes': item['user_likes'], 'type': size['type'], 'url': size['url']}
    return big_foto

images_url = list_for_foto(friends)
filename = images_url.get(['user_likes'])

#3. Скачиваем их.
res = requests.get(images_url)
with open(f'image/{filename}', 'wb') as f:
    f.write(res.content)

#4. Создаем папку на Я.Диске.
create_folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
params = {
    'path': 'vk'
}
headers = {
    'Authorization': 'OAuth #сюда пишите свой токен для яндекс диска'
}
res = requests.put(create_folder_url,
                   headers=headers,
                   params=params)

#5. Загружаем фото на Я.Диск.
upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
params = {
    'path': f'vk/{filename}'
}
res = requests.get(upload_url,
                   params=params,
                   headers=headers)
upload_link = res.json()['href']

with open(f'image/{filename}', 'rb') as f:
    res = requests.put(upload_link, files={'file': f})

for i in tqdm(range(100)):
    pass