from Model import model
from random import randint
from tool import date_2_str
'''[publisher, isbn, version, public_time, author, title, detail]'''
class Book(model):
    def __init__(self, args):
        self.publisher = args[0]
        self.ISBN = args[1]
        self.version = args[2]
        self.public_time = args[3]
        self.author = args[4]
        self.bookname = args[5]
        self.introduce = args[6]
        self.type_id = args[7]
        if len(args) > 8:
            self.remain = args[8]
        else:
            self.remain = randint(1, 5)
        self.total = self.remain


    # @classmethod
    # def get_book_by_booktype(cls, booktype):
    #     sql = '''
    #         SELECT id
    #         FROM book_type
    #         WHERE type = %s
    #     '''
    #     conn, cursor = cls.get_cursor()
    #     cursor.execute(sql, booktype)
    #     id = cursor.fetchall()[0]["id"]
    #     sql = '''
    #         SELECT *
    #     '''

    @classmethod
    def left_of_the(cls, id):
        sql = '''
            SELECT remain
            FROM book
            WHERE id = %s
        '''
        conn, cursor = cls.get_cursor()
        cursor.execute(sql, id)
        conn.commit()
        return cursor.fetchall()[0]["remain"]

    @classmethod
    def add_book_remain(cls, id):
        sql = '''
            UPDATE book
            SET remain = remain + 1
            WHERE id=%s
        '''
        conn, cursor = cls.get_cursor()
        cursor.execute(sql, id)
        conn.commit()

    @classmethod
    def get_all_book(cls):
        conn, cursor = cls.get_cursor()
        sql = '''
                    SELECT b.id, b.bookname, b.introduce, b.remain, b.total, b.ISBN, b.author, b.publisher,b.version,b.public_time, t.type
                    FROM book b, book_type t
                    WHERE b.type_id = t.id
                '''
        cursor.execute(sql)
        res = cursor.fetchall()
        return date_2_str(res)

    @classmethod
    def del_book(cls, id):
        sql = '''
            DELETE
            FROM {}
            WHERE id = %s
        '''.format(cls.tablename())
        conn, cursor = cls.get_cursor()
        try:
            cursor.execute(sql, id)
            conn.commit()
        except Exception as e:
            return False
        return True

if __name__ == "__main__":
    print(Book.left_of_the(6))