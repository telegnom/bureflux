from app import db, login
import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Accounts(db.Model):
    id = db.Column(db.String(42), primary_key=True, default=str(uuid.uuid4()))
    nickname = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    modified_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())


class Vouchers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voucher = db.Column(db.String(128), unique=True)
    assigned_at = db.Column(db.DateTime, nullable=True, default=None)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    modified_at = db.Column(db.DateTime, default=datetime.datetime.now())


class Requests(db.Model):
    id = db.Column(db.String(42), primary_key=True, default=str(uuid.uuid4()))
    nickname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    request_type = db.Column(db.Integer)
    requested_by = db.Column(db.String(42), db.ForeignKey("accounts.id"))
    voucher = db.Column(db.Integer, db.ForeignKey("vouchers.id"))
    requestor_comment = db.Column(db.Text, nullable=True)
    admin_comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    modified_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())


class Admins(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    nickname = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    modified_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())

    def set_password(self, password):
        print(password, self.nickname)
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    return Admins.query.get(int(id))
