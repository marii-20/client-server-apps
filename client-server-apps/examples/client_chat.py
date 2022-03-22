import datetime
import json
from json import JSONDecodeError
from socket import *
from threading import Thread


class SockHandler():
    ''' Базовый класс для работы с сокетом
    '''

    def __init__(self, sock):
        self.sock = sock
        self.is_alive = False

    def __call__(self):
        ''' Класс-наследник должен выставить флаг is_alive = True '''
        raise NotImplemented

    def stop(self):
        self.is_alive = False


class ConsoleHandler(SockHandler):
    ''' Обработчик ввода из консоли
    '''

    _name = ''

    def __init__(self, sock, name):
        super().__init__(sock)
        self._name = name

    def __call__(self):
        while True:
            data = input('>>')

            if data == 'exit':
                break

            msg = {
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "name": self._name,
                "message": data
            }

            self.sock.send(json.dumps(msg).encode('utf-8'))  # Отправить!


class ClientChat:

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.name = ''

    def start_chat_loop(self):
        # Начиная с Python 3.2 сокеты имеют протокол менеджера контекста
        # При выходе из оператора with сокет будет автоматически закрыт
        with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
            try:
                sock.connect((self.address, self.port))  # Соединиться с сервером
            except ConnectionRefusedError as e:
                print("Connection exception")
                return

            self.name = input('Введите ваше имя в чате: ')

            sender = ConsoleHandler(sock=sock, name=self.name)
            th_sender = Thread(target=sender)
            th_sender.daemon = True
            th_sender.start()

            while True:
                dataJsonStr = sock.recv(10000000)
                if not dataJsonStr or dataJsonStr == '':
                    break
                try:
                    data = json.loads(dataJsonStr)
                except JSONDecodeError:
                    pass
                else:
                    print("\n{} - {} : {}".format(data['time'], data['name'], data['message']))


if __name__ == '__main__':
    client = ClientChat('localhost', 10000)

    client.start_chat_loop()
