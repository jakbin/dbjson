from dbjson import DBjson, Base
from sqlalchemy import Column, Integer, String

class User(Base):
    '''set structure of database'''
    sno = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)

db = DBjson('sqlite:///test.db')

# insert data
add_data = {"name": "Jak","city": "india"}
print(db.add(User, add_data))

# read all data
print(db.getall(User))

# read single data
data = {"sno":1}
print(db.get(User, data))

# update data
update_data = {"sno":1,"name": "jak bin","city": "india"}
print(db.update(User, update_data, 'sno'))

# search data
search_data = {'name':'jak'}
print(db.search(User, search_data))

# delete data
delete_data = {"sno":1}
print(db.delete(User, delete_data))
