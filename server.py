from flask import (
   Flask,
   render_template,
   redirect,
   request,
   url_for
)

from db import DatabaseHandler

app = Flask("appname")
app.config["DB_NAME"] = "blog.db"
db = DatabaseHandler(app.config["DB_NAME"])


@app.route("/login", methods=["GET", "POST"])
def login():
   if request.method == "POST":
      username = request.form['username']
      password = request.form['password']
      if db.do_login(username=username, password=password):
         return render_template('index.html', username=username, password=password)
      

@app.route("/register", methods=["GET", "POST"])
def register():
   pass


@app.route("/post/<int:id>")
def view_post(id):
   if id:
      post = db.fetch_post_by_id(int(id))
      post = post.fetchone()
      return render_template('show.html', post=post)


@app.route('/post')
def show_post():
   post = db.fetch_post().fetchall()
   if post:
      return render_template('post.html', all_post=post)
   return render_template('post.html')


@app.route('/add', methods=['POST', 'GET'])
def add_post():
   if request.method == "POST":
      title = request.form['title']
      body = request.form['body']
      db.add_post(title=title, body=body)
      return redirect(url_for('show_post'))
   return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
   if post_id:
      if request.method == "POST":
         db.delete_post(post_id)
         return redirect(url_for('show_post'))


@app.route('/')
def index_page(): 
   post = db.fetch_post().fetchall()
   if post:
      return render_template('index.html', post=post)
   return render_template('index.html')


if __name__ == "__main__":
   app.run(port=8080)
