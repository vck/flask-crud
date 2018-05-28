import sys
import sqlite3 as sql
import os
import hashlib

# schema database
# user table --> id, username, password
# post table --> id, title, body
# todo: 
# 1. add tagging 
# 2. add search
# 3. add admin 
# 4. add multiuser 


CREATE_USER_TABLE_QUERY = """CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                               username VARCHAR(20), 
                                               password VARCHAR(20))"""

CREATE_POST_TABLE_QUERY = """CREATE TABLE post(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                         title VARCHAR(200),
                                         body VARCHAR(1000))"""

INSERT_POST_QUERY = "INSERT INTO post(title, body) values (?, ?);"
INSERT_USER_QUERY = "INSERT INTO user(username, password) values (?, ?);"

FETCH_ALL_USERS = "SELECT * FROM user"
FETCH_ALL_POST = "SELECT * FROM post"
FETCH_POST_BY_ID = "SELECT * FROM post WHERE id='{}'"
DELETE_POST_BY_ID = "DELETE FROM post WHERE id='{}'"
SEARCH_POST = "SELECT * FROM post WHERE body like %?%"
DROP_TABLE_USER = "DROP TABLE IF EXISTS user"
DROP_TABLE_POST = "DROP TABLE IF EXISTS post"


class DatabaseHandler:

   def __init__(self, db_name):
      self.db_name = db_name 
      self.con = sql.connect(self.db_name)
      self.cur = self.con.cursor()
   
   def init(self):
      self.cur.execute(CREATE_USER_TABLE_QUERY)
      self.cur.execute(CREATE_POST_TABLE_QUERY)
      self.con.commit()   
  
 
   def drop_tables(self):
      self.cur.execute(DROP_TABLE_USER)
      self.cur.execute(DROP_TABLE_POST)


   def add_user(self, **kwargs):
      if 'username' and 'password' in kwargs:
         self.cur.execute(INSERT_USER_QUERY, (kwargs['username'], kwargs['password']))
         print('storing data')
         self.con.commit()
  
 
   def add_post(self, **kwargs):
      if 'title' and 'body' in kwargs:
         self.cur.execute(INSERT_POST_QUERY, (kwargs['title'], kwargs['body']))
         self.con.commit()


   def fetch_user(self):
      data = self.cur.execute(FETCH_ALL_USERS)
      return data

   
   def do_login(self, **kwargs):
      if 'username' and 'password' in kwargs:
         user = self.cur.execute(FETCH_SPESIFIED_USER, (kwargs['username'], kwargs['password']))
         if user:
            return True
         return False


   def fetch_post(self):
      data = self.cur.execute(FETCH_ALL_POST)
      return data


   def fetch_post_by_id(self, user_id):
      data = self.cur.execute(FETCH_POST_BY_ID.format(user_id))
      if data:
         return data

   
   def fetch_all_post(self):
      data = self.cur.execute(FETCH_POST)
      if data:
         return data      


   def search_post(self, query):
      data = self.cur.execute(SEARCH_POST, (query))
      if data:
         return data
   
   def delete_post(self, post_id):
      self.cur.execute(DELETE_POST_BY_ID.format(post_id))
      self.con.commit()
   

def test():
   db = DatabaseHandler('blog.db') 
   db.init()
   db.add_user(username='admin', password='admin123')
   db.add_post(title="python + flask is great!", body="python and flask is another awesome idea")
   
   users = db.fetch_user()
   for user in users:
      print(user)
   
   post_all = db.fetch_post()
   for post in post_all:
      print(post)

   post_by_id = db.fetch_post_by_id(1)
   print(post_by_id.fetchone())


if __name__ == "__main__":
   test() 
