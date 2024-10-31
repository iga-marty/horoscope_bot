from peewee import Model, IntegerField, TextField, SqliteDatabase
from playhouse.shortcuts import model_to_dict

db = SqliteDatabase('db.sqlite')


class User(Model):
    user_id = IntegerField(primary_key=True)
    zodiac_sign = TextField(default='')

    # for update
    horoscope_number = IntegerField(default=0)
    last_message_id = IntegerField(default=0)

    class Meta:
        table_name = 'User'
        database = db


class Messages(Model):
    message_id = IntegerField(primary_key=True)
    chat_id = IntegerField()

    class Meta:
        table_name = 'Messages'
        database = db


class Horoscopes(Model):
    sign = TextField(primary_key=True)
    horoscope_0 = TextField()
    horoscope_1 = TextField()
    horoscope_2 = TextField()
    horoscope_3 = TextField()

    class Meta:
        table_name = 'Horoscopes'
        database = db


cursor = db.cursor()
User.create_table()
Messages.create_table()
Horoscopes.create_table()


def create_user(chat_id) -> bool:
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


def add_message(message_id, chat_id):
    Messages.get_or_create(message_id=message_id, chat_id=chat_id)


def get_messages(chat_id) -> list:
    query = Messages.select().where(Messages.chat_id == chat_id)
    messages = [row['message_id'] for row in query.dicts()]
    return messages


def delete_user_messages(chat_id):
    query = Messages.delete().where(Messages.chat_id == chat_id)
    query.execute()
    add_message(get_last_message_id(chat_id), chat_id)


def get_data_for_notifications() -> dict:
    query = User.select().where(User.zodiac_sign != '').dicts()
    answer = {row['user_id']: row['zodiac_sign'] for row in query}
    return answer


def create_or_update_horo_base(horoscopes: dict):
    for key, value in horoscopes.items():
        Horoscopes.insert(sign=key, horoscope_0=value[0], horoscope_1=value[1], horoscope_2=value[2],
                          horoscope_3=value[3]).on_conflict('replace').execute()


def get_horoscope(sign, number):
    return model_to_dict(Horoscopes.get_by_id(sign))[f'horoscope_{number}']


def print_all_table():
    query = User.select()
    for user_data in query:
        print(model_to_dict(user_data))
    print()
    query = Messages.select()
    for user_data in query:
        print(model_to_dict(user_data))
    print()
    query = Horoscopes.select()
    for user_data in query:
        print(model_to_dict(user_data))
    print()


db.close()
