from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR   # MySQLのテーブルを作る時に必要


app = Flask(__name__)


# MySQLに接続するための情報
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
    'user': "root",
    'password': "rootpassword",
    'host': "localhost",
    'db_name': "sample_db"
})

# おまじない
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# dbの初期化
db = SQLAlchemy(app)


##  by SQL lite ##
#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
#db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)


# テーブル作成
db.create_all()


# ルートページ作成
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts)

    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')

        due = datetime.strptime(due, '%Y-%m-%d')
        new_post = Post(title=title, detail=detail, due=due)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')


# 作成
@app.route('/create')
def create():
    return render_template('create.html')


# 詳細
@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)

    return render_template('detail.html', post=post)


# 削除
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
