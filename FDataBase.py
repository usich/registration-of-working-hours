import math
import sqlite3
import time
import main


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
        loc_time = time.localtime()
        struct_time_yesterday = (loc_time.tm_year, loc_time.tm_mon, loc_time.tm_mday - 1, 0, 0, 0, 0, 0, 0)
        self.day_begin = time.mktime(time.struct_time(struct_time_yesterday))
        self.day_end = self.day_begin + 86399
        main.create_db()

    def add_record(self, user_code, device_code):
        tm = math.floor(time.time())
        # print(f'ADD time:  {time.gmtime(tm).tm_mday}')
        sql = "INSERT INTO registration_of_employees VALUES(NULL, ?,?,?,?, 0)"
        try:
            self.__cur.execute(sql, (user_code, device_code, tm, 0))
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Ошибка записи в БД {e}')
            return False
        return True

    def edit_record(self, user_code, device_code):
        tm = math.floor(time.time())
        # print(f'END time:  {time.gmtime(tm).tm_mday}')
        sql = f"UPDATE registration_of_employees SET timeOut = {tm} WHERE userCode = '{user_code}' and " \
              f"id = (SELECT id FROM registration_of_employees WHERE userCode = '{user_code}' and timeOut = 0 " \
              f"ORDER BY timeIn DESC LIMIT 1)"
        print(user_code)
        try:
            self.__cur.execute(sql)
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Ошибка записи в БД {e}')
            return False
        return True

    def search_record_incomplete(self, user_code):
        sql = f"SELECT count(id) as count FROM registration_of_employees WHERE userCode = '{user_code}' and " \
              f"timeIn != 0 and timeOut = 0"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res['count'] > 0:
                return False
            return True
        except sqlite3.Error as e:
            print(f'Ошибка записи в БД {e}')
            return False

    def get_record_not_unloaded(self):
        sql = f'SELECT * FROM registration_of_employees WHERE unloaded = 0 and timeIn >= {self.day_begin} ' \
              f'and timeIn < {self.day_end}'
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print(f'Ошибка записи в БД {e}')
            return False

    def enable_unloaded_check(self):
        sql = f"UPDATE registration_of_employees SET unloaded = 1 WHERE " \
              f"id IN (SELECT id FROM registration_of_employees WHERE unloaded = 0 and timeIn >= {self.day_begin} " \
              f"and timeIn < {self.day_end})"
        try:
            self.__cur.execute(sql)
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Ошибка записи в БД {e}')
            return False
        return True

    def no_end_record(self):
        sql = f'SELECT COUNT() as count FROM registration_of_employees ' \
              f'WHERE timeIn > {self.day_begin+86400} and timeOut = 0'
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res['count'] == 0:
                return True
            return False
        except sqlite3.Error as e:
            print(f'Ошибка чтения из БД {e}')
            return False

    def get_relevant_record(self, user_code):
        sql = f'SELECT id FROM registration_of_employees WHERE userCode = "{user_code}" and timeOut = 0 and ' \
              f'timeIn > {self.day_end + 2} ORDER BY timeIn DESC LIMIT 1'
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if len(res) > 0:
                return True
            return False
        except sqlite3.Error as e:
            print(f'Ошибка чтения из БД {e}')
            return False
