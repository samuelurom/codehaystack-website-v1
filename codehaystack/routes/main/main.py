from flask import Blueprint, render_template

from ...models.post import Post

main = Blueprint("main", __name__)


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route("/<slug>")
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template("main/single_post.html", post=post)
