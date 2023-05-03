import os
from flask import Blueprint, current_app, render_template, redirect, url_for, flash
from slugify import slugify
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required

from ..models.post import Post
from ..models.term import Term, terms
from ..forms import PostArticleForm
from ..extensions import db
from ..functions import allowed_image, unique_filename

post = Blueprint("post", __name__, url_prefix="/dashboard/posts")


@post.route("/")
@login_required
def posts():
    """Route to show all posts in database"""

    # get all the posts
    posts = Post.query.all()

    return render_template("/dashboard/posts.html", posts=posts)


@post.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    """Route to create a new post"""

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

        # check or set slug if none is submitted
        if not slug:
            slug = slugify(title)

        # check if slug is unique
        if Post.query.filter_by(slug=slug).first():
            flash("Slug already exists", "danger")

        # check if uploaded `featured_image` is valid
        elif featured_image and not allowed_image(featured_image.filename):
            flash("Featured image can only be jpg, png, gif, or webp formats!")

        # manual validations passed, process the data

        # retrieve the selected categories and terms
        category_ids = post_form.categories.data
        tag_ids = post_form.tags.data

        # retrieve the corresponding `Term` objects from the database
        categories = Term.query.filter(Term.id.in_(category_ids)).all()
        tags = Term.query.filter(Term.id.in_(tag_ids)).all()

        # if `featured_image` is uploaded, make filename unique
        if featured_image:
            # set secure filename
            featured_filename = secure_filename(featured_image.filename)

            # set unique filename
            unique_featured_filename = unique_filename(featured_filename)

            # set featured_image filepath
            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"], unique_featured_filename
            )

            # upload and save the image with defined `filepath`
            featured_image.save(filepath)
        else:
            unique_featured_filename = None

        # create a new `Post` instance
        # with the selected categories and tags added to its `terms` list
        new_post = Post(
            title=title,
            slug=slug,
            description=post_form.description.data,
            content=post_form.content.data,
            featured_image_path=unique_featured_filename,
            status=post_form.status.data,
            post_type="post",
            user_id=current_user.id,
            terms=categories + tags,
        )

        # add the Post instance to database
        db.session.add(new_post)
        db.session.commit()

        flash("Post saved!", "success")

        return redirect(url_for("post.posts"))
    else:
        # validation not passed
        for field, errors in post_form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "error")

    return render_template("/dashboard/create_post.html", form=post_form)


@post.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    """Route to edit an existing post"""

    # get the post by `id`
    post = Post.query.filter_by(id=id).first()

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

        # set featured_filename if new featured image is not uploaded
        if featured_image:
            # check if uploaded `featured_image` is valid
            if not allowed_image(featured_filename):
                flash("Featured image can only be jpg, png, gif, or webp formats!")
            else:
                featured_filename = secure_filename(featured_image.filename)
                # make filename unique
                featured_filename = unique_filename(featured_filename)

                # set featured_image filepath
                filepath = os.path.join(
                    current_app.config["UPLOAD_FOLDER"], featured_filename
                )

                # upload and save the image with defined `filepath`
                featured_image.save(filepath)
        else:
            featured_filename = post.featured_image_path

        # check or set slug if none is submitted
        if not slug:
            slug = slugify(title)

        # check if slug is existing
        existing_slug = Post.query.filter_by(slug=slug).first()

        if existing_slug and slug != post.slug:
            flash("Slug already exists", "danger")

        # process the data
        else:
            # retrieve the selected categories and terms
            category_ids = post_form.categories.data
            tag_ids = post_form.tags.data

            # retrieve the corresponding `Term` objects from the database
            categories = Term.query.filter(Term.id.in_(category_ids)).all()
            tags = Term.query.filter(Term.id.in_(tag_ids)).all()

            # update post details
            post.title = title
            post.slug = slug
            post.description = post_form.description.data
            post.content = post_form.content.data
            post.featured_image_path = featured_filename
            post.status = post_form.status.data
            post.terms = categories + tags
            post.modified_at = db.func.now()

            # add the Post instance to database
            db.session.add(post)
            db.session.commit()

            flash("Post updated!", "success")

            return redirect(url_for("post.posts"))
    else:
        # validation not passed
        for field, errors in post_form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "error")

    # populate the `post_form` with existing data based on `post.id`
    # also preselect options already in post category and tags term
    post_form.title.data = post.title
    post_form.slug.data = post.slug
    post_form.description.data = post.description
    post_form.content.data = post.content
    post_form.status.data = post.status
    post_form.categories.process_data([term_id for term_id in post.terms])
    post_form.tags.process_data([term_id for term_id in post.terms])

    return render_template("/dashboard/edit_post.html", form=post_form, post=post)


@post.route("/delete/<int:id>")
@login_required
def delete_post(id):
    """Route to delete post"""

    # get the post by id
    post = Post.query.get(id)

    # delete the post from session and commit to database
    db.session.delete(post)
    db.session.commit()

    flash("Category deleted successfully!", "success")

    return redirect(url_for("post.posts"))
