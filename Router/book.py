from flask import (
    Blueprint,
    request,
    session,
    render_template,
    redirect,
    url_for,
)
from Model.book import Book
from Model.book_type import book_Type
from tool import jsonlify, log


blueprint = Blueprint("book", __name__)


@blueprint.route("books")
def get_books_template():
    return render_template("book/books2.html")


@blueprint.route("all_book")
def get_all_book():
    return jsonlify(Book.get_all_book())


@blueprint.route("book_type_of", methods=["POST"])
def get_books_by_type():
    type = request.json["type"]
    res = book_Type.get_books_of(type)
    return jsonlify(res)

@blueprint.route("all_book_type", methods=["GET"])
def get_all_book_type():
    res = book_Type.get_all()
    return jsonlify(res)





if __name__ == "__main__":
    print(get_all_book())