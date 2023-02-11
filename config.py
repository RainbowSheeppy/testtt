from peewee import SqliteDatabase


class ConfigClass(object):
    SECRET_KEY = '53CR3D'
    DATABASE = SqliteDatabase('people.db')
