from flask import (
    Blueprint,
    request,
    session,
    render_template,
    redirect,
    url_for,
)
from functools import wraps
from tool import log
from Model.user import Users
blueprint = Blueprint("user", __name__)

def require_login(fn):
    @wraps(fn)
    def f(*args, **kwargs):
        if session.get("username", None) is None:
            return redirect(url_for("user.get_login"))
        else:
            return fn(*args, **kwargs)
    return f


def require_login_url(fn):
    @wraps(fn)
    def f(*args, **kwargs):
        if session.get("username", None) is None:
            return url_for("user.get_login")
        else:
            return fn(*args, **kwargs)
    return f


def check_register_data(data):
    keys = ["username", "password", "email"]
    for key in keys:
        if data.get(key, None) is None:
            return False
    return True



@blueprint.route("/login", methods=["POST"])
def login():
    if session.get("username", None) is not None:
        return url_for("index.index")
    data = request.json
    username = data.get("username", None)
    password = data.get("password", None)
    if username and password:
        res = Users.login(username, password)
        log("before update", res)
        if res is not None:
            session.update(res)
        else:
            return url_for("index.index")
        log("login ok", session)
    return url_for("index.index")


@blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index.index"))

@blueprint.route("/get_login")
def get_login():
    return render_template("users/login.html")


@blueprint.route("/get_register")
def get_register():
    return render_template("users/register.html")


@blueprint.route("/register", methods=["POST"])
def register():
    data = request.json
    log("in register", data)
    if check_register_data(data):
        try:
            u = Users(data)
            u.register()
        except Exception as e:
            log("exceptino")
            return url_for("user.get_register")
        else:
            return url_for("user.get_login")
    else:
        return url_for("user.get_register")



