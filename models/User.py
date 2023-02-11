from peewee import CharField, ForeignKeyField

from models.BaseModels import BaseModel, BaseModelNoSoftDelete


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()

    def __str__(self):
        return f"ID: {self.id}, Username: {self.username}, password: {self.password}"


class Role(BaseModelNoSoftDelete):
    is_deleted = None
    name = CharField()

    def delete(self):
        return super().delete()


class UserRole(BaseModel):
    user = ForeignKeyField(User, backref='roles')
    role = ForeignKeyField(Role)
