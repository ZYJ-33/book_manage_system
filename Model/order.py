from Model import model
from tool import get_date, date_2_str


class pending_Orders(model):
    def __init__(self, kwargs):
        self.user_id = kwargs["user_id"]
        self.book_id = kwargs["book_id"]
        self.start_date, self.end_date = get_date(kwargs["howlong"])

    @classmethod
    def check_for_due_order(cls):
        sql = '''
            SELECT user_id
            FROM begin_orders o 
            WHERE now() > end_date 
        '''
        conn,cursor = cls.get_cursor()
        cursor.execute(sql)
        conn.commit()
        res = cursor.fetchall()
        for r in res:
            id = r["user_id"]
            sql = '''
                UPDATE users
                SET status="due"
                WHERE id = %s
            '''
            cursor.execute(sql, id)


    @classmethod
    def how_many_startorder_from(cls, id):
        sql = '''
            SELECT count(*)
            FROM begin_orders
            WHERE user_id = %s AND now() > end_date
        '''
        conn,cursor = cls.get_cursor()
        cursor.execute(sql, id)
        duenum =  cursor.fetchall()[0]["count(*)"]
        sql = '''
                    SELECT count(*)
                    FROM begin_orders
                    WHERE user_id = %s 
                '''
        cursor.execute(sql, id)
        totalnum = cursor.fetchall()[0]["count(*)"]
        return duenum, totalnum

    @classmethod
    def all_order(cls):
        sql = '''
            SELECT o.id, u.username, u.credit, u.status, b.bookname, b.remain, o.start_date, o.end_date 
            FROM  pending_orders o, users u, book b
            WHERE o.user_id = u.id and o.book_id = b.id
        '''
        conn, cursor = cls.get_cursor()
        cursor.execute(sql)
        conn.commit()
        res =  cursor.fetchall()
        return date_2_str(res)


    # @classmethod
    # def apply_to_return_book(cls, id):
    #     sql = '''
    #         insert into return_book
    #         select *
    #         from begin_orders
    #         where id = %s
    #     '''
    #     conn, cursor = cls.get_cursor()
    #     cursor.execute(sql, id)
    #     conn.commit()
    #     sql = '''
    #         DELETE
    #         FROM begin_orders
    #         WHERE id = %s
    #     '''
    #     conn, cursor = cls.get_cursor()
    #     cursor.execute(sql, id)
    #     conn.commit()

    @classmethod
    def orders_record_of(cls, order_type, id):
        print("in record of", id)
        sql = '''
            SELECT o.id, o.start_date, o.end_date, o.status, b.bookname
            FROM {} o, book b
            WHERE o.user_id = %s AND o.book_id = b.id
        '''.format(order_type)
        conn, cursor = cls.get_cursor()
        cursor.execute(sql, id)
        return date_2_str(cursor.fetchall())

    @classmethod
    def pending_order_record_of(cls, id):
        return cls.orders_record_of("pending_orders", id)

    @classmethod
    def begin_order_record_of(cls, id):
        return cls.orders_record_of("begin_orders", id)

    @classmethod
    def end_order_record_of(cls, id):
        return cls.orders_record_of("end_orders", id)

    @classmethod
    def update_pending_order(cls, id, status):
        sql = '''
                   UPDATE pending_orders
                   SET status= %s
                   WHERE id = %s
               '''
        conn, cursor = cls.get_cursor()

        cursor.execute(sql, [status, id])
        conn.commit()
        sql = '''
                   DELETE
                   FROM pending_orders
                   WHERE id = %s
               '''
        cursor.execute(sql, id)
        conn.commit()
        return

    @classmethod
    def get_remain(cls, id):
        sql = '''
            SELECT remain
            FROM book b, pending_orders o 
            WHERE o.id = %s and o.book_id = b.id
        '''
        conn, cursor = cls.get_cursor()
        cursor.execute(sql, id)
        return cursor.fetchall()[0]["remain"]

    @classmethod
    def get_all_return_book_apply(cls):
        sql = '''
            SELECT o.id, o.user_id, o.book_id, u.username,b.bookname, o.start_date, o.end_date
            FROM  begin_orders o, users u, book b
            WHERE o.user_id = u.id and o.book_id = b.id
        '''
        conn, cursor = cls.get_cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        return date_2_str(res)

    @classmethod
    def return_book_done(cls, id):
        sql1 = '''
             
            UPDATE begin_orders
            SET status = "finished"
            WHERE id = %s
          '''
        sql2 = '''
            INSERT INTO end_orders
            SELECT *
            FROM begin_orders
            WHERE id = %s
        '''
        sql3 = '''
            DELETE 
            FROM begin_orders
            WHERE id = %s
        '''

        conn, cursor = cls.get_cursor()
        for sql in [sql1, sql2, sql3]:
            cursor.execute(sql, [id])
            conn.commit()


    @classmethod
    def allow_continue(cls, id):
        if cls.get_remain(id) > 0:
            cls.update_pending_order(id, "start")
        else:
            cls.deny_continue(id)

    @classmethod
    def deny_continue(cls, id):
        cls.update_pending_order(id, "deny")

    @classmethod
    def current_book_num_of(cls, id):
        sql1 = '''
            SELECT COUNT(*)
            FROM begin_orders
            WHERE user_id = %s 
        '''
        sql2 = '''
            SELECT COUNT(*)
            FROM pending_orders
            WHERE user_id = %s
        '''
        conn, cursor = cls.get_cursor()
        cursor.execute(sql1, id)
        t1 = cursor.fetchall()[0]["COUNT(*)"]
        cursor.execute(sql2, id)
        t2 = cursor.fetchall()[0]['COUNT(*)']
        return t1+t2

if __name__ == "__main__":
    print(pending_Orders.orders_record_of("end_orders", 13))