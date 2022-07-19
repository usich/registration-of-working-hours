import win32com.client
import time
import main
import sqlite3
import FDataBase
import json


def get_usb_device():
    '''Получает список usb устройств '''
    try:
        usb_list = []
        wmi = win32com.client.GetObject("winmgmts:")
        for usb in wmi.InstancesOf("Win32_USBHub"):
            usb_list.append(usb.DeviceID.split('\\')[-1])
        return usb_list
    except Exception as error:
        print('error', error)


def detect_device():
    original = set(get_usb_device())
    time.sleep(1)
    add_device = set(get_usb_device()) - original
    subt_device = original - set(get_usb_device())
    if len(add_device):
        for drive in add_device:
            print("The drives added: %s." % (drive))
            device_add_rem('add', drive)

    elif len(subt_device):
        for drive in subt_device:
            print("The drives remove: %s." % (drive))
            device_add_rem('remove', drive)


def device_add_rem(action, id):
    db = main.connect_db()
    db.row_factory = sqlite3.Row
    dbase = FDataBase.FDataBase(db)
    with open('usersFlashCard.json', 'r') as f:
        data = json.load(f)
    # wmi = win32com.client.GetObject("winmgmts:")
    if data.get(id) is not None:
        try:
            if action == 'add':
                dbase.add_record(data[id], id)
                print(f'Подключили:  {dbase.search_record_incomplete(data[id])}')
            elif action == 'remove' and dbase.get_relevant_record(data[id]):
                dbase.edit_record(data[id], id)
                print(f'Отключили:  {dbase.search_record_incomplete(data[id])}')
                # uploadOut.upload_out()
        except Exception as e:
            print('Ошибка записи в БД# ', e)
