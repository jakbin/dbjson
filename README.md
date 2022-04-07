# DBjson

crud operation with database using json.

 [![PyPI version](https://badge.fury.io/py/dbjsonpy.svg)](https://pypi.org/project/dbjsonpy/)
 [![Downloads](https://pepy.tech/badge/dbjsonpy/month)](https://pepy.tech/project/dbjsonpy)
 [![Downloads](https://static.pepy.tech/personalized-badge/dbjsonpy?period=total&units=international_system&left_color=green&right_color=blue&left_text=Total%20Downloads)](https://pepy.tech/project/dbjsonpy)

## Features 

 * create data.
 * read data.
 * delete data
 * update data
 * search data

## Install 
```python
pip install dbjsonpy
```
### Example

minimal example
```python
from dbjson import DBjson

db = DBjson('sqlite:///test.db')

class User(db.Model):
    name = db.Column(db.String)

# insert data
add_data = {"name": "Jak","city": "india"}
print(db.add(User, add_data))

# read all data
print(db.getall(User))
```

see full example [here](examples/test.py)

## Todo

 - [x] update data
 - [x] add multiple data
 - [x] search data
 - [ ] paginate data
