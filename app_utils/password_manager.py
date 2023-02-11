import bcrypt

from models.User import User


def hash_password(raw_password):
    hashed_password = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password


def check_password(user: User, raw_password):
    if bcrypt.checkpw(raw_password.encode("utf-8"), user.password.encode("utf-8")):
        return True
    return False
