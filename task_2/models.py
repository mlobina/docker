from app import db
from datetime import datetime
import re
from sqlalchemy import exc
import errors


def slugify(_string):
    """Функция для получения slug строки"""
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', _string)


class BaseModelMixin:

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadLuck

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
        except exc.IntegrityError:
            raise errors.BadLuck


class Advertisement(db.Model, BaseModelMixin):
    __tablename__ = 'advertisements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    slug = db.Column(db.String(64), unique=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, *args, **kwargs):
        """Конструктор класса"""
        super(Advertisement, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        """Получаем slug заголовка объявления"""
        self.slug = slugify(self.title)

    def __repr__(self):
        return f'<Advertisement {self.id} - {self.title}>'


class User(db.Model, BaseModelMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), unique=True)
    advertisements = db.relationship(Advertisement, backref='user')

    def __init__(self, *args, **kwargs):
        """Конструктор класса"""
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'
