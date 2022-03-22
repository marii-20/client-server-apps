# coding=cp1251
# 2. ������� �� ����������� ������ �� ������ json.
# ���� ���� orders � ������� JSON � ����������� � �������. �������� ������,
# ���������������� ��� ���������� �������.
# ��� �����:
# ������� ������� write_order_to_json(), � ������� ���������� 5 ���������� �
# ����� (item), ���������� (quantity), ���� (price), ���������� (buyer), ����
# (date). ������� ������ ���������������  ������ ������ � ���� ������� � ����
# orders.json. ��� ������ ������ ������� �������� ������� � 4 ���������� �������;
# ��������� ������ ��������� ����� ����� ������� write_order_to_json() � ���������
# � ��� �������� �������
# ���������. ###

import json


def read_orders_from_json():
    with open('orders.json') as f_n:
        orders = json.load(f_n)
        return orders


def write_order_to_json(orders, item, quantity, price, buyer, date):
    new_data = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }
    orders["orders"].append(new_data)
    with open('orders.json', 'w') as o_j:
        o_j.write(json.dumps(orders, indent=4))


# ������ ������� ������ ������� �� �����
orders_list = read_orders_from_json()
# print("������ �������: ", orders_list)
# ��������� ������ � ����� � ����
# write_order_to_json(orders_list, 'fork', 5, 124, 'Jane', '25.10.2018')
# write_order_to_json(orders_list, 'table', 2, 2099, 'Mark', '16.10.2018')
write_order_to_json(orders_list, 'spoon', 5, 125, 'James', '23.10.2018')
write_order_to_json(orders_list, 'table', 200, 2099, 'Natalie', '19.10.2018')
