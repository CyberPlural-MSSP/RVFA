from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'RVFA'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rvfa.db"