# -*- coding: utf-8 -*-
"""
Задание 17.3b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно, чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии, но и удалять дублирующиеся соединения (их лучше всего видно на схеме, которую генерирует draw_topology).

Проверить работу функции на файле topology.yaml (должен быть создан в задании 17.3a).
На основании полученного словаря надо сгенерировать изображение топологии с помощью функции draw_topology.
Не копировать код функции draw_topology.

Результат должен выглядеть так же, как схема в файле task_17_3b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть дублирующихся линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

"""
import yaml
import draw_network_graph

def transform_topology(file_name):
    """
    Transfor file to topology file
    :param file_name: name of the yaml file
    :return: dictionary
    """
    with open(file_name) as f:
        data = yaml.safe_load(f)
    connect_dict = {}
    clear_dict = {}
    for key in data.keys():
        for port in data[key].keys():
            local_port = (key, port)
            remote_port = tuple(data[key][port].items())[0]
            connect_dict[local_port] = remote_port
    for key, value in connect_dict.items():
        if key not in clear_dict.values():
            clear_dict[key] = value
    return clear_dict

if __name__ == "__main__":
    topology = transform_topology('topology.yaml')
    draw_network_graph.draw_topology(topology)
