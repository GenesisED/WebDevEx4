from flask import Flask, render_template, url_for, flash, redirect, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ABC54321'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rainblog.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"


class Post(db.Model):
    __tablename__ = 'post'
    __searchable__ = ['content']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

###The code below is for the first time creating the new database and adding new data.

#db.create_all()

#user_1 = User(username='Example name', email='example@gmail.com')
#db.session.add(user_1)
#db.session.commit()

#post_1 = Post(title='Example Title', content='Good example', user_id=1)
#db.session.add(post_1)
#db.session.commit()


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def sigup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('signup.html', title='signup', form=form)


@app.route('/post')
def post():
    posts = Post.query.all()
    return render_template('post.html', title='post', posts=posts)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        term = request.form['search_term']
        if term == "":
            flash("Enter a name to search for")
            return redirect('/')
        results = Post.query.filter(Post.content.contains(term)).all()
        if not results:
            flash("No students found with that name.")
            return redirect('/')
        return render_template('search.html', results=results)
    else:
        return redirect(url_for('home'))



if __name__ == '__main__':
    app.run()
