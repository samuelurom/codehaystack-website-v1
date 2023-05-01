from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from slugify import slugify

from ..forms import TermForm
from ..models.post import terms, Post, Term
from ..extensions import db

# create `Blueprint`
category = Blueprint("category", __name__, url_prefix="/dashboard/categories")


@category.route("/", methods=["GET", "POST"])
@login_required
def categories():
    """Route to view and manage category `Term` in database"""

    # new instance of `TermForm`
    term_form = TermForm()

    # get all categories in database
    all_categories = Term.query.filter_by(taxonomy="Category").order_by(Term.name).all()

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
                taxonomy="Category",
                description=term_form.description.data,
            )

            # add the `Term` instance to database
            db.session.add(new_term)
            db.session.commit()

            # flash success message
            flash("New category added successfully!", "success")

            return redirect(url_for("category.categories"))
    else:
        # validation not passed
        for field, errors in term_form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "error")

    return render_template(
        "/dashboard/categories.html", form=term_form, categories=all_categories
    )


@category.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_category(id):
    """Route to edit `category` term."""

    # get the category based on passed category
    category = Term.query.get(id)

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

        if existing_name and name != category.name:
            flash("Term already exists", "danger")
        elif existing_slug and slug != category.slug:
            flash("Slug already exists", "danger")
        else:
            # update the records
            category.name = name
            category.slug = slug
            category.description = term_form.description.data

            db.session.add(category)
            db.session.commit()

            flash("Category updated successfully!", "success")

            return redirect(url_for("category.categories"))
    else:
        # validation not passed
        for field, errors in term_form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "error")

    # populate the form data with existing record from database
    term_form.name.data = category.name
    term_form.slug.data = category.slug
    term_form.description.data = category.description

    return render_template("/dashboard/edit_category.html", form=term_form)


@category.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_category(id):
    # get the record based on id
    category = Term.query.get(id)

    # delete the record from the session and commit to database
    db.session.delete(category)
    db.session.commit()

    flash("Category deleted successfully!", "success")

    return redirect(url_for("category.categories"))
