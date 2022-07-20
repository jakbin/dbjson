from dbjson import DBjson

db = DBjson('sqlite:///test.db')

class User(db.Model):
    '''set structure of database'''
    sno = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String)
    city = db.Column(db.String)

# insert data
add_data = {"name": "Jak","city": "india"}
print(db.add(User, add_data))

# insert multiple data
addMany_data = [{"name": "Jaky","city": "india"},{"name": "Jak bin","city": "india"}]
print(db.add_many(User, addMany_data))

# read all data
print(db.get_all(User))

# read single data
data = {"sno":1}
print(db.get(User, data))

# update data
update_data = {"sno":2,"name": "jak bin","city": "india"}
print(db.update(User, update_data, 'sno'))

# search data
search_data = {'name':'jak'}
print(db.search(User, search_data))

# delete data
delete_data = {"sno":1}
print(db.delete(User, delete_data))
