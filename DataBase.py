import math
import time
import re
import sqlite3
from flask import url_for




class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()