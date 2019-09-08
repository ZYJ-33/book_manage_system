from flask import Flask
from tool import check_due_thread
import _thread
from Router import (
    user_blueprint,
    index_blueprint,
    admin_blueprint,
    book_blueprint,
    order_blueprint,
    reserve_book_blueprint,
)

app = Flask(__name__)
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(book_blueprint, url_prefix="/book")
app.register_blueprint(order_blueprint, url_prefix="/order")
app.register_blueprint(reserve_book_blueprint, url_prefix="/reserve")
app.register_blueprint(index_blueprint)
app.secret_key = "zhengyujia"


if __name__ == "__main__":
    config = dict(
        host='127.0.0.1',
        port=3333,
        debug=True,
    )
    _thread.start_new_thread(check_due_thread, ())
    app.run(**config)
