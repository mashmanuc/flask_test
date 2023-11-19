from flask import *
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from datetime import datetime
from flask_login import UserMixin
db = SQLAlchemy()

# DEFINE YOUR MODELS HERE


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)





class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def checkPassword(self, entered_password):
        return sha256_crypt.verify(entered_password, self.password)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = sha256_crypt.encrypt(password)

        return None
    def get_id(self):
        return str(self.id)
# # FLASK_ADMIN CONFIGURATION
# class DefaultModelView(ModelView):
#     restricted = True

#     def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, **kwargs):
#         self.column_default_sort = ('id', True)
#         super(DefaultModelView, self).__init__(model, session, name=name, category=category, endpoint=endpoint, url=url)

#     def is_accessible(self):
#         return current_user.is_admin

#     def inaccessible_callback(self, name, **kwargs):
#         abort(401)
# ---------------------------------------------------------------------------- #
class User_test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, nullable=False)
    tema_test_id =  db.Column(db.Integer, nullable=False)
    test_id = db.Column(db.Integer, nullable=False)
    vid = db.Column(db.String(120), nullable=False)
    pr_vid= db.Column(db.String(120), nullable=False)
    date_completed = db.Column(db.DateTime, default=datetime.utcnow)



    def __init__(self, users_id,tema_test_id, test_id,  vid,  pr_vid  ):
            self.users_id = users_id
            self.tema_test_id  = tema_test_id
            self.test_id = test_id
            self.vid = vid
            self.pr_vid  = pr_vid
def add_user_test(users_id, tema_test_id, test_id, vid, pr_vid):
    new_user_test = User_test(users_id=users_id, tema_test_id=tema_test_id, test_id=test_id, vid=vid, pr_vid=pr_vid)
    db.session.add(new_user_test)
    db.session.commit()
with app.app_context():
    db.create_all()
