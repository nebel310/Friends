import sqlite3
import os
import random as rn
from flask import Flask, render_template, request, session, abort



#Конфигурация
DATABASE = 'tmp/friends.db'
DEBUG = True
SECRET_KEY = 'djf^*#gbjkhd/fbg545jdf$!@ghO;b;9354m,64$$'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'friends.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


Activities = [
    "погладить кошку",
    "помыть посуду",
    "почитать книгу",
    "прогуляться в парке",
    "позаниматься спортом",
    "приготовить ужин",
    "смотреть фильм",
    "поиграть в настольную игру",
    "позвонить другу",
    "сходить в магазин",
    "написать письмо",
    "порисовать",
    "послушать музыку",
    "выпить кофе в кафе",
    "посетить музей",
    "поучаствовать в волонтерской деятельности",
    "посадить растение",
    "убраться в квартире",
    "выучить новое слово",
    "попробовать медитацию"
]


@app.route('/')
def index():
    return render_template('index.html', title='Вход')


@app.route('/game', methods=['GET', 'POST'])
def game():
    activity = None
    if request.method == 'POST':
        activity = rn.choice(Activities)
    return render_template('game.html', title='Friends', activity=activity)


@app.route('/register')
def register():
    return render_template('register.html', title='Регистрация')


@app.route('/login', methods=['POST', 'GET'])
def login():   
    return render_template('login.html', title='Авторизация')


@app.route('/profile/<username>')
def profile(username):
    session['userLogged'] = 'adm'
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    
    return render_template('profile.html', username=username, email='adm@adm.com')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена')


if __name__ == '__main__':
    app.run(debug=True)