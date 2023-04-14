from ..extensions import db


class Post(db.Model):
    """Post Model"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(250), index=True, nullable=False)
    url = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, index=True, nullable=False)
    content = db.Column(db.Text, index=True, nullable=False)
    featured_image_path = db.Column(db.String(250))
    status = db.Column(db.String(20), index=True,
                       server_default='draft', nullable=False)
    created_at = db.Column(db.DateTime, index=True,
                           server_default=db.func.now(), nullable=False)
    modifiled_at = db.Column(db.DateTime, index=True,
                             server_default=db.func.now(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """String representation of Posts Model"""
        return f"Post: {self.title}, Published {self.published_date}"
