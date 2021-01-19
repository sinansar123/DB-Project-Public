from flask import current_app
import psycopg2
from flask_login import UserMixin


class AuthUser(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active


def get_user(username):
    with psycopg2.connect(dbname='findyourtone', user='postgres', password='qweqweqwe') as connection:
        cursor = connection.cursor()
        query = "SELECT username,password FROM users WHERE (username = %s)"
        try:
            cursor.execute(query, (username,))
            user_credentials = cursor.fetchone()
            ret_user = AuthUser(user_credentials[0], user_credentials[1])
            print("Returned persons username: {} Returned persons password: {}".format(
                ret_user.username, ret_user.password))

            return ret_user
        except:
            print('Error: User does not exist.')
            pass


#new_user = get_user('sinan')
"""
connection = psycopg2.connect(
    dbname='webapp', user='postgres', password='password')
cursor = connection.cursor()
query = "SELECT * FROM person WHERE (person_username = %s)"
cursor.execute(query, ('sinan',))
person_attributes = cursor.fetchone()
print('Username: {} Password: {}'.format(
    person_attributes[2], person_attributes[3]))
"""
