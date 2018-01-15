from flask import Flask, request, redirect, render_template, sessions, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:helloworld@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'thekeytomythoughts'

class Blogs(db.Model):
 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique =True)
    body = db.Column(db.Text)
    time_stamp = db.Column(db.DateTime)
 
    def __init__(self, title, body, time_stamp=None):
        self.title = title
        self.body = body
        if time_stamp is None:
            time_stamp = datetime.utcnow()
        self.time_stamp = time_stamp
 
    def validation(self):
        if self.title and self.body and self.time_stamp:
            return True
        else:
            return False

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        new_blog = Blogs(new_title, new_body)
 
        if new_blog.validation():
            db.session.add(new_blog)
            db.session.commit()
 
            new_id = "/blog?id=" + str(new_blog.id) 
            return redirect('/blog')
        else:
            flash('You must enter something in every field', 'error')
            return render_template('newpost.html', title = "Newpost", new_title=new_title, new_body=new_body)
 
    else:
        return render_template('newpost.html', title = "Newpost")

@app.route('/blog', methods=['POST', 'GET'])
def blog():
 
    blog_id = request.args.get('id')
    if blog_id:
        blog = Blogs.query.get(blog_id)
        return render_template('blog.html', title="Blog", blog=blog)
 
    else:
        all_blogs = Blogs.query.order_by(Blogs.time_stamp.desc()).all()
        return render_template('index.html', title="Main Page", all_blogs=all_blogs)
 
if __name__ == '__main__':
    app.run()