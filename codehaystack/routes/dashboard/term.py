from flask import (Blueprint, render_template, redirect, url_for, flash)
from flask_login import login_required
from slugify import slugify

from ...forms import TermForm
from ...models.post import terms, Post, Term
from ...extensions import db

# create `Blueprint`
term = Blueprint("term", __name__, url_prefix='/dashboard')


@term.route("/create-term", methods=["GET", "POST"])
@login_required
def create_term():
    # new instance of `TermForm`
    term_form = TermForm()

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
                taxonomy=term_form.taxonomy.data,
                description=term_form.description.data
            )

            # add the `Term` instance to database
            db.session.add(new_term)
            db.session.commit()

            # flash success message
            flash("Term created", "success")

            return redirect(url_for("manage_term.create_term"))
    else:
        # validation not passed
        for field, errors in term_form.errors.items():
            for error in errors:
                flash(f"{field.title().replace('_', ' ')}: {error}", "error")

    return render_template("/dashboard/create_term.html", form=term_form)
