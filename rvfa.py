from flask import render_template, request, session
from database import User, Wallet, Transaction, db
from app import app
from auth import authenticate
import sqlalchemy

import uuid
import hashlib

DEMOS = {
  'login': {
    'title': 'LOGIN',
    'name': 'Generation of Error Message Containing Sensitive Information',
    'description': 'The product generates an error message that includes sensitive information about its environment, users, or associated data.',
    'template': 'pages/login.html',
    'CWE': 'CWE-209'
  },
  'register': {
    'title': 'REGISTER',
    'name': 'Generation of Error Message Containing Sensitive Information',
    'description': 'The product generates an error message that includes sensitive information about its environment, users, or associated data.',
    'template': 'pages/register.html',
    'CWE': 'CWE-209'
  }
}

@app.route("/")
def index():
  return render_template("index.html", DEMOS = DEMOS)

@app.route("/pages/home")
def home():
  if not '_id' in session:
    return app.redirect("/")
  
  query = sqlalchemy.select(User).where(User.id == int(session["_id"]))
  user, = db.session.execute(query).first().tuple()

  return render_template("pages/home.html", USER = user)

@app.route("/pages/<name>")
def demo(name: str):
  if not name in DEMOS:
    return app.redirect("/")
  
  return render_template(DEMOS[name]['template'], **DEMOS[name])

@app.post("/demo/CWE-209/login")
def demo_209_login():
  data = request.json

  query = sqlalchemy.select(User).where(User.username == data['username'])

  user = db.session.execute(query).first()

  if user is None:
    return {'error': 'User not found'}
  else:
    user_obj, = user.tuple()

    if hashlib.md5(data['password'].encode('utf-8')).digest() == user_obj.password:
      session['_id'] = user_obj.id
      return {'success': 'Yay! Valid Credentails!!'}
    return {'error': 'Incorrect Password'}
  
@app.post("/demo/CWE-209/register")
def demo_209_register():
  data = request.json

  data['password'] = hashlib.md5(data['password'].encode('utf-8')).digest()

  try:
    stmt = sqlalchemy.insert(User).values(**data)
    db.session.execute(stmt)
    db.session.commit()

    query = sqlalchemy.select(User).where(User.username == data['username'])
    user = db.session.execute(query).first()

    user_obj, = user.tuple()

    session['_id'] = user_obj.id
  except sqlalchemy.exc.IntegrityError:
    return {'error': 'User already exists'}

  return {'success': 'Registration successfull'}

@app.post('/demo/cwe-287/transaction')
def demo_287_transaction():
  data = request.json

  if "_id" not in session or data is None:
    return app.redirect('/')
  
  user_id = int(session["_id"])
  reference = uuid.uuid4().__str__()

  stmt = sqlalchemy.insert(Transaction).values(reference=reference)
  