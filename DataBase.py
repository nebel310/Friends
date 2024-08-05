import math
import time
import re
import sqlite3
from flask import url_for




class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    
    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM users WHERE email LIKE "{email}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким email уже существует')
                return False
            
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?, ?)', (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления пользователя в БД'+str(e))
            return False
        
        return True
    
    def getUser(self, user_id):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE id = {user_id} LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            
            return res
        except sqlite3.Error as e:
            print('Ошибка во входе пользователя'+str(e))
            
        return False
    
    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE email = "{email}" LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            
            return res
        except sqlite3.Error as e:
            print('Ошибка во входе пользователя'+str(e))
    
    def getUserName(self, user_id):
        try:
            user = self.getUser(user_id)
            if user:
                return user['name']
            return None
        except sqlite3.Error as e:
            print('Ошибка в функции getUserName'+str(e))
    
    def getUserEmail(self, user_id):
        user = self.getUser(user_id)
        if user:
            return user['email']
        return None

    def addRequest(self, user_id, friend_id):
        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM users WHERE id LIKE "{friend_id}"')
            res = self.__cur.fetchone()
            if res['count'] == 0:
                print('Пользователя с таким ID не существует')
                return False
            
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO requests VALUES(NULL, ?, ?, ?)', (user_id, friend_id, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка создания инвайта'+str(e))
            return False
        
        return True