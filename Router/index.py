from flask import (
    Blueprint,
    render_template,
    session,
)
blueprint = Blueprint("index", __name__)


@blueprint.route("/")
def index():
    u = session.get("username", None)
    return render_template("index/index.html", User=u)