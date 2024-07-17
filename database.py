from flask_sqlalchemy import SQLAlchemy, model
from sqlalchemy import ForeignKey, insert, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app import app

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

db.init_app(app)

with app.app_context():
  db.create_all()

class Model(db.Model):
  @classmethod
  def create(Self: type[model.Model], **kwargs):
    stmt = insert(Self).values(kwargs)
    db.session.execute(stmt)
    db.session.commit()

  @classmethod
  def from_id[T: type[Model]](Self: T, id: int) -> 'T | None':
    query = select(Self).where(Self.id == id)

    result = db.session.execute(query).first()

    if result is None:
      return result
    
    user, = result.tuple()

    return user

class User(db.Model):
  __tablename__ = "user"

  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(unique=True)
  email: Mapped[str] = mapped_column()
  password: Mapped[str] = mapped_column()

  @classmethod
  def create(Self, **kwargs):
    stmt = insert(Self).values(kwargs)
    db.session.execute(stmt)
    db.session.commit()

  @classmethod
  def from_id(Self, id) -> 'User | None':
    query = select(Self).where(Self.id == id)

    result = db.session.execute(query).first()

    if result is None:
      return result
    
    user, = result.tuple()

    return user

class Wallet(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True)
  account_number: Mapped[str] = mapped_column(unique=True)
  name: Mapped[str] = mapped_column()
  user: Mapped[int] = mapped_column()

  @classmethod
  def create(Self, **kwargs):
    stmt = insert(Self).values(kwargs)
    db.session.execute(stmt)
    db.session.commit()

  @classmethod
  def from_id(Self, id) -> 'Wallet | None':
    query = select(Self).where(Self.id == id)

    result = db.session.execute(query).first()

    if result is None:
      return result
    
    obj, = result.tuple()

    return obj

class Transaction(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True)
  reference: Mapped[str] = mapped_column(unique=True)
  amount: Mapped[int] = mapped_column()
  user: Mapped[int] = mapped_column()
  wallet: Mapped[int] = mapped_column()

  @classmethod
  def create(Self, **kwargs):
    stmt = insert(Self).values(kwargs)
    db.session.execute(stmt)
    db.session.commit()

  @classmethod
  def from_id(Self, id) -> 'Transaction | None':
    query = select(Self).where(Self.id == id)

    result = db.session.execute(query).first()

    if result is None:
      return result
    
    obj, = result.tuple()

    return obj
