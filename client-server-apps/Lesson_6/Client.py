# -*- coding: utf8 -*-
# Продолжая задачу логирования, реализовать декоратор @log, фиксирующий
# обращение к декорируемой функции. Он сохраняет ее имя и аргументы.
# В декораторе @log реализовать фиксацию функции, из которой была вызвана
# декорированная. Если имеется такой код:
# @log
# def func_z():
#     pass
#
# def main():
#     func_z()
#
# ...
# в логе должна быть отражена информация:
# # "<дата-время> Функция func_z() вызвана из функции main"

from socket import *
import time
import argparse
import json
import logging
import inspect
import client_log_config

cli_log = logging.getLogger('client')

enable_tracing = True

def log(func):
    if enable_tracing:
        def callf(*args,**kwargs):
            cli_log.info("Функция %s: вызвана из функции  %s" % (func.__name__ , inspect.stack()[1][3]))
            r = func(*args, **kwargs)
            cli_log.info("%s вернула %s" % (func.__name__, r))
            return r
        return callf
    else:
        return func


@log
def parse_message(str1):  # разобрать сообщение сервера;
    serv_message = {}
    try:
        serv_message = json.loads(str1.decode('utf-8'))
        if serv_message["response"] in (100, 101, 102, 200, 201, 202):
            cli_log.info("Сообщение доставлено на сервер, код возврата %s, %s " % (
            str(serv_message["response"]), serv_message["alert"]))
    except json.decoder.JSONDecodeError:
        cli_log.critical("Сообщение от сервера не распознано: %s ", str1)


@log
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


@log
def message_from_user(from_user):  # сформировать presence-сообщение;
    to_user = ""
    while (len(to_user) == 0) or (len(to_user) > 25):
        to_user = input("Кому отправить сообщение:")
        if (len(to_user) == 0) or (len(to_user) > 25):
            print("имя пользователя/название чата должно содержать от 1 до 25 символов")
    msg = ""
    while (len(msg) == 0) or (len(msg) > 500):
        msg = input("Введите сообщение:")
        if (len(msg) == 0) or (len(msg) > 500):
            print("сообщение должно содержать максимум 500 символов")
    return {
        "action": "msg",
        "time": time.time(),
        "to": to_user,
        "from": from_user,
        "encoding": "utf-8",
        "message": msg
    }


@log
def send_message(msg, s):  # отправить сообщение серверу;
    cli_log.info("Sending message %s" % msg)
    s.send(msg.encode('utf-8'))


@log
def get_response(s):  # получить ответ сервера;
    data = s.recv(1024)
    parse_message(data)


@log
def communicate(msg, resp, host, port):
    cli_log.info("Попытка соединения с %s по порту %s" % (host, port))
    my_socket = socket(AF_INET, SOCK_STREAM)
    try:
        my_socket.connect((host, port))
    except ConnectionRefusedError:
        cli_log.critical("Сервер %s недоступен по порту %s" % (host, port))
        return
    except OSError as err:
        cli_log.critical("OS error: {0}".format(err))
        return
    else:
        cli_log.info("Подключен к %s по порту %s" % (host, port))
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
    cli_log.debug('Старт приложения')
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
