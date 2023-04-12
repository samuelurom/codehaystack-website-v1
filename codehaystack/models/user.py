from ..extensions import db


class User(db.Model):
    """Users Model"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), index=True,
                         unique=True, nullable=False)
    full_name = db.Column(db.String(80))
    email = db.Column(db.String(250), unique=True, nullable=False)
    bio = db.Column(db.Text)
    posts = db.relationship('Post', backref='user', lazy=True)

    def __repr__(self):
        """String representation of User object"""
        return f"User: {self.username}<{self.email}>"
