from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import sqlalchemy

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(unique=True)
  email: Mapped[str] = mapped_column()
  password: Mapped[str] = mapped_column()