from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db


class User(db.Model):
    """Users Model"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), index=True,
                         unique=True, nullable=False)
    full_name = db.Column(db.String(80))
    email = db.Column(db.String(250), unique=True, nullable=False)
    bio = db.Column(db.Text)
    password_hash = db.Column(db.String(250), nullable=False)

    posts = db.relationship('Post', backref='user', lazy=True)

    def __repr__(self):
        """String representation of User object"""
        return f"User: {self.username}<{self.email}>"

    def set_password(self, password):
        """Hash password and set `password_hash` for `User` object"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check hash password and check that it matches `User` `password_hash`"""
        return check_password_hash(self.password_hash, password)
