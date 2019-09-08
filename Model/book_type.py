from Model import model
from jd_spider import book_info_iterator
from Model.book import Book
from tool import date_2_str
class book_Type(model):
    def __init__(self, typename):
        self.type = typename

    @classmethod
    def del_type_by_id(cls, id):
        sql = '''
            DELETE
            FROM book
            WHERE type_id = %s
        '''
        conn,cursor = cls.get_cursor()
        cursor.execute(sql, id)
        conn.commit()
        sql = '''
            DELETE
            FROM book_type
            WHERE id = %s
        '''
        cursor.execute(sql, id)
        conn.commit()
        return

    def get_self_id(self):
        sql = '''
             SELECT id
             FROM book_type
             WHERE type = %s
         '''
        conn, cursor = self.get_cursor()
        cursor.execute(sql, self.type)
        return cursor.fetchall()[0]["id"]

    def add_book(self, type_id):
        iterator = book_info_iterator(self.type)
        for info in iterator:
            info.append(type_id)
            b = Book(info)
            try:
                b.save()
            except Exception:
                continue

    def add_type_and_add_books(self):
        self.save()
        type_id = self.get_self_id()
        start_new_thread(self.add_book, (type_id, ))

    @classmethod
    def get_books_of(cls, type):
        sql = '''
            SELECT b.id, b.bookname, b.introduce, b.remain, b.total, b.ISBN, b.author, b.publisher,b.version,b.public_time, t.type
            FROM book b, book_type t
            WHERE t.type = %s AND b.type_id = t.id
        '''
        conn, cursor = cls.get_cursor()
        cursor.execute(sql, type)
        return date_2_str(cursor.fetchall())

if __name__ == "__main__":
    iterator = book_info_iterator("python")
    for info in iterator:
        print(info)
