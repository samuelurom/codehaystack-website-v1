from ..extensions import db

terms = db.Table(
    "terms",
    db.Column("term_id", db.Integer, db.ForeignKey("term.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
)


class Term(db.Model):
    """Model for Tags"""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), unique=True, index=True)
    description = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(120), unique=True)
    taxonomy = db.Column(db.Enum("Category", "Tag"), nullable=False)

    def __repr__(self):
        """String representation of Term Model"""
        return f"{self.id}"

    def get_terms_by_taxonomy(taxonomy):
        """Method to return a list of terms that match a specific `taxonomy`"""
        return Term.query.filter_by(taxonomy=taxonomy).order_by(Term.name).all()
