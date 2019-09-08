from send_email_part import send_email
import Model
class reserve_Book(Model.model):
    def __init__(self, userid, bookid):
        self.user_id = userid
        self.book_id = bookid

    @classmethod
    def have_stock_now(cls, bookid):
        sql = '''
            SELECT r.id, r.email, b.bookname
            FROM reserve_book r, book b
            WHERE book_id = %s and r.book_id = b.id
            ORDER BY r.id
            LIMIT 1
        '''
        conn, cursor = cls.get_cursor()
        cursor.execute(sql, bookid)
        res = cursor.fetchall()
        if len(res) > 0:
            id, email, bookname = res[0]["id"], res[0]["email"], res[0]["bookname"]
            if id is not None:
                sql = '''
                    DELETE 
                    FROM reserve_book
                    WHERE id = %s
                '''
                cursor.execute(sql, id)
                conn.commit()
                send_email(email, bookname)


if __name__ == "__main__":
    reserve_Book.have_stock_now(6)
