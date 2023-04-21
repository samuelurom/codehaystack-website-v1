from flask import Blueprint, render_template, flash
from slugify import slugify

from ..forms import PostArticleForm
from ..models.post import Post

create_post = Blueprint("create_post", __name__, url_prefix="/dashboard")


@create_post.route("/new-post")
def new_post():
    # new instance of post form
    post_form = PostArticleForm()

    # form validation and processing
    if post_form.validate_on_submit():
        # get data from form fields
        title = post_form.title.data
        url = post_form.url.data

        # check or set url slug if none is submitted
        if url:
            slugify(url)
        else:
            url = slugify(title)

        if Post.query.filter_by(url=url).first():
            flash("URL slug already exists", "danger")
        else:
            post_details = Post(
                title=title,
                url=url,
                description=post_form.description.data,
                content=post_form.content.data,
                featured_image_url=post_form.featured_image.data,
                status=post_form.status.data
            )

            flash("Post saved!", "success")

    return render_template("/dashboard/create_post.html", form=post_form)
