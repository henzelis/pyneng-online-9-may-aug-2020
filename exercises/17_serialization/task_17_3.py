# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""
import re


def parse_sh_cdp_neighbors(output):
    """
    Pasre 'show cdp neighbors' command output
    :param output: output of the command 'show cdp neighbors' command
    :return: dictionary with device connections
    """
    conf_regex = r'(\S+)>'
    priv_regex = r'(\S+)#'
    con_dict = {}
    con_port_dict = {}
    for line in output.strip().splitlines():
        host_match = re.search(conf_regex, line)
        if host_match:
            local_host = host_match.group(1)
        host_match_priv = re.search(priv_regex, line)
        if host_match_priv:
            local_host = host_match_priv.group(1)

    data = output.strip().splitlines()
    for line in data:
        if 'Device ID' in line:
            start_line = data.index(line) + 1

    for line in data[start_line:]:
        con_elements = re.split(r'  +', line)
        local_port = con_elements[1]
        if len(con_elements) < 6:
            regex = r'- (\S+.*)'
            result = re.search(regex, con_elements[-1])
            if result:
                remote_port = result.group(1)
        else:
            remote_port = con_elements[-1]
        remote_host = con_elements[0]
        con_port_dict[local_port] = {remote_host: remote_port}
    con_dict[local_host] = con_port_dict
    return con_dict

if __name__ == '__main__':
    with open('sh_cdp_n_sw1.txt') as f:
        data = f.read()
    result = parse_sh_cdp_neighbors(data)
    print(data)
    print(result)