# -*- coding: utf-8 -*-
"""
Задание 17.4

Создать функцию write_last_log_to_csv.

Аргументы функции:
* source_log - имя файла в формате csv, из которого читаются данные (пример mail_log.csv)
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Функция write_last_log_to_csv обрабатывает csv файл mail_log.csv.
В файле mail_log.csv находятся логи изменения имени пользователя. При этом, email
пользователь менять не может, только имя.

Функция write_last_log_to_csv должна отбирать из файла mail_log.csv только
самые свежие записи для каждого пользователя и записывать их в другой csv файл.

Для части пользователей запись только одна и тогда в итоговый файл надо записать только ее.
Для некоторых пользователей есть несколько записей с разными именами.
Например пользователь с email c3po@gmail.com несколько раз менял имя:
C=3PO,c3po@gmail.com,16/12/2019 17:10
C3PO,c3po@gmail.com,16/12/2019 17:15
C-3PO,c3po@gmail.com,16/12/2019 17:24

Из этих трех записей, в итоговый файл должна быть записана только одна - самая свежая:
C-3PO,c3po@gmail.com,16/12/2019 17:24

Для сравнения дат удобно использовать объекты datetime из модуля datetime.
Чтобы упростить работу с датами, создана функция convert_datetimestr_to_datetime - она
конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
Полученные объекты datetime можно сравнивать между собой.

Функцию convert_datetimestr_to_datetime использовать не обязательно.

"""
import csv
import datetime


def convert_datetimestr_to_datetime(datetime_str):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")

def write_last_log_to_csv(old_csv_file, clear_csv_file):
    """
    Put only fresh logs from one csv file to the other
    :param old_csv_file: Old csv file to analize
    :param clear_csv_file: Celar cvs file to write
    :return: None
    """
    clear_mail_log = []
    with open(old_csv_file) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            clear_mail_log.append(row)
        for line in clear_mail_log:
            mail = line[1]
            date = convert_datetimestr_to_datetime(line[2])
            for line in clear_mail_log:
                if mail == line[1] and date > convert_datetimestr_to_datetime(line[2]):
                    line_index = clear_mail_log.index(line)
                    clear_mail_log.pop(line_index)
    clear_mail_log.insert(0, header)
    with open(clear_csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in clear_mail_log:
            writer.writerow(row)

if __name__ == "__main__":
    write_last_log_to_csv('mail_log.csv', 'clear.mail_log.csv')