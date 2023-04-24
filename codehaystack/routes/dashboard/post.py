import os
from flask import (Blueprint, current_app, render_template,
                   redirect, url_for, flash)
from slugify import slugify
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required

from ...models.post import Post
from ...models.term import Term, terms
from ...forms import PostArticleForm
from ...extensions import db
from ...functions import allowed_image, unique_filename

post = Blueprint("post", __name__, url_prefix="/dashboard")

# set `post_type`
post_type = 'post'


@post.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    # new instance of post form
    post_form = PostArticleForm()

    # populate form `categories` and `tags` with data from the `Term` model
    # values would be set to `term` `id`
    post_form.categories.choices = [
        (term.id, term.name) for term in Term.get_terms_by_taxonomy("Category")
    ]
    post_form.tags.choices = [
        (term.id, term.name) for term in Term.get_terms_by_taxonomy("Tag")
    ]

    # form validation and processing
    if post_form.validate_on_submit():

        # get data from form fields
        title = post_form.title.data
        slug = slugify(post_form.slug.data)
        featured_image = post_form.featured_image.data
        featured_filename = secure_filename(featured_image.filename) or None

        # check or set slug if none is submitted
        if not slug:
            slug = slugify(title)

        # check if slug is unique
        if Post.query.filter_by(slug=slug).first():
            flash("Slug already exists", "danger")

        # check if uploaded `featured_image` is valid
        elif not allowed_image(featured_filename):
            flash("Featured image can only be jpg, png, gif, or webp formats!")

        # process the data
        else:
            # retrieve the selected categories and terms
            category_ids = post_form.categories.data
            tag_ids = post_form.tags.data

            # retrieve the corresponding `Term` objects from the database
            categories = Term.query.filter(Term.id.in_(category_ids)).all()
            tags = Term.query.filter(Term.id.in_(tag_ids)).all()

            # if `featured_image` is uploaded, make filename unique
            if featured_filename:
                unique_featured_filename = unique_filename(featured_filename)

            # set featured_image filepath
            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"], unique_featured_filename)

            # upload and save the image with defined `filepath`
            featured_image.save(filepath)

            # create a new `Post` instance
            # with the selected categories and tags added to its `terms` list
            new_post = Post(
                title=title,
                slug=slug,
                description=post_form.description.data,
                content=post_form.content.data,
                featured_image_path=unique_featured_filename,
                status=post_form.status.data,
                post_type=post_type,
                user_id=current_user.id,
                terms=categories + tags
            )

            # add the Post instance to database
            db.session.add(new_post)
            db.session.commit()

            flash("Post saved!", "success")

            return redirect(url_for('post.create_post'))
    else:
        # validation not passed
        for field, errors in post_form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "error")

    return render_template("/dashboard/create_post.html", form=post_form)
