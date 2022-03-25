# -*- coding: utf-8 -*-
"""
Задание 17.2

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv), в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы:
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
Вы можете раскомментировать строку print(sh_version_files), чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""
import re
import csv
import glob

sh_version_files = glob.glob("sh_vers*")
# print(sh_version_files)

headers = ["hostname", "ios", "image", "uptime"]

def parse_sh_version(output):
    """
    Parsing show version output
    :param output: string with output from the device
    :return: tuple with ios, image, uptime
    """
    image_regex = r'file is \"(\S+)\"'
    ios_regex = "IOS.*Version (\S+),"
    uptime_regex = r'uptime is (.*)'
    for line in output.splitlines():
        ios_match = re.search(ios_regex, line)
        if ios_match:
            ios = ios_match.group(1)
        image_match = re.search(image_regex, line)
        if image_match:
            image = image_match.group(1)
        uptime_match = re.search(uptime_regex, line)
        if uptime_match:
            uptime = uptime_match.group(1)
    version = (ios, image, uptime)
    return version

def write_inventory_to_csv(data_filenames, csv_filename):
    """
    Write inventory information to csv
    :param data_filenames: names of the files
    :param csv_filename: name of cvs file to write out
    :return: None
    """
    out = []
    headers = ["hostname", "ios", "image", "uptime"]
    out.append(headers)
    for file in data_filenames:
        hostname = file.replace('sh_version_', '').replace('.txt', '')
        with open(file) as f:
            data = f.read()
            version = list(parse_sh_version(data))
            version.insert(0, hostname)
            out.append(version)
    with open(csv_filename, 'w', newline='') as o:
        writer = csv.writer(o)
        writer.writerows(out)

if __name__ == "__main__":
    write_inventory_to_csv(sh_version_files, 'task_17_2.csv')
