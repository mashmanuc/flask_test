from sqlalchemy import Column, Integer, String,  ForeignKey,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
# import sqlalchemy
from sqlalchemy import create_engine
Base = declarative_base()



class Predmet(Base):
    __tablename__ = 'predmet'
    id = Column(Integer, primary_key=True)
    predmet_name = Column(String(255))
    claass_list = relationship("Claass", back_populates="predmet")

class Claass(Base):
    __tablename__ = 'claass'
    id = Column(Integer, primary_key=True)
    claass_name = Column(String(255))
    predmet_id = Column(Integer, ForeignKey('predmet.id'))
    predmet = relationship("Predmet", back_populates="claass_list")
    tema_test_list = relationship("Tema_test", back_populates="claass")

class Tema_test(Base):
    __tablename__ = 'tema_test'
    id = Column(Integer, primary_key=True)
    test_name = Column(String(255))
    claass_id = Column(Integer, ForeignKey('claass.id'))
    claass = relationship("Claass", back_populates="tema_test_list")
    test_list = relationship("Test", back_populates="tema_test")

class Test(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True)
    num_quest = Column(String(255))
    quest_img = Column(String(255))
    quest_text = Column(String(255))
    ans_data = Column(String(255))
    vidpov= Column(String(255))
    tema_test_id = Column(Integer, ForeignKey('tema_test.id'))
    tema_test = relationship("Tema_test", back_populates="test_list")







