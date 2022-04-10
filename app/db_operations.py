from models import *
from sqlalchemy.orm import Session


def add_data(table_name, data_obj):
    with Session(engine) as session:
        session.begin()
        try:
            session.add(data_obj)
        except Exception as e:
            print(e)
            session.rollback()
            raise
        else:
            session.commit()

def get_data(table_name, condition=None):

    with Session(engine) as session:
        if condition:
            data = session.query(table_name).filter_by(condition).all()
        else:
            data = session.query(table_name).all()
    data = [row.__dict__ for row in data]
    for row in data:
        del row['_sa_instance_state']
    return data

def update_data(table_name, data_object, filter_value):
    with Session(engine) as session:
        try:
            session.query(table_name).filter_by(id=filter_value).update(data_object)
            session.commit()
        except Exception as e:
            print(e)

def delete_data(table_name,filter_value):
    with Session(engine) as session:
        session.begin()
        try:
            session.query(table_name).filter_by(id=filter_value).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise

# if __name__ == "__main__":
#     from models import Continent, Country, City
#     data = get_data(table_name=Continent)
#     # data[0]['population'] = 1001
#     # update_data(table_name=Continent, data_object={Continent.population: 2001}, filter_value=1)
#     # data = get_data(table_name=Continent)
#     data2 = Continent(name='North America', population=2, area=102.5)
#     add_data(table_name=Continent, data_obj=data2)
#     data = get_data(table_name=Continent)
#     delete_data(Continent, filter_value=1)
#     data = get_data(table_name=Continent)
#     print(data)