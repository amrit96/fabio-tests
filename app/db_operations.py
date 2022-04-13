from models import *
from sqlalchemy.orm import Session
from tasks import app


@app.task
def add_data(data_obj):
    """
    this method will be used to insert new data tot the db
    Args:
        data_obj: object of the orm class

    Returns:

    """
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


@app.task
def get_data(table_name, filter_key=None, filter_value=None):
    """
    this method will be used to fetch data of a particular table from the db
    Args:
        table_name: name of the table from which data is to be fetched
        filter_key: name of the column against which the filtering is to be done
        filter_value: value of the filtering column

    Returns:
        a list of dictionary where each dictionary represents a row
    """
    with Session(engine) as session:
        if filter_key:
            data = session.query(table_name).filter(getattr(table_name, filter_key).like(filter_value)).all()
        else:
            data = session.query(table_name).all()
    data = [row.__dict__ for row in data]
    for row in data:
        del row['_sa_instance_state']
    return data


@app.task
def update_data(table_name, data_object, id_value):
    """
    this method will be used to update an existing record
    Args:
        table_name: name of the table in which the data is to be updated
        data_object: a dict containing the key value pair(s) of th updated data
        id_value: the primary key (id) of the row where the data is to be altered

    Returns:

    """
    with Session(engine) as session:
        try:
            session.query(table_name).filter_by(id=id_value).update(data_object)
            session.commit()
        except Exception as e:
            print(e)


@app.task
def delete_data(table_name, id_value):
    """
    this method will me used to remove data from db table
    Args:
        table_name: name of the table from where data is to be removed
        id_value: the primary key (id) of the row which is to be removed

    Returns:

    """
    with Session(engine) as session:
        session.begin()
        try:
            session.query(table_name).filter_by(id=id_value).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise


# if __name__ == "__main__":
    # from models import Continent, Country, City
    # data = get_data(table_name=Continent)#, filter_key='population',filter_value=2)
    #     # data[0]['population'] = 1001
    # update_data(table_name=Continent, data_object={Continent.population: 2001}, filter_value=1)
    # data = get_data(table_name=Continent)
    #     data2 = Continent(name='North America', population=2, area=102.5)
    #     add_data(table_name=Continent, data_obj=data2)
    #     data = get_data(table_name=Continent)
    # delete_data(Continent, filter_value=2)
    #     data = get_data(table_name=Continent)
    # print(data)
