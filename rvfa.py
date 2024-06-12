from flask import Flask, render_template, request
from database import db, User, sqlalchemy

import hashlib

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rvfa.db"
db.init_app(app)

with app.app_context():
  db.create_all()

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
    print(user_obj.password)
    if hashlib.md5(data['password'].encode('utf-8')).digest() == user_obj.password:
      return {'success': 'Yay! Valid Credentails!!'}
    return {'error': 'Incorrect Password'}
  
@app.post("/demo/CWE-209/register")
def demo_209_register():
  data = request.json

  data['password'] = hashlib.md5(data['password'].encode('utf-8')).digest()

  stmt = sqlalchemy.insert(User).values(**data)
  db.session.execute(stmt)
  db.session.commit()

  return {'success': 'Registration successfull'}