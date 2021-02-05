from . import db


class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(64), unique=True, index=True)
        first_name = db.Column(db.String(64), unique=False, index=True)
        last_name = db.Column(db.String(64), unique=False, index=True)
        role = db.Column(db.Integer, db.ForeignKey('roles.id'))
        def __repr__(self):
                return '<User %r>' % self.email



