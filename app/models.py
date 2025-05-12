import datetime

from sqlalchemy.orm import relationship

from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import login


@login.user_loader
def load_user(user_id: str) -> Optional['Parent']:
    return db.session.get(Parent, int(user_id))


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('parents.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(80), unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255))


class Parent(db.Model, UserMixin):
    __tablename__: str = 'parents'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    surname: so.Mapped[str] = so.mapped_column(sa.String(64))
    patronymic: so.Mapped[str | None] = so.mapped_column(sa.String(64), nullable=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)

    fs_uniquifier: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False, unique=True)
    active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)
    roles: so.Mapped[list[Role]] = relationship('Role', secondary=roles_users,
                                                backref=db.backref('users', lazy='dynamic'))

    children: so.Mapped[list['Child']] = so.relationship(back_populates='parent')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_id(self) -> str:
        return str(self.fs_uniquifier)


class Child(db.Model):
    __tablename__: str = 'children'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    surname: so.Mapped[str] = so.mapped_column(sa.String(64))
    patronymic: so.Mapped[str | None] = so.mapped_column(sa.String(64), nullable=True)
    group: so.Mapped[str] = so.mapped_column(sa.String(64))

    id_parent: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('parents.id', name='fk_child_parent_id'), index=True
    )
    parent: so.Mapped[Parent] = so.relationship(back_populates="children")


class Payment(db.Model):
    __tablename__: str = 'payments'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    value: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    date_pay: so.Mapped[datetime.datetime] = so.mapped_column(sa.DateTime(timezone=True), nullable=True, index=True)
    path_pdf_file: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)

    id_child: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('children.id', name='fk_payment_child_id'), index=True
    )
