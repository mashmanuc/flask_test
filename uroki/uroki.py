from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
# SQLALCHEMY_DATABASE_URI ='mysql+mysqlconnector://mash:123mMm321@mash.mysql.database.azure.com:3306/prosto'
from uroki.forms_ur import NameForm
from flask_login import current_user, login_required

from func import *
title='Goooooo'
uroki= Blueprint('uroki', __name__, template_folder='templates')

from model import *
from models import *



@uroki.app_template_filter('zip')
def jinja2_zip(a, b):
    return zip(a, b)
predmets = get_all_items(Predmet)
claasses = get_all_items(Claass)
tema_test=get_all_items(Tema_test)
testes=get_all_items(Test)


@uroki.route('/')
# @login_required
def index_ur():
        data=find_temi_by_test(1)

        temma=find_Tema_test_by_id(1)
        form=NameForm()
        m_ans=mass_ans(1)
        return render_template('testes_ur.html',data=data, m_ans= m_ans, temma=temma,form=form)


@uroki.route('/predmet_ur/<int:predmet_id>')
def predmet_ur(predmet_id=2):
    # Create a new SQLAlchemy session
    claass_list = ob1_ob2(classs=Predmet,id=predmet_id)
    return render_template('predmet_ad.html',title=title,  claass_list=claass_list)



@uroki.route('/tema_test_ur/<int:id>')
def tema_test_ur(id):
    per_page = 20  # You can adjust this to the desired number of items per page
    page = request.args.get('page', type=int, default=1)
    test_names = find_temi_by_predmet(id)
    pagination_info = paginate_query(test_names, page, per_page)
    return render_template('tema_test_ad.html',  pagination=pagination_info, id=id)


@uroki.route('/testes_ur/<int:id>')
def testes_ur(id):
    data=find_temi_by_test(id)

    m_ans=mass_ans(id)
    return render_template('testes_ur.html',data=data, m_ans= m_ans,)


@uroki.route('/testes_ur/<int:tema_test_id>/<int:test_id>/<string:an>/')
def save_test(tema_test_id,test_id,an):
    users_id=current_user.id
    print(tema_test_id)
    print(test_id)
    vid=an
    pr_vid="777"
    add_user_test(users_id, tema_test_id, test_id, vid, pr_vid)
    data=find_temi_by_test(1)
    temma=find_Tema_test_by_id(1)
    form=NameForm()
    m_ans=mass_ans(1)
    return render_template('testes_ur.html',data=data, m_ans= m_ans, temma=temma,form=form)
