from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from  sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
import json
from typing import Any, Dict, List
from os.path import isfile

__version__ = '1.0.6'

class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

Base = declarative_base(cls=Base)

def dicty(data):
    if type(data) is list:
        jdata=[]
        for a in data:
            (a.__dict__).pop('_sa_instance_state')
            b = a.__dict__
            jdata.append(b)
        return jdata
    else:
        (data.__dict__).pop('_sa_instance_state')
        return data.__dict__

def sessionlocal(db):
    SQLALCHEMY_DATABASE_URI = f'{db}'

    engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread":False})

    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return SessionLocal()

def _include_sqlalchemy(obj):
    for module in sqlalchemy, sqlalchemy.orm:
        for key in module.__all__:
            if not hasattr(obj, key):
                setattr(obj, key, getattr(module, key))

class DBjson:
    """give database url like : DBjson('sqlite:///your.db')"""
    def __init__(self, app:str=None):
        self.app = app
        if isfile(self.app) != True:
            engine = create_engine(self.app, connect_args={"check_same_thread":False})
            Base.metadata.create_all(engine)
        self.db = sessionlocal(self.app)

        _include_sqlalchemy(self)

    @property    
    def Model(self):
        return Base

    def getall(self, dataclass):
        rdata = (self.db).query(dataclass).all()
        if rdata == []:
            res = {'status': False, 'data':'no data not found'}
        else:
            res = {'status': True, 'data':dicty(rdata)}
        return json.dumps(res)

    def get(self, dataclass, data: Dict[str, Any]):
        if len(data) == 1:
            try:
                rdata = (self.db).query(dataclass).filter_by(**data).first()
            except InvalidRequestError:
                key, _ = data.popitem()
                res = {'status': False, 'data':f"'{dataclass.__name__}' class has no attribute '{key}' "}
                return json.dumps(res)
            if rdata == None:
                res = {'status': False, 'data':'no data not found'}
            else:
                res = {'status': True, 'data':dicty(rdata)}
        else:
            res = {"status": False, "data":"give only one key"}
        return json.dumps(res)

    def add(self, dataclass, data: Dict[str, Any]):
        try:
            rdata = dataclass(**data)
            (self.db).add(rdata)
            (self.db).commit()
            res = {'status': True, 'data':'data added successfully'}
        except TypeError as e:
            res = {'status': False, 'data':str(e)}
        return json.dumps(res)

    def addMany(self, dataclass, data: List[Dict[str, Any]]):
        for d in data:
            try:
                rdata = dataclass(**d)
                (self.db).add(rdata)
                (self.db).commit()
            except TypeError as e:
                res = {'status': False, 'data':str(e)}
            else:
                res = {'status': True, 'data':'all data added successfully'}
        return json.dumps(res)


    def delete(self, dataclass, data: Dict[str, Any]):
        if len(data) == 1:
            try:
                rdata = (self.db).query(dataclass).filter_by(**data).first()
            except InvalidRequestError:
                key, _ = data.popitem()
                res = {'status': False, 'data':f"'{dataclass.__name__}' class has no attribute '{key}' "}
                return json.dumps(res)
            if rdata == None:
                _, value = data.popitem()
                res = {'status': False, 'data':f"no data found value '{value}' "}
            else:
                current_ssession  = (self.db).object_session(rdata)
                current_ssession.delete(rdata)
                current_ssession.commit()
                res = {'status': True, 'data':'data deleted successfully'}
        else:
            res = {"status": False, "data":"give only one key"}
        return json.dumps(res)

    def update(self, dataclass, data: Dict[str, Any], key: str):
        key_value = data.get(key)
        key1 = {key:key_value}
        rdata = (self.db).query(dataclass).filter_by(**key1).first()
        check_key = None
        for key, value in data.items():
            if hasattr(rdata, key):
                check_key = True
            else:
                res = {'status': False, 'data':f"'{dataclass.__name__}' class has no atrribute {key}"}
                return json.dumps(res)
        if check_key:
            for key, value in data.items():
                setattr(rdata, key, value)
        (self.db).commit()
        res = {'status': True, 'data':'data updated successfully'}
        return json.dumps(res)

    def search(self, dataclass, data: Dict[str, Any]):
        search = "%{0}%".format(list(data.values())[0])
        attr = (list(data)[0])
        search_attr = getattr(dataclass, attr)
        rdata =  (self.db).query(dataclass).filter(search_attr.like(search)).all()
        if rdata == []:
            res = {'status': False, 'data':'no data not found'}
        else:
            res = {"status": True, "data":dicty(rdata)}
        return json.dumps(res)
