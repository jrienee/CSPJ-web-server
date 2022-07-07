from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy_utils.functions import database_exists
from flask_mail import Mail



app = Flask(__name__)
app.config['SECRET_KEY'] = '1c08ad57cd5716ddd3e425afab3b7d5b'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' #name of the function
login_manager.login_message_category = 'info' #class name of bootstrap

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'aspj.ecommerce.review@gmail.com'
app.config['MAIL_PASSWORD'] = 'Abcd1234!'
mail = Mail(app)

db.init_app(app)
# if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
#     pass
# else:
#     with app.app_context():
#         from flaskblog.models import User,Post
#         db.create_all()
#         db.session.commit()

from flaskblog import routes

from flaskblog.posts.routes import posts
app.register_blueprint(posts)

