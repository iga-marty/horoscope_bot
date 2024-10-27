from peewee import Model, IntegerField, TextField, SqliteDatabase
from playhouse.shortcuts import model_to_dict

db = SqliteDatabase('db2.sqlite')


class User(Model):
    user_id = IntegerField(primary_key=True)
    zodiac_sign = TextField(default='')

    # for update
    horoscope_number = IntegerField(default=0)
    last_message_id = IntegerField(default=0)

    class Meta:
        table_name = 'User'
        database = db


cursor = db.cursor()
User.create_table()


def create_user(chat_id):
    user, creation_status = User.get_or_create(user_id=chat_id)
    return creation_status


def change_sign(chat_id, new_sign):
    User.update({User.zodiac_sign: new_sign}).where(User.user_id == chat_id).execute()


def get_sign(chat_id):
    return model_to_dict(User.get(User.user_id == chat_id))['zodiac_sign']


def change_number(chat_id, horoscope_number):
    if horoscope_number == 3:
        horoscope_number = 0
    else:
        horoscope_number += 1
    User.update({User.horoscope_number: horoscope_number}).where(User.user_id == chat_id).execute()


def get_number(chat_id):
    horoscope_number = model_to_dict(User.get(User.user_id == chat_id))['horoscope_number']
    return horoscope_number


def change_last_message_id(chat_id, new_message_id):
    User.update({User.last_message_id: new_message_id}).where(User.user_id == chat_id).execute()


def get_last_message_id(chat_id):
    return model_to_dict(User.get(User.user_id == chat_id))['last_message_id']


def print_all_table():
    query = User.select()
    for user_data in query:
        print(model_to_dict(user_data))
    print()


db.close()
