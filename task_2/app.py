from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Configuration)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=Configuration.POSTGRE_URI)
db = SQLAlchemy(app)