# engine = sqlalchemy.create_engine('mysql+mysqlconnector://mash:123mMm321@mash.mysql.database.azure.com:3306/prosto')
engine = create_engine("sqlite:///E:/project/flask51/flask/basaSS.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def add_predmet(predmet_name):
    try:
        with Session() as session:
            new_predmet = Predmet(predmet_name=predmet_name)
            session.add(new_predmet)
            session.commit()
    except Exception as e:
        print(f"Помилка додавання предмету: {e}")

def add_claass(claass_name,predmet_id):
    try:
        with Session() as session:
            new_claass = Claass(claass_name=claass_name,predmet_id=predmet_id)
            session.add(new_claass)
            session.commit()
    except Exception as e:
        print(f"Помилка додавання предмету: {e}")
"""************************************************************************"""
def add_Tema_test(test_name, claass_id ):
    try:
        with Session() as session:
            new_Tema_test = Tema_test(test_name=test_name, claass_id =claass_id )
            session.add(new_Tema_test)
            session.commit()
    except Exception as e:
        print(f"Помилка додавання теми: {e}")
"""************************************************************************"""
# add_Tema_test(test_name="все", claass_id =1 )
def ob1_ob2(classs=Predmet,id=1):
    with Session() as session:
        # Retrieve the Predmet with the specified ID
        predmet = session.query(classs).filter_by(id=id).first()
        # Access claass_list while the session is open
        return predmet.claass_list

"""************************************************************************"""
def ob2_ob3(classs=Claass,id=1):
    with Session() as session:
        claass = session.query(classs).filter_by(id=id).first()
        return claass.tema_test_list

"""************************************************************************"""
def find_last_Tema_test():
    try:
        with Session() as session:
            last_Tema_test = session.query(Tema_test).order_by(Tema_test.id.desc()).first()
            return last_Tema_test
    except Exception as e:
        print(f"Помилка пошуку останньої теми: {e}")
        return None
"""************************************************************************"""
def find_claass(id):
    try:
        with Session() as session:
            last = session.query(Claass).filter_by(id=id).first()
            return last
    except Exception as e:
        print(f"Помилка пошуку останньої теми: {e}")
        return None
"""************************************************************************"""

def find_Tema_test_by_id(Tema_test_id):
    try:
        with Session() as session:
            t_test = session.query(Tema_test).filter_by(id=Tema_test_id).first()
            return t_test
    except Exception as e:
        print(f"Помилка пошуку теми: {e}")
        return None
def find_temi_by_predmet(id):
    """шукаєм назви тем по id класу(1-8)"""
    try:
        with Session() as session:
            temi = session.query(Tema_test).filter(Tema_test.claass_id == id).all()
            return temi
    except Exception as e:
        print(f"Помилка пошуку тем за предметом: {e}")
        return []
def find_temi_by_test(id):
    """шукаєм назви тем по id класу(1-8)"""
    try:
        with Session() as session:
            temi = session.query(Test).filter(Test.tema_test_id == id).all()
            return temi
    except Exception as e:
        print(f"Помилка пошуку тем за предметом: {e}")
        return []
def find_test_to_slovo(slovo):
    mass=[]
    m_slovo= [word[:-2].lower() if len(word) > 3 else word for word in slovo.split()]
    try:
        with Session() as session:
            last_Tema_test = session.query(Tema_test).all()
            for tema in last_Tema_test:
                m_text = [word[:-2].lower() if len(word) > 3 else word for word in tema.test_name.split()]
                fl=False
                for i in m_slovo:
                    if (len(i)<4) or (i in m_text):
                        fl=True
                    else:
                        fl=False
                        break
                if fl==True:
                    mass.append(tema)
        # print(mass)
        return mass
    except Exception as e:
        print(f"Помилка пошуку останньої теми: {e}")

        return None
# print(len(find_test_to_slovo('рівняння')))

def mass_ans(id):
    """Перетворює відповіді з бази даних у список"""
    return [item.ans_data.replace("\n","").replace('\r', '').replace('\xa0', '').split('!')for item in find_temi_by_test(id)]
def tes_ans(id_):
    """Перетворює відповіді з бази даних у список"""
    try:
        with Session() as session:
            test = session.query(Test).filter_by(id=id_).first()
            return test.ans_data.replace("\n","").replace('\r', '').replace('\xa0', '').split('!')
    except Exception as e:
        print(f"Помилка пошуку тем за предметом: {e}")
        return []

def find_test(id_):
    try:
        with Session() as session:
            test = session.query(Test).filter_by(id=id_).first()
            return test
    except Exception as e:
        print(f"Помилка пошуку тем за предметом: {e}")
        return []


# Припустимо, що у вас вже є екземпляр вашої сесії (session) і модель (Base).

def first_tema_test( tema_test_id):
    # Використовуйте вашу сесію і запит ORM для пошуку першого тесту з відповідним Tema_test_id.
    with Session() as session:
        first_test = session.query(Test).filter_by(tema_test_id=tema_test_id).first()
    return first_test







def add_test(num_quest, quest_img, quest_text, ans_data, vidpov, tema_test_id):
    try:
        with Session() as session:
            new_test = Test(
                num_quest=num_quest,
                quest_img=quest_img,
                quest_text=quest_text,
                ans_data=ans_data,
                vidpov=vidpov,
                tema_test_id=tema_test_id  # Set the tema_test_id attribute
            )
            session.add(new_test)
            session.commit()
    except Exception as e:
        print(f"Помилка додавання тесту: {e}")
def update_test(test_id, num_quest, quest_img, quest_text, ans_data, vidpov):
    try:
        with Session() as session:
            test = session.query(Test).get(test_id)
            test.num_quest = num_quest
            test.quest_img = quest_img
            test.quest_text = quest_text
            test.ans_data = ans_data
            test.vidpov = vidpov
            session.commit()
    except Exception as e:
        print(f"Помилка зміни тесту: {e}")


def update_by_id(class_, id_, update_data):
    """class_=Predmet Claass Tema_test Test"""
    try:
        with Session() as session:
            item = session.query(class_).filter_by(id=id_).first()
            if item:
                for key, value in update_data.items():
                    setattr(item, key, value)
                session.commit()
                return True
            else:
                return False
    except Exception as e:
        print(f"Помилка оновлення запису: {e}")
        return False
def delete_by_id(class_, id_):
    """class_=Predmet Claass Tema_test Test"""
    try:
        with Session() as session:
            item = session.query(class_).filter_by(id=id_).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            else:
                return False
    except Exception as e:
        print(f"Помилка видалення запису: {e}")
        return False
# Пошук Predmet за ID



"""***************************************************"""
def find_test( id_):
    """class_=Predmet Claass Tema_test Test"""
    try:
        with Session() as session:
            item = session.query(Test).filter_by(id=id_).first()
            if item:

                return item

    except Exception as e:
        print(f"Помилка пошуку тесту: {e}")
        return None
"""***************************************************"""



def find_by_id(class_, id_):
    """class_=(Predmet, Claass, Tema_, test Test)"""
    try:
        with Session() as session:
            item = session.query(class_).filter_by(id=id_).first()
            if item:
                if class_ == Predmet:
                    # Завантажити список класів при потребі
                    item.claass_list
                elif class_ == Claass:
                    # Завантажити список тем при потребі
                    item.tema_test_list
            return item
    except Exception as e:
        print(f"Помилка пошуку запису: {e}")
        return None

def get_all_items(class_):
    try:
        with Session() as session:
            items = session.query(class_).all()
            if class_ == Predmet:
                for item in items:
                    item.claass_list  # Завантажити список класів при потребі
            elif class_ == Claass:
                for item in items:
                    item.tema_test_list  # Завантажити список тем при потребі
            return items
    except Exception as e:
        print(f"Помилка отримання всіх записів: {e}")
        return []

"""************************************************************"""
def delete_tema_test_and_tests(tema_test_id):
    """Видаляє екземпляр Tema та всі тести з tema_test.id

    Args:
        tema_test_id: ID екземпляра Tema
    """

    with Session() as session:
        # Видаляємо всі тести з tema_test.id
        session.query(Test).filter_by(tema_test_id=tema_test_id).delete()

        # Видаляємо екземпляр Tema
        session.query(Tema_test).filter_by(id=tema_test_id).delete()

        # Підтверджуємо зміни
        session.commit()
        # print("Видалено",tema_test_id )
"""**************************тимчасові***************************"""
def update_test_num_quest(test_id, num_quest):
    try:
        with Session() as session:
            test = session.query(Test).get(test_id)
            test.num_quest = num_quest
            session.commit()
    except Exception as e:
        print(f"Помилка зміни тесту: {e}")
def find_last_test():
    try:
        with Session() as session:
            test = session.query(Test).order_by(Test.num_quest.desc()).first()
            return test
    except Exception as e:
        print(f"Помилка пошуку останнього тесту: {e}")
        return None
