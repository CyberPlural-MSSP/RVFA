from flask import session
from database import User, db
import base64

import sqlalchemy

def authenticate(id: int) -> str:
  query = sqlalchemy.select(User).where(User.id == id)
  user, = db.session.execute(query).first().tuple()

  return base64.b64encode((user.email + ':' + str(user.id)).encode('utf-8')).decode('utf-8')
