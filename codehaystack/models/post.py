from ..extensions import db

terms = db.Table('terms',
                 db.Column('term_id', db.Integer, db.ForeignKey(
                     'term.id'), primary_key=True),
                 db.Column('post_id', db.Integer, db.ForeignKey(
                     'post.id'), primary_key=True)
                 )


class Post(db.Model):
    """Post Model"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(250), index=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, index=True, nullable=False)
    content = db.Column(db.Text, index=True, nullable=False)
    featured_image_path = db.Column(db.String(250))
    status = db.Column(db.String(20), index=True,
                       server_default='draft', nullable=False)
    created_at = db.Column(db.DateTime, index=True,
                           server_default=db.func.now(), nullable=False)
    post_type = db.Column(db.Enum('post', 'page'), index=True, nullable=False)
    modified_at = db.Column(db.DateTime, index=True,
                            server_default=db.func.now(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    terms = db.relationship(
        'Term', secondary=terms, lazy='subquery', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        """String representation of Posts Model"""
        return f"Post: {self.title}, Published {self.published_date}"


class Term(db.Model):
    """Model for Tags"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), unique=True, index=True)
    description = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(120), unique=True)
    taxonomy = db.Column(db.Enum('category', 'tag'), nullable=False)

    def __repr__(self):
        """String representation of Term Model"""
        return f"Term {self.taxonomy}: {self.name}"
