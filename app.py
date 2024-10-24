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


@app.route('/')
def index():
    return render_template('index.html', title='Вход')


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
    user_name = dbase.getUser(user_id)[1]
    email = dbase.getUser(user_id)[2]
    
    if request.method == 'POST':
        if 'create_request' in request.form:
            friend_id = request.form.get('friend_id')
            if not friend_id == user_id:
                dbase.addRequest(user_id, friend_id, user_name)
                flash('Запрос другу отправлен', 'success')
            else:
                flash('Нельзя отправить запрос самому себе', 'error')
        
        elif 'request_interract' in request.form:
            request_interract = request.form.get('request_interract')
            interract_type, request_id = request_interract.split('_')
            request_id = int(request_id)

            if interract_type == 'accept':
                if dbase.getRequestByID(request_id) != False:
                    user1 = dbase.getRequestByID(request_id)[1]
                    user2 = dbase.getRequestByID(request_id)[2]
                    name1 = list(dbase.getUser(user1))[1]
                    name2 = list(dbase.getUser(user2))[1]

                    dbase.addCouple(user1, user2, name1, name2)
                    dbase.delRequest(request_id)
            elif interract_type == 'decline':
                dbase.delRequest(request_id)
        
        elif 'couple_interract' in request.form:
            couple_interract = request.form.get('couple_interract')
            interract_type, couple_id = couple_interract.split('_')
            couple_id = int(couple_id)

            if interract_type == 'play':
                if dbase.getCoupleByID(couple_id) != False:
                    return redirect(url_for('game', couple_id=couple_id))
            elif interract_type == 'delete':
                dbase.delCouple(couple_id)

   
    requests = dbase.getRequest(user_id)
    couples = dbase.getCouple(user_id)
    
    return render_template('profile.html', username=user_name, email=email, user_id=user_id, requests=requests, couples=couples)


@app.route('/game/<int:couple_id>', methods=['GET', 'POST'])
@login_required
def game(couple_id):
    user_id = current_user.get_id()
    user1 = dbase.getCoupleByID(couple_id)[1]
    user2 = dbase.getCoupleByID(couple_id)[2]

    task_to1 = dbase.getCoupleByID(couple_id)[5]
    task_to2 = dbase.getCoupleByID(couple_id)[6]
    print(f'task_to1: {task_to1} task_to2: {task_to2}')
    
    #Логика если текущий юзер - user1
    if user_id == user1:
        current_task = dbase.getCoupleByID(couple_id)[5]
        if request.method == 'POST':
            if 'done' in request.form:
                dbase.updateCouple(couple_id, 'Заданий нет', task_to2)
                return redirect(url_for('game', couple_id=couple_id))
            
            elif 'send' in request.form:
                task_to2 = request.form['textarea']
                dbase.updateCouple(couple_id, task_to1, task_to2)
                return redirect(url_for('game', couple_id=couple_id))
    
    #Лоигка если текущий юзер - user2
    elif user_id == user2:
        current_task = dbase.getCoupleByID(couple_id)[6]
        if request.method == 'POST':
            if 'done' in request.form:
                dbase.updateCouple(couple_id, task_to1, "Заданий нет")
                return redirect(url_for('game', couple_id=couple_id))
            
            elif 'send' in request.form:
                task_to1 = request.form['textarea']
                dbase.updateCouple(couple_id, task_to1, task_to2)
                return redirect(url_for('game', couple_id=couple_id))
    else:
        return redirect(url_for('profile'))


    couple = dbase.getCoupleByID(couple_id)
    return render_template('game.html', title='Friends', couple=couple, current_task=current_task)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена')


if __name__ == '__main__':
    create_db() #Временное решение для ускорения разработки
    app.run(debug=True)
