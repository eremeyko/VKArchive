#!/usr/bin/python
# -*- coding: utf8 -*-
from os import system
from time import sleep, time

from requests import post
from random import randint


already_in_archive = 0


def getDays(welcome_text):
    while True:
        system("cls")
        try:
            check = int(
                input(
                    f"{welcome_text}[?] Архивировать чаты с неактивностью более:\n ├[0] Все чаты | [1] 3 дня | [2] 7 дней | [3] 30 дней | [4] Свое значение\n └"
                )
            )
        except ValueError:
            continue
        # Да, у меня старая версия питона, и что?
        if check == 0:
            return 0
        elif check == 1:
            return 3 * 86400
        elif check == 2:
            return 7 * 86400
        elif check == 3:
            return 30 * 86400
        elif check == 4:
            try:
                return int(input("[•] Введите количество дней: ")) * 86400
            except ValueError:
                continue
        else:
            continue


def getChats(token, i, days):
    conversations_id = []
    while True:
        try:
            chats = post(
                "https://api.vk.com/method/messages.getConversations",
                data={"offset": i, "count": 200, "access_token": token, "v": 5.174},
                timeout=10,
            ).json()

            for j in chats["response"]["items"]:
                if days == 0:
                    conversations_id.append(j["conversation"]["peer"]["id"])
                else:
                    timeback = int(time()) - int(j["last_message"]["date"])
                    if timeback > days:
                        conversations_id.append(j["conversation"]["peer"]["id"])
            break
        except KeyError:
            sleep(randint(2,5))

    sleep(randint(1,3))
    own_id = post(
        "https://api.vk.com/method/users.get",
        data={"access_token": token, "v": "5.174"},
        timeout=10,
    ).json()["response"][0]["id"]

    if own_id in conversations_id:
        conversations_id.remove(own_id)
    if 100 in conversations_id:
        conversations_id.remove(100)

    return conversations_id


def printStatus(welcome_text, total, successful_archive, already_in_archive, flood_control, error_archive):
    system("cls")
    print(
        f"{welcome_text}[•] Всего чатов: {total}\n ├[v] Заархивировано:\t{successful_archive}\n ├[o] Уже в архиве:\t{already_in_archive}\n ├[x] Ошибок:\t\t{error_archive}\n └[f] Флуд контроль:\t{flood_control}"
    )


def archiveChats(token, conversations_id, welcome_text):
    global already_in_archive
    total = len(conversations_id)
    successful_archive = 0
    error_archive = 0
    flood_control = 0

    for peer_id in conversations_id:
        response = post(
            "https://api.vk.com/method/messages.archiveConversation",
            data={"access_token": token, "peer_id": peer_id, "v": "5.174"},
            timeout=10,
        ).json()
        if "error" in response:
            error_code = response["error"]["error_code"]
            if error_code == 6:
                flood_control += 1
                sleep(3)
                conversations_id.insert(0, peer_id)
            elif error_code == 100:
                error_archive += 1
            elif error_code == 964:
                already_in_archive += 1
                sleep(10)
        else:
            successful_archive += 1

        printStatus(welcome_text, total, successful_archive, already_in_archive, flood_control, error_archive)

    already_in_archive += successful_archive


def getChannels(token):
    # Каналы (id вида -229854243) не входят в messages.getConversations —
    # это отдельная сущность со своим недокументированным публично методом.
    # channels.get, как и messages.getConversations, по умолчанию отдаёт
    # только неархивные каналы — фильтровать по is_archived не нужно.
    response = post(
        "https://web.api.vk.ru/method/channels.get",
        params={"v": "5.282", "client_id": 6287487},
        data={"access_token": token},
        timeout=10,
    ).json()
    if "error" in response:
        return []
    return [item["channel"]["channel_id"] for item in response["response"]["items"]]


def archiveChannels(token, channel_ids):
    successful = 0
    failed = []
    for channel_id in channel_ids:
        response = post(
            "https://web.api.vk.ru/method/channels.archive",
            params={"v": "5.282", "client_id": 6287487},
            data={"channel_ids": channel_id, "access_token": token},
            timeout=10,
        ).json()
        if "error" in response:
            failed.append(channel_id)
        else:
            successful += 1
    return successful, failed


if __name__ == "__main__":
    welcome_text = f"""Просто собирает все диалоги и отправляет их в архив

Q: Зачем?\n\tA: Избавиться от мусора в чате\n  Q: А если мне нужны некоторые диалоги\n\tA: Тогда включите заранее на них уведомление и они сами вернутся в чат, когда поступит новое сообщение\n  Q: Почему в статусе есть счётчик "Уже в архиве"?\n\tA: Не архивируются только Вы сами и диалог с id100 — остальные чаты идут пачками по 200
{'_'*8}
"""
    while True:
        system("cls")
        token = input("Токен: ")

        chats = post(
            "https://api.vk.com/method/messages.getConversations",
            data={"offset": 0, "count": 200, "access_token": token, "v": 5.174},
            timeout=10,
        ).json()

        if "error" in chats:
            print("Введён неверный токен")
            sleep(2)
            continue
        else:
            chats = chats["response"]["count"]
            break

    days = getDays(welcome_text)

    for j in range(0, chats, 200):
        system("cls")
        print(
            f"{welcome_text}Собираем список\nБудет заархивированно ~{j+200 if chats > j else chats} чатов..."
        )
        list_id = getChats(token, j, days)
        if len(list_id) != 0:
            archiveChats(token, list_id, welcome_text)

    if days == 0:
        channel_ids = getChannels(token)
        if channel_ids:
            successful, failed = archiveChannels(token, channel_ids)
            print(f"Каналы: заархивировано {successful}, не удалось {len(failed)} {failed if failed else ''}")
