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
data = {"sno":1}
print(a.get(User, data))

# update data
update_data = {"sno":1,"name": "jak bin","city": "india"}
print(a.update(User, update_data, 'sno'))

# search data
search_data = {'name':'jak'}
print(a.search(User, search_data))

# delete data
delete_data = {"sno":1}
print(a.delete(User, delete_data))
