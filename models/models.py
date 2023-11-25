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
    num_quest=db.Column(db.Integer, nullable=False)
    users_id = db.Column(db.Integer, nullable=False)
    tema_test_id =  db.Column(db.Integer, nullable=False)
    test_id = db.Column(db.Integer, nullable=False)
    vid = db.Column(db.String(120), nullable=False)
    pr_vid= db.Column(db.String(120), nullable=False)
    date_completed = db.Column(db.DateTime, default=datetime.utcnow)



    def __init__(self, users_id,num_quest,tema_test_id, test_id,  vid,  pr_vid  ):
            self.users_id = users_id
            self.num_quest=num_quest
            self.tema_test_id  = tema_test_id
            self.test_id = test_id
            self.vid = vid
            self.pr_vid  = pr_vid
# def add_user_test(users_id, tema_test_id, test_id, vid, pr_vid):
#     new_user_test = User_test(users_id=users_id, tema_test_id=tema_test_id, test_id=test_id, vid=vid, pr_vid=pr_vid)
#     db.session.add(new_user_test)
#     db.session.commit()
def add_user_test(users_id,num_quest, tema_test_id, test_id, vid, pr_vid):
    # Перевірка, чи існує вже запис для користувача і номера тесту
    existing_record = User_test.query.filter_by(users_id=users_id, test_id=test_id).first()

    if existing_record:
        # Якщо запис існує, змінюємо його значення
        existing_record.vid = vid
        existing_record.pr_vid = pr_vid
    else:
        # Якщо запису немає, додаємо новий запис
        new_user_test = User_test(users_id=users_id,num_quest=num_quest, tema_test_id=tema_test_id, test_id=test_id, vid=vid, pr_vid=pr_vid)
        db.session.add(new_user_test)

    # Зберігаємо зміни в базі даних
    db.session.commit()
def user_test(users_id, tema_test_id):
    # Перевірка, чи існує вже запис для користувача і номера тесту
    record = User_test.query.filter_by(users_id=users_id, tema_test_id=tema_test_id).all()

    if record:
       return [ (m.test_id , m.vid, (m.num_quest.split()[-1]) ) for m in record  ]
def dinamic(users_id, tema_test_id):
    record = User_test.query.filter_by(users_id=users_id, tema_test_id=tema_test_id).all()

    if record:
       return [ m.test_id  for m in record  ]


def user_t_ans(users_id, tema_test_id):
    # Перевірка, чи існує вже запис для користувача і номера тесту
    record = User_test.query.filter_by(users_id=users_id, tema_test_id=tema_test_id).all()

    if record:
       return [ (m.test_id, m.vid) for m in record  ]

def find_vid(users_id, tema_test_id, test_id):
    # Використовуйте метод query вашого ORM для пошуку відповідного запису в базі даних.
    user_test_record = User_test.query.filter_by(users_id=users_id, tema_test_id=tema_test_id, test_id=test_id).first()

    # Перевірте, чи знайдено відповідний запис.
    if user_test_record:
        return user_test_record.vid
    else:
        return None  # Або ви можете повернути яке-небудь значення за замовчуванням або порожній рядок.


with app.app_context():
    db.create_all()
