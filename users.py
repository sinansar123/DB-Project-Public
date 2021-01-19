from flask_login import UserMixin


class User():
    def __init__(self, name, username, password, location, about, genre, category=0,reg_date=None, id=None):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.location = location
        self.about = about
        self.genre = genre
        self.category = category
        self.reg_date = reg_date

