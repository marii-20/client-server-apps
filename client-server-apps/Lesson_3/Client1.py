# -*- coding: utf8 -*-
# 1. Реализовать простое клиент-серверное взаимодействие
# по протоколу JIM (JSON instant messaging):
# клиент отправляет запрос серверу;
# сервер отвечает соответствующим кодом результата.
# Клиент и сервер должны быть реализованы в виде
# отдельных скриптов, содержащих соответствующие функции.
# Функции клиента: сформировать presence-сообщение;
# отправить сообщение серверу;
# получить ответ сервера;
# разобрать сообщение сервера;
# параметры командной строки скрипта
# client.py <addr> [<port>]:
# addr — ip-адрес сервера;
# port — tcp-порт на сервере, по умолчанию 7777.

from socket import *
import time
import argparse
import json


def parse_message(str1):  # разобрать сообщение сервера;
    serv_message = {}
    try:
        serv_message = json.loads(str1.decode('utf-8'))
        if serv_message["response"] in (100, 101, 102, 200, 201, 202):
            print("Сообщение доставлено на сервер, код возврата ", serv_message["response"], serv_message["alert"])
    except json.decoder.JSONDecodeError:
        print("Сообщение от сервера не распознано", str1)


def presence(username, status):  # сформировать presence-сообщение;
    return {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": username,
            "status": status
        }
    }


def message_from_user(from_user):  # сформировать presence-сообщение;
    to_user = input("Кому отправить сообщение:")
    msg = input("Введите сообщение:")
    return {
        "action": "msg",
        "time": time.time(),
        "to": to_user,
        "from": from_user,
        "encoding": "utf-8",
        "message": msg
    }


def send_message(msg, s):  # отправить сообщение серверу;
    print("Sending message %s" % msg)
    s.send(msg.encode('utf-8'))


def get_response(s):  # получить ответ сервера;
    data = s.recv(1024)
    parse_message(data)


def communicate(msg, resp, host, port):
    print("Попытка соединения с %s по порту %s" % (host, port))
    my_socket = socket(AF_INET, SOCK_STREAM)
    try:
        my_socket.connect((host, port))
    except ConnectionRefusedError:
        print("Сервер %s недоступен по порту %s" % (host, port))
    send_message(msg, my_socket)
    resp = get_response(my_socket)
    my_socket.close()


# получить и обработать параметры командной строки
def parse_args():
    parser = argparse.ArgumentParser(description='Client App')
    parser.add_argument("-a", action="store", dest="addr", type=str, default='localhost',
                        help="enter IP address, default is localhost")
    parser.add_argument("-p", action="store", dest="port", type=int, default=7777,
                        help="enter port number, default is 7777")
    return parser.parse_args()


def main():
    args = parse_args()
    port = args.port
    host = args.addr
    resp = ''
    msg = json.dumps(presence("Nastya", "Yep, I am here!"))
    communicate(msg, resp, host, port)
    msg = json.dumps(message_from_user("Nastya"))
    communicate(msg, resp, host, port)


# Entry point
if __name__ == '__main__':
    main()
