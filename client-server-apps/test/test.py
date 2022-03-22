# -*- coding: utf8 -*-
import logging
import sys
import os

# Создать регистратор верхнего уровня с именем 'app'
app_log = logging.getLogger('app')
app_log.setLevel(logging.INFO)
app_log.propagate = False


# имя файла
curr_dir = os.path.dirname(os.path.realpath(__file__))
print(curr_dir)
logging_file = os.path.join(curr_dir, 'log', 'app.log')
print(logging_file)

# Добавить несколько обработчиков в регистратор 'app'
app_log.addHandler(logging.FileHandler(logging_file))
app_log.addHandler(logging.StreamHandler(sys.stderr))

# Отправить несколько сообщений. Они попадут в файл app.log
# и будут выведены в поток sys.stderr
app_log.critical('Creeping death detected!')
app_log.info('FYI')

# Определить формат сообщений
_format = logging.Formatter("%(levelname)-10s %(asctime)s %(message)s")

# Создать обработчик, который выводит сообщения с уровнем CRITICAL в поток stderr
crit_hand = logging.StreamHandler(sys.stderr)
crit_hand.setLevel(logging.CRITICAL)
crit_hand.setFormatter(_format)

# Создать регистратор
log = logging.getLogger('basic')

# Добавить обработчик к регистратору
log.addHandler(crit_hand)
# Передать сообщение обработчику
log.critical('Oghr! Kernel panic!')