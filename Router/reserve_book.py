from flask import (
    session,
    Blueprint,
    redirect,
    request,
    render_template,
    url_for,
)
from Model.reserve_book import reserve_Book
from Router.user import require_login_url

blueprint = Blueprint("reserve_book", __name__)

@blueprint.route("add_reserve", methods=["POST"])
@require_login_url
def add_reserve():
    book_id = request.json["book_id"]
    user_id = session["id"]
    o = reserve_Book(user_id, book_id)
    try:
        o.save()
    except Exception:
        return url_for("index.index")
    return url_for("book.get_books_template")


