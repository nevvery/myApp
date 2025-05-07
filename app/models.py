import datetime

from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import login


@login.user_loader
def load_user(user_id: str) -> Optional['Parent']:
    return db.session.get(Parent, int(user_id))


class Parent(db.Model, UserMixin):
    __tablename__: str = 'parents'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    surname: so.Mapped[str] = so.mapped_column(sa.String(64))
    patronymic: so.Mapped[str | None] = so.mapped_column(sa.String(64), nullable=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)

    children: so.Mapped[list['Child']] = so.relationship(back_populates='parent')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Child(db.Model):
    __tablename__: str = 'children'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    surname: so.Mapped[str] = so.mapped_column(sa.String(64))
    patronymic: so.Mapped[str | None] = so.mapped_column(sa.String(64), nullable=True)
    group: so.Mapped[str] = so.mapped_column(sa.String(64))

    id_parent: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Parent.id), index=True)
    parent: so.Mapped[Parent] = so.relationship(back_populates="children")


class Payment(db.Model):
    __tablename__ = 'payments'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    value: so.Mapped[float] = so.mapped_column(sa.Float)
    last_pay: so.Mapped[datetime.datetime] = so.mapped_column(sa.DateTime(timezone=True), nullable=True, index=True)

    id_payment_from_parent: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Parent.id), index=True)
