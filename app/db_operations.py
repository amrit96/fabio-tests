from models import *
from sqlalchemy.orm import Session


def add_data(data_obj):
    with Session(engine) as session:
        session.begin()
        try:
            session.add(data_obj)
        except:
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
    return data

def update_data(table_name, data_object, condition):
    with Session(engine) as session:
        session.query(table_name).filter(condition).update(data_object, synchronize_session="fetch")

def delete_data(data_obj):
    with Session(engine) as session:
        session.begin()
        try:
            session.delete(data_obj)
        except:
            session.rollback()
            raise
