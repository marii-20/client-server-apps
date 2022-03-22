# -*- coding: utf8 -*-
# Для всех функций из урока 3 написать тесты с использованием unittest.
# Они должны быть оформлены в отдельных скриптах с префиксом test_
# в имени файла (например, test_client.py).

# Программа клиента, запрашивающего текущее время
from socket import *


# функция получения времени с сервера
def get_time_server():
    s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
    s.connect(('localhost', 8888))  # Соединиться с сервером
    tm = s.recv(1024)  # Принять не более 1024 байтов данных
    s.close()
    return tm.decode('ascii')


if __name__ == "__main__":
    print(get_time_server())
