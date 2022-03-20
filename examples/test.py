from dbjson import DBjson, Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'user'
    '''set structure of database'''
    sno = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)

a = DBjson('db_url') # example url = 'sqlite:///your.db'

# insert data
add_data = {"name": "Jak","city": "india"}
print(a.add(User, add_data))

# read all data
print(a.getall(User))

# read single data
data = {"sno":2}
print(a.get(User, data))

# delete data
delete_data = {"sno":6}
print(a.delete(User, delete_data))
