# Публикация комиксов

Скрипт скачивает случайно выбранный комикс с сайта [xkcd](https://xkcd.com/) и публикует его в паблике ВКонтакте.

## Как установить

Скачайте код
```
https://github.com/user-name-art/week6_api_comic.git
```
При необходимости создайте виртуальное окружение. Например: 
```
python -m venv .venv
``` 
Установите зависимости:
```
pip install -r requirements.txt
```

## Как запустить

Для работы понадобится файл **.env** (смотри **.env.template** для примера). 
* **VK_GROUP_ID** идентификатор группы ВКонтакте, можно узнать на [regvk.com](https://regvk.com/id/).
* **VK_ACCSESS_TOKEN** [access_token](https://vk.com/dev/implicit_flow_user) с соответствующими правами доступа ВКонтакте. Из запроса на получение ключа нужно убрать параметр *redirect_uri*, а для scope указать: *scope=photos,groups,wall*.

Запустите скрипт:
```
python main.py
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
