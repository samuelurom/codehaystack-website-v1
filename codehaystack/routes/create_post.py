from flask import Blueprint, render_template

from ..forms import PostArticle

create_post = Blueprint("create_post", __name__, url_prefix="/dashboard")


@create_post.route("/new_post")
def new_post():
    form = PostArticle()

    return render_template("/dashboard/create_post.html", form=form)
