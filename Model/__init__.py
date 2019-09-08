import pymysql
from config import sqlpass
import time

def log(*args, **kwargs):
    print(time.strftime("%Y-%m-%d  %H:%M:%S --- ", time.localtime(time.time())), args, kwargs)


class model(object):
    @classmethod
    def tablename(cls):
        return cls.__name__.lower()

    @classmethod
    def get_cursor(cls):
        conn = pymysql.connect("localhost", "root", sqlpass, "book_manage",cursorclass = pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        return conn, cursor

    def save(self):
        conn, cursor = model.get_cursor()
        sql = self.get_insert_sql()
        para = []
        for v in self.__dict__.values():
            para.append(v)
        cursor.execute(sql, para)
        conn.commit()
        conn.close()

    @classmethod
    def get_all(cls):
        conn, cursor = cls.get_cursor()
        sql = '''
            SELECT * 
            FROM {}
        '''.format(cls.tablename())
        cursor.execute(sql)
        res = cursor.fetchall()
        return res


    def get_insert_sql(self):
        i = 0
        tablename = self.tablename()
        sql = '''INSERT 
    INTO {}('''.format(tablename)
        value_sql = 'VALUE('
        for k in self.__dict__.keys():
            sql += k
            value_sql += '%s'
            if i == self.__dict__.__len__() - 1:
                break;
            i = i + 1
            sql += ','
            value_sql += ','
        sql += ')'
        value_sql += ')'
        return sql + "\n" + value_sql