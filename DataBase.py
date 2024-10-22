import math
import time
import re
import sqlite3
from flask import url_for




class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    
    #Работа с пользователем
    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM users WHERE email LIKE "{email}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким email уже существует')
                return False
            
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?)', (name, email, hpsw, 0, tm))
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
                print('Пользователь не найден getUser')
                return False
            
            return res
        except sqlite3.Error as e:
            print('Ошибка во входе пользователя getUser'+str(e))
            
        return False
    
    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE email = "{email}" LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден getUserByEmail')
                return False
            
            return res
        except sqlite3.Error as e:
            print('Ошибка во входе пользователя getUserByEmail'+str(e))

    #Работа с запросами
    def addRequest(self, user_id, friend_id, user_name):
        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM users WHERE id LIKE "{friend_id}"')
            res = self.__cur.fetchone()
            print(res)
            if res['count'] == 0:
                print('Пользователя с таким ID не существует')
                return False
            
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO requests VALUES(NULL, ?, ?, ?, ?)', (user_id, friend_id, user_name, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка создания инвайта addRequest'+str(e))
            return False
        
        return True
    
    def getRequest(self, user_id):
        try:
            self.__cur.execute(f'SELECT * FROM requests WHERE friend_id = "{user_id}"')
            res = self.__cur.fetchall()
            if not res:
                print('Запрос не найден getRequest')
                return False
            
            return res
        except sqlite3.Error as e:
            print('Ошибка в получении запроса getRequest'+str(e))
            
        return False
    
    def getRequestByID(self, request_id):
        try:
            self.__cur.execute(f'SELECT * FROM requests WHERE id = {request_id}')
            res = self.__cur.fetchone()
            if not res:
                print('Запрос не найден getRequestByID')
                return False
            
            return res
        except sqlite3.Error as e:
            print('Ошибка в получении запроса getRequestByID'+str(e))
            
        return False
    
    def delRequest(self, request_id):
        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM requests WHERE id = {request_id}')
            res = self.__cur.fetchone()
            if res['count'] == 0:
                print('Запроса с таким ID не существует')
                return False
            
            self.__cur.execute(f'DELETE FROM requests WHERE id = {request_id}')
            self.__db.commit()
            print(f'Запрос с ID: {request_id} успешно удален')
        except sqlite3.Error as e:
            print('Ошибка в удалении запроса'+str(e))
    
    #Работа с парами
    def addCouple(self, user1, user2, name1, name2):
        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM couples WHERE (user1 LIKE "{user1}" AND user2 LIKE "{user2}") OR (user1 LIKE "{user2}" AND user2 LIKE "{user1}")')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пара с таким набором ID пользователей уже существует')
                return False
            
            
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO couples VALUES(NULL, ?, ?, ?, ?, ?)', (user1, user2, name1, name2, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка создания пары'+str(e))
            return False
        
        return True
    
    def getCouple(self, user_id):
        try:
            self.__cur.execute(f'SELECT * FROM couples WHERE user1 LIKE "{user_id}" OR user2 LIKE "{user_id}"')
            res = self.__cur.fetchall()
            if not res:
                print('Пары с таким user_id не существует getCouple')
                return False
            
            return res
        except sqlite3.Error as e:
            print('Ошибка в getCouple'+str(e))
    
    def getCoupleByID(self, couple_id):
        try:
            self.__cur.execute(f'SELECT * FROM couples WHERE id = {couple_id}')
            res = self.__cur.fetchone()
            if not res:
                print('Пара не найдена getCoupleByID')
                return False
            
            return res
        except sqlite3.Error as e:
            print('Ошибка в получении пары getCoupleByID'+str(e))
    
    def delCouple(self, couple_id):
        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM couples WHERE id = {couple_id}')
            res = self.__cur.fetchone()
            if res['count'] == 0:
                print('Пары с таким ID не существует')
                return False
            
            self.__cur.execute(f'DELETE FROM couples WHERE id = {couple_id}')
            self.__db.commit()
            print(f'Пара с ID: {couple_id} успешно удалена')
        except sqlite3.Error as e:
            print('Ошибка в удалении пары'+str(e))