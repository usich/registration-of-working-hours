import sqlite3
import event_USB
import schedule
import uploadOut
import FDataBase
import os
import json
import configparser


config = configparser.ConfigParser()
config.read('config.ini')


def connect_db():
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        return conn


def create_db():
    db = connect_db()
    with open('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def alert_end_day():
    ''' Функция запускается ночью и показывает системное уведомление, если подключены USB устройства.
        Нужно для того, что если сотрудники до полуночи на работе, переподключали свою флешку, для создание записи
        в новом дне'''
    db = connect_db()
    dbase = FDataBase.FDataBase(db)
    if not dbase.no_end_record():
        os.system('msg "%username%" Если вы еще на работе, извлеките свою флешку и подключите ее снова после полуночи')


def detect_device_first_run():
    '''Выводит системное сообщение при запуске скрипта, если устройство из списка userFlashCard.json было подключено
    до запуска скрипта'''
    db = connect_db()
    dbase = FDataBase.FDataBase(db)
    list_device = event_USB.get_usb_device()
    with open('usersFlashCard.json', 'r') as f:
        data = json.load(f)
    for key, value in data.items():
        res = dbase.get_relevant_record(value)
        if key in list_device and not res:
            os.system(f'msg "%username%" Переподключите флешку пользователя: {int(value)}')


def main():
    detect_device_first_run()
    schedule.every().day.at(config['TIMESHEDULE']['upload_xml_out']).do(uploadOut.upload_xml_out)
    schedule.every().day.at(config['TIMESHEDULE']['alert_end_day']).do(alert_end_day)
    while True:
        event_USB.detect_device()
        schedule.run_pending()
        # time.sleep(1)


if __name__ == '__main__':
    main()
