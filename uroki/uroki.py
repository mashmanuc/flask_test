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
    tema_test_id=1
    temma=find_Tema_test_by_id(tema_test_id)
    data=find_temi_by_test(tema_test_id)
    num_quest=int(data[test_id-1].num_quest.split()[-1])

    pr_vid=data[test_id-1].vidpov
    add_user_test(users_id, num_quest, tema_test_id, test_id, an, pr_vid)
    tata=user_test(users_id, tema_test_id)

    for i,j in tata:
        print(i,j)

    form=NameForm()
    m_ans=mass_ans(tema_test_id)
    return render_template('testes_ur.html',data=data, m_ans= m_ans, temma=temma,form=form,tata=tata)
"""************************Test**************************"""
@uroki.route('/urok_test/')
def urok_test():
    if current_user.is_authenticated:
        tema_test_id=1
        temma=find_Tema_test_by_id(tema_test_id)
        return render_template('page_test/urok_test.html', temma=temma)
    else: return redirect((url_for('login')))


@uroki.route('/page_test/<int:tema_test_id>/')
def page_test(tema_test_id):
    users_id=current_user.id
    temma=find_Tema_test_by_id(tema_test_id)
    test=first_tema_test( tema_test_id)
    print(tema_test_id)
    m_ans=tes_ans(test.id)
    print(test.id)
    tata=find_vid(users_id, tema_test_id, test.id)
    max_question_id=len(find_temi_by_test(tema_test_id))
    # dinamic=user_test(users_id, tema_test_id)
    dinamics=dinamic(users_id, tema_test_id)

    return render_template('page_test/page_test.html',dinamics=dinamics,test=test,m_ans=m_ans , temma=temma,max_question_id=max_question_id)
from flask import request


@uroki.route('/show_question/<int:tema_test_id>/<int:test_id>/<string:an>/')
def show_question(tema_test_id,test_id,an):
    temma = find_Tema_test_by_id(tema_test_id)
    test = find_test(test_id)
    users_id=current_user.id
    temma = find_Tema_test_by_id(tema_test_id)
    print(test.vidpov)
    pr_vid=test.vidpov
    num_quest =test.num_quest

    add_user_test(users_id,num_quest , tema_test_id, test_id, an, pr_vid)
    tata=find_vid(users_id, tema_test_id, test.id)
    m_ans = tes_ans(test_id)
    print(tata)
    print(m_ans)
    # dinamic=user_test(users_id, tema_test_id)
    dinamics=dinamic(users_id, tema_test_id)

    # Assuming max_question_id is the maximum ID of questions
    max_question_id = len(find_temi_by_test(tema_test_id))

    return render_template('page_test/page_test.html',dinamics=dinamics,tata=tata, test=test, m_ans=m_ans, temma=temma, max_question_id=max_question_id)

@uroki.route('/show_next_quest/<int:tema_test_id>/<int:test_id>')
def show_next_quest(tema_test_id,test_id):
    temma=find_Tema_test_by_id(tema_test_id)
    users_id=current_user.id
    test=find_test(test_id+1)
    tata=find_vid(users_id, tema_test_id, test.id)
    m_ans=tes_ans(test_id+1)
    max_question_id=len(find_temi_by_test(tema_test_id))
    # dinamic=user_test(users_id, tema_test_id)
    dinamics=dinamic(users_id, tema_test_id)


    return render_template('page_test/page_test.html',dinamics=dinamics, test=test, tata=tata, m_ans=m_ans , temma=temma,max_question_id=max_question_id)
