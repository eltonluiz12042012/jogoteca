
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bscrypt = Bcrypt(app)
from views_user import *

from views_games import *

if __name__ == '__main__':
    app.run(debug=True)
