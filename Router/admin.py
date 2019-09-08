from functools import wraps
from flask import (
    session,
    Blueprint,
    redirect,
    request,
    render_template,
    url_for,
)
from Model.book import Book
from Model.order import pending_Orders
from Model.user import Users
from Model.reserve_book import reserve_Book
from Model.book_type import book_Type
from tool import log,jsonlify,str2date,get_current_date
from _thread import start_new_thread

blueprint = Blueprint("admin", __name__)

def require_admin(fn):
    @wraps(fn)
    def f(*args, **kwargs):
        res = session.get("level", None)
        if res == 1:
            return fn(*args, **kwargs)
        else:
            return redirect(url_for("index.index"))
    return f

def check_addbook(data):
    if data is None:
        return False
    keys = ["bookname", "remain", "introduce"]
    for key in keys:
        if data.get(key, None) is None:
            return False
        return True

@blueprint.route("/")
def index():
    return render_template("admin/index.html")

@blueprint.route("add_book", methods=["GET", "POST"])
@require_admin
def add_book():
    if request.method == "GET":
        return render_template("admin/add_book.html")
    else:
        data = request.json
        b = Book(data)
        b.save()
        return "ok"

@blueprint.route("pending_order_page", methods=["GET"])
@require_admin
def get_admin_pending_order_page():
    return render_template("admin/pending_order_page.html")


@blueprint.route("all_pending_orders", methods=["POST"])
@require_admin
def get_all_pending_orders():
    data = pending_Orders.all_order()
    return jsonlify(data)


@blueprint.route("deal_with_pending", methods=["POST"])
@require_admin
def deal_with_pending():
    switch = {
        "agree": pending_Orders.allow_continue,
        "deny": pending_Orders.deny_continue,
    }
    action, id = request.json["action"], request.json["id"]
    switch[action](id)
    return url_for("admin.get_admin_pending_order_page")


@blueprint.route("delete_book", methods=["GET", "POST"])
@require_admin
def del_book():
    if request.method == "GET":
        return render_template("admin/delete_book.html")
    else:
        book_id = request.json
        if Book.del_book(book_id):
            return "ok"
        else:
            return "notok"


@blueprint.route("all_return_book_apply_page", methods=["GET"])
def get_return_book_page():
    return render_template("admin/all_return_book_apply_page.html")


@blueprint.route("all_return_book_apply", methods=["POST"])
@require_admin
def get_all_return_book_apply():
    res = pending_Orders.get_all_return_book_apply()
    return jsonlify(res)


'''
    id:target.dataset.id,
    user_id:target.dataset.userid,
    book_id:target.dataset.bookid,
    start_date:target.dataset.startdate,
    end_date:target.dataset.enddate,
'''


@blueprint.route("confirm_return", methods=["POST"])
@require_admin
def after_confirm_return_apply():
    data = request.json
    start_new_thread(reserve_Book.have_stock_now,(data["book_id"], ))
    Book.add_book_remain(data["book_id"])
    if get_current_date() > str2date(data["end_date"]):
        Users.add_credit(data["user_id"], -1)
    else:
        Users.add_credit(data["user_id"], 1)
    pending_Orders.return_book_done(data["id"])
    Users.change_user_status(data["user_id"])
    return data["id"]


@blueprint.route("add_type_page", methods=["GET"])
@require_admin
def add_type_page():
    return render_template("admin/add_type_page.html")


@blueprint.route("add_type", methods=["POST"])
@require_admin
def add_type():
    type = request.json["type"]
    log(type)
    t = book_Type(type)
    t.add_type_and_add_books()
    return url_for("admin.add_type_page")

@blueprint.route("del_type", methods=["POST"])
@require_admin
def del_type():
    id = request.json["id"]
    book_Type.del_type_by_id(id)
    return url_for("admin.add_type_page")




