#!/usr/bin/python
# -*- coding: utf8 -*-
from os import system
from time import sleep

from requests import post


def getChats(token, i):
    conversations_id = []
    chats = post(
        "https://api.vk.com/method/messages.getConversations",
        data={"offeset": i, "count": 200, "access_token": token, "v": 5.174},
    ).json()
    for j in chats["response"]["items"]:
        conversations_id.append(j["conversation"]["peer"]["id"])

    return conversations_id


def archiveChats(token, conversations_id):
    successful_archive = 0
    error_archive = 0
    flood_control = 0
    already_in_archive = 0
    conversations_id.remove(100)
    conversations_id.remove(
        post(
            "https://api.vk.com/method/users.get",
            data={"access_token": token, "v": "5.174"},
        ).json()["response"][0]["id"]
    )
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
                    f"[•] Всего чатов: {len(conversations_id)}\n ├[v] Заархивировано:\t{successful_archive} \n └[f] Флуд контроль:\t{flood_control}"
                )
                conversations_id.insert(0, peer_id)
            if response["error"]["error_code"] == 100:
                error_archive += 1
                system("cls")
                print(
                    f"[•] Всего чатов: {len(conversations_id)}\n ├[v] Заархивировано:\t{successful_archive} \n └[f] Флуд контроль:\t{flood_control}"
                )
            elif response["error"]["error_code"] == 964:
                already_in_archive += 1
                system("cls")
                print(
                    f"[•] Всего чатов: {len(conversations_id)}\n ├[v] Заархивировано:\t{successful_archive} \n └[f] Флуд контроль:\t{flood_control}"
                )
                sleep(10)
            else:
                pass
        else:
            successful_archive += 1
            system("cls")
            print(
                f"[•] Всего чатов: {len(conversations_id)}\n ├[v] Заархивировано:\t{successful_archive} \n └[f] Флуд контроль:\t{flood_control}"
            )
            pass
    return 0


if __name__ == "__main__":
    print("Просто собирает все диалоги и отправляет их в архив")
    token = input("Токен: ")
    chats = post(
        "https://api.vk.com/method/messages.getConversations",
        data={"offeset": 0, "count": 200, "access_token": token, "v": 5.174},
    ).json()["response"]["count"]

    for j in range(0, chats, 200):
        system("cls")
        print(
            f"\n  Q: Зачем?\n\tA: Избавиться от мусора в чате\n  Q: А если мне нужны некоторые диалоги\n\tA: Тогда включите заранее на них уведомление и они сами вернутся в чат, когда поступит новое сообщение\n  Q: Почему он постоянно перезапускается?\n\tA: Особенность vk api, архивируется первые 200 чатов (Не включая Вас и id100 — их нельзя архивировать)\n\nСобираем список\tАрхивированно чатов: ~{j+200 if chats > j else chats}..."
        )
        list_id = getChats(token, j)
        print(f"[i] Всего будет заархивировано {len(list_id)} чатов.")
        check = archiveChats(token, list_id)
