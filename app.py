import sqlite3
import os
import random as rn
from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, session
from DataBase import DataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin


#Конфигурация
DATABASE = '/tmp/app.py'
DEBUG = True
SECRET_KEY = 'fljahglahlvfdvln.n.xbvrea;ih3#5434343!'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'friends.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Войдите в аккаунт для доступа к закрытым страницам'

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)


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


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    
    return g.link_db


dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


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
@login_required
def game():
    activity = None
    if request.method == 'POST':
        activity = rn.choice(Activities)
    return render_template('game.html', title='Friends', activity=activity)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if len(request.form['username']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['password']) > 4:
            hash = generate_password_hash(request.form['password'])
            res = dbase.addUser(request.form['username'], request.form['email'], hash)
            if res:
                return redirect(url_for('login'))
            else:
                flash('Ошибка в регистрации', 'error')
        else:
            flash('Неверно заполнены поля', 'error')

    return render_template('register.html', title='Регистрация')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(url_for('profile'))
        
        flash('Неверная пара логин/пароль', 'error')
    
    return render_template('login.html', title='Авторизация')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта')
    return redirect(url_for('login'))


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    user_id = current_user.get_id()
    username = dbase.getUserName(user_id)
    email = dbase.getUserEmail(user_id)
    
    if request.method == 'POST':
        friend_id = request.form['friend_id']
        print('Friend-id', friend_id)
        if not friend_id == user_id:
            dbase.addRequest(user_id, friend_id)
            flash('Запрос другу отправлен', 'success')
        else:
            flash('Нельзя отправить запрос самому себе', 'error')
    
    return render_template('profile.html', username=username, email=email, user_id=user_id)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена')


if __name__ == '__main__':
    app.run(debug=True)