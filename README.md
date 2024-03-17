# VKArchive (Архивация всех переписок)
![Windows](https://img.shields.io/badge/os-windows-blue)
![Python 3.8](https://img.shields.io/badge/python-3.8+-blue)

## Введение: 
1. [Установка библиотек](https://github.com/eremeyko/VKArchive#%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%B1%D0%B8%D0%B1%D0%BB%D0%B8%D0%BE%D1%82%D0%B5%D0%BA%D0%B8)
2. [Получение токена](https://github.com/eremeyko/VKArchive#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0)

3. [Запуск](https://github.com/eremeyko/VKArchive#%D0%97%D0%B0%D0%BF%D1%83%D1%81%D0%BA)

4. [Информатион](https://github.com/eremeyko/VKArchive#%D0%98%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BE%D0%BD)
____
## Установка библиотеки
Для работы требуется только библиотека requests, но перед началось убедитесь, что вы установили Python не ниже версии 3.8!

Открываем консоль и вводим:
```
pip install requests
```
____
## Получение токена
Для работы необходим любой токен с доступом к messages.

Просто возьмите токен от [vk.com (*клик*)](https://oauth.vk.com/authorize?client_id=6287487&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1)
Токеном будет являться часть от `https://oauth.vk.com/blank.html#access_token=` до `&expires_in=86400...`
____
## Запуск
Дабл-клик по bat-нику.
____
## Информатион
Странная особенность: архивировать можно только первые 200 чатов, остальные он будет помечать как уже находящиеся в архиве. Не знаю с чем это связано, но благо всё работает

Если Вы введёте некорректный токен, то это никак не обработается, имейте в виду. Мне лень что-либо делать, будьте внимательны, ей богу
