from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from slugify import slugify

from ..forms import TermForm
from ..models.post import terms, Post, Term
from ..extensions import db

# create `Blueprint`
tag = Blueprint("tag", __name__, url_prefix="/dashboard/tags")


@tag.route("/", methods=["GET", "POST"])
@login_required
def tags():
    """Route to view and manage tag `Term` in database"""

    # new instance of `TermForm`
    term_form = TermForm()

    # get all tags in database
    all_tags = Term.query.filter_by(taxonomy="Tag").order_by(Term.name).all()

    # if form is submitted
    if term_form.validate_on_submit():
        # get submitted term name and slug
        name = term_form.name.data
        slug = slugify(term_form.slug.data)

        # check or set slug if not submitted
        if not slug:
            slug = slugify(name)

        # check if name or slug exists
        if Term.query.filter_by(name=name).first():
            flash("Term already exists", "danger")
        elif Term.query.filter_by(slug=slug).first():
            flash("Slug already exists", "danger")
        else:
            # create a new `Term` instance
            new_term = Term(
                name=name,
                slug=slug,
                taxonomy="Tag",
                description=term_form.description.data,
            )

            # add the `Term` instance to database
            db.session.add(new_term)
            db.session.commit()

            # flash success message
            flash("Term created", "success")

            return redirect(url_for("tag.tags"))
    else:
        # validation not passed
        for field, errors in term_form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "error")

    return render_template("/dashboard/tags.html", form=term_form, tags=all_tags)


@tag.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_tag(id):
    """Route to edit `tag` term."""

    # get the tag based on passed id
    tag = Term.query.filter_by(id=id).first()

    # new instance of Term form
    term_form = TermForm()

    # validate the form and update record in database
    if term_form.validate_on_submit():
        # get submitted term name and slug
        name = term_form.name.data
        slug = slugify(term_form.slug.data)

        # check or set slug if not submitted
        if not slug:
            slug = slugify(name)

        # check if name or slug exists
        existing_name = Term.query.filter_by(name=name).first()
        existing_slug = Term.query.filter_by(slug=slug).first()

        if existing_name and name != tag.name:
            flash("Term already exists", "danger")
        elif existing_slug and slug != tag.slug:
            flash("Slug already exists", "danger")
        else:
            # update the records
            tag.name = name
            tag.slug = slug
            tag.description = term_form.description.data

            db.session.add(tag)
            db.session.commit()

            flash("Tag updated successfully!", "success")

            return redirect(url_for("tag.tags"))
    else:
        # validation not passed
        for field, errors in term_form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "error")

    # populate the form data with existing record from database
    term_form.name.data = tag.name
    term_form.slug.data = tag.slug
    term_form.description.data = tag.description

    return render_template("/dashboard/edit_tag.html", form=term_form)


@tag.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_tag(id):
    # get the record based on id
    tag = Term.query.get(id)

    # delete the record from the session and commit to database
    db.session.delete(tag)
    db.session.commit()

    return redirect(url_for("tag.tags"))
