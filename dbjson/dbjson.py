from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from  sqlalchemy.orm import sessionmaker
import json
from typing import Any, Dict

__version__ = '1.0.0'

Base = declarative_base()

def jsony(data, many:bool=None):
    if many:
        jdata=[]
        for a in data:
            (a.__dict__).pop('_sa_instance_state')
            b = a.__dict__
            jdata.append(b)
        return json.dumps(jdata)
    else:
        (data.__dict__).pop('_sa_instance_state')
        return json.dumps(data.__dict__)

def sessionlocal(db):
    SQLALCHEMY_DATABASE_URI = f'{db}'

    engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread":False})

    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return SessionLocal()

class DBjson:
    """give database url like : DBjson('sqlite:///your.db')"""
    def __init__(self, app:str=None):
        self.app = app
        self.db = sessionlocal(self.app)

    def getall(self, dataclass):
        users = (self.db).query(dataclass).all()
        return jsony(users, many=True)

    def get(self, dataclass, data: Dict[str, Any]):
        if len(data) == 1:
            user = (self.db).query(dataclass).filter_by(**data).first()
            if user == None:
                res = {'status': False, 'data':'data not found'}
            else:
                return jsony(user)
        else:
            res = {"status": False, "data":"give only one key"}
        return json.dumps(res)

    def add(self, dataclass, data: Dict[str, Any]):
        try:
            user = dataclass(**data)
            (self.db).add(user)
            (self.db).commit()
            res = {'status': True, 'data':'data added successfully'}
        except TypeError as e:
            res = {'status': False, 'data':str(e)}
        return json.dumps(res)

    def addMany(self):
        pass

    def delete(self, dataclass, data: Dict[str, Any]):
        if len(data) == 1:
            user = (self.db).query(dataclass).filter_by(**data).first()
            if user == None:
                res = {'status': False, 'data':'data not found'}
            else:
                current_ssession  = (self.db).object_session(user)
                current_ssession.delete(user)
                current_ssession.commit()
                res = {'status': True, 'data':'data deleted successfully'}
        else:
            res = {"status": False, "data":"give only one key"}
        return json.dumps(res)

    def update(self, dataclass, data: Dict[str, Any]):
        # user = User.query.filter_by(sno=sno).first()
        # user.name = name
        # user.city = city
        # db.session.commit()
        # res = {'status': True, 'data':'data deleted successfully'}
        # return json.dumps(res)
        pass

    def search(self, dataclass, data: Dict[str, Any]):
        pass
