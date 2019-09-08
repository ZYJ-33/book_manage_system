from Model import model
from Model.order import pending_Orders
class Users(model):
    def __init__(self, kwargs):
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.email = kwargs.get("email")
        self.credit = kwargs.get("credit", None)
        self.level = kwargs.get("level", 0)
        self.status = kwargs.get("status", None)

    @classmethod
    def update_user_status(cls, id, new):
        sql = '''
            UPDATE users
            set status = %s
            WHERE id = %s
        '''
        conn, cursor = cls.get_cursor()
        cursor.execute(sql, [new, id])
        conn.commit()

    @classmethod
    def change_user_status(cls, id):
        duenum, totalnum = pending_Orders.how_many_startorder_from(id)
        if totalnum == 0:
            cls.update_user_status(id, "nobook")
        elif duenum == 0:
            cls.update_user_status(id, "booked")
        else:
            cls.update_user_status(id, "due")


    def register(self):
        if self.credit == None:
            self.credit = 5
        if self.status is None:
            self.status = "nobook"
        self.save()

    @classmethod
    def login(cls, username, password):
        res = cls.get_user_by_username(username)
        if len(res) == 0:
            return None
        else:
            if res[0]["password"] == password:
                return res[0]
            else:
                return None

    @classmethod
    def add_credit(cls, uid, amount):
        sql = '''
                UPDATE users
                SET credit = credit + %s
                WHERE id = %s
        '''
        conn,cursor = cls.get_cursor()
        cursor.execute(sql, [amount, uid])
        conn.commit()

    @classmethod
    def get_user_by_username(cls, username):
        conn, cursor = cls.get_cursor()
        sql = '''
            SELECT *
            FROM {}
            WHERE username = %s
        '''.format(cls.tablename())
        cursor.execute(sql, username)
        res = cursor.fetchall()
        return res


'''
self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.email = kwargs.get("email")
        self.credit = kwargs.get("credit", None)
        self.level = kwargs.get("level", 0)
        self.status = kwargs.get("status", None)
'''

if __name__ == "__main__":
    t = dict(username="zyj", password="123", email="jobsera@163.com",level=1)
    u = Users(t)
    u.save()
    print(u.login("zyj", "123"))
