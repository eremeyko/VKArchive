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
        check = int(
            input(
                f"{welcome_text}[?] Архивировать чаты с неактивностью более:\n ├[0] Все чаты | [1] 3 дня | [2] 7 дней | [3] 30 дней | [4] Свое значение\n └"
            )
        )
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
            return int(input("[•] Введите количество дней: ")) * 86400
        else:
            continue


def getChats(token, i, days):
    conversations_id = []
    while True:
        try:
            chats = post(
                "https://api.vk.com/method/messages.getConversations",
                data={"offeset": i, "count": 200, "access_token": token, "v": 5.174},
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
    try:
        conversations_id.remove(
            post(
                "https://api.vk.com/method/users.get",
                data={"access_token": token, "v": "5.174"},
            ).json()["response"][0]["id"]
        )
        conversations_id.remove(100)
    except ValueError:
        pass 

    return conversations_id


def archiveChats(token, conversations_id, welcome_text):
    global already_in_archive
    successful_archive = 0
    error_archive = 0
    flood_control = 0

    for peer_id in conversations_id:
        response = post(
            "https://api.vk.com/method/messages.archiveConversation",
            data={"access_token": token, "peer_id": peer_id, "v": "5.174"},
        ).json()
        if "error" in response:
            if response["error"]["error_code"] == 6:
                flood_control += 1
                sleep(3)
                system("cls")
                print(
                    f"{welcome_text}[•] Всего чатов: {len(conversations_id)}\n ├[v] Заархивировано:\t{successful_archive}\n ├[o] Уже в архиве:\t{already_in_archive}\n └[f] Флуд контроль:\t{flood_control}"
                )
                conversations_id.insert(0, peer_id)
            if response["error"]["error_code"] == 100:
                error_archive += 1
                system("cls")
                print(
                    f"{welcome_text}[•] Всего чатов: {len(conversations_id)}\n ├[v] Заархивировано:\t{successful_archive}\n ├[o] Уже в архиве:\t{already_in_archive}\n └[f] Флуд контроль:\t{flood_control}"
                )
            elif response["error"]["error_code"] == 964:
                already_in_archive += 1
                system("cls")
                print(
                    f"{welcome_text}[•] Всего чатов: {len(conversations_id)}\n ├[v] Заархивировано:\t{successful_archive}\n ├[o] Уже в архиве:\t{already_in_archive}\n └[f] Флуд контроль:\t{flood_control}"
                )
                sleep(10)
        else:
            successful_archive += 1
            system("cls")
            print(
                f"{welcome_text}[•] Всего чатов: {len(conversations_id)}\n ├[v] Заархивировано:\t{successful_archive}\n ├[o] Уже в архиве:\t{already_in_archive}\n └[f] Флуд контроль:\t{flood_control}"
            )
    already_in_archive += successful_archive

if __name__ == "__main__":
    welcome_text = f"""Просто собирает все диалоги и отправляет их в архив

Q: Зачем?\n\tA: Избавиться от мусора в чате\n  Q: А если мне нужны некоторые диалоги\n\tA: Тогда включите заранее на них уведомление и они сами вернутся в чат, когда поступит новое сообщение\n  Q: Почему он постоянно перезапускается?\n\tA: Особенность vk api, архивируется первые 200 чатов (Не включая Вас и id100 — их нельзя архивировать)
{'_'*8}
"""
    while True:
        system("cls")
        token = input("Токен: ")

        chats = post(
            "https://api.vk.com/method/messages.getConversations",
            data={"offeset": 0, "count": 200, "access_token": token, "v": 5.174},
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
