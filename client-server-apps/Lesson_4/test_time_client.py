# -*- coding: utf8 -*-
# Для всех функций из урока 3 написать тесты с использованием unittest.
# Они должны быть оформлены в отдельных скриптах с префиксом test_
# в имени файла (например, test_client.py).
import unittest
import time
from time_client import get_time_server


# эмуляция сервера времени
def mock_time_server():
    timestr = time.ctime(time.time()) + "\n"
    return timestr


class TestTime(unittest.TestCase):
    # проверяет, что время возвращаемое сервером совпадает с временем клиента
    def test_check_time(self):
        self.assertEqual(get_time_server(), mock_time_server())

    # проверяет что в строке, возвращаемой сервером, присутствуют день недели и месяц
    def test_format(self):
        self.assertRegex(get_time_server(),
                         "(Mon|Tue|Wed|Thu|Fri|Sat|Sun)(\s+)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\s+)(.+)")
        # (?i)([\d]{1,2}(\s)?)


if __name__ == "__main__":
    print(get_time_server())
    print(mock_time_server())
    unittest.main()
