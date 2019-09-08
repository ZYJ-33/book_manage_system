from flask import (
    session,
    Blueprint,
    redirect,
    request,
    render_template,
    url_for,
)
from tool import log
from Model.order import pending_Orders
from Router.user import require_login, require_login_url
from Model.book import Book
from tool import jsonlify
blueprint = Blueprint("order", __name__)


@blueprint.route("get_comfirm", methods=["GET", "POST"])
@require_login_url
def get_comfirm():
    if request.method == "POST":
        book_name = request.json["book_name"]
        book_id = request.json["book_id"]
        return url_for("order.get_comfirm", book_name=book_name, book_id=book_id)
    else:
        book_name = request.args["book_name"]
        book_id = request.args["book_id"]
        return render_template("order/confirm_page.html", book_name=book_name, id=book_id)



@blueprint.route("new_order", methods=["POST"])
@require_login
def new_order():
    user_id = session["id"]
    book_id = request.json["book_id"]
    howlong = int(request.json["howlong"])
    if pending_Orders.current_book_num_of(user_id) > 3:
        return url_for("index.index")
    if Book.left_of_the(book_id) <= 0:
        return url_for("book.get_books_template")
    if howlong <= 7 and howlong > 0:
        data = dict(
            user_id = user_id,
            book_id = book_id,
            howlong = howlong,
        )
        o = pending_Orders(data)
        o.save()
    return url_for("book.get_books_template")


@blueprint.route("pending_order_record_page")
@require_login
def get_pending_order_record_page():
    return render_template("order/pending_order_record.html")


@blueprint.route("begin_order_record_page")
@require_login
def get_begin_order_record_page():
    return render_template("order/begin_order_record.html")


@blueprint.route("end_order_record_page")
@require_login
def get_end_order_record_page():
    return render_template("order/cancel_order_record.html")


@blueprint.route("all_pending_orders", methods=["POST"])
@require_login
def all_pending_orders():
    res = pending_Orders.pending_order_record_of(session.get("id"))
    return jsonlify(res)

@blueprint.route("cancel_pending_order", methods=["POST"])
@require_login
def cancel_pending_order():
    id = request.json["id"]
    pending_Orders.deny_continue(id)
    return url_for("order.get_pending_order_record_page")

@blueprint.route("begin_orders", methods=["POST"])
@require_login
def all_begin_orders():
    res = pending_Orders.begin_order_record_of(session.get("id"))
    return jsonlify(res)


@blueprint.route("end_orders", methods=["POST"])
@require_login
def all_end_orders():
    res = pending_Orders.end_order_record_of(session.get("id"))
    return jsonlify(res)



# @blueprint.route("apply_return_book", methods=["POST"])
# @require_login
# def apply_to_return_book():
#     id = request.json["id"]
#     log(id)
#     pending_Orders.apply_to_return_book(id)
#     return id