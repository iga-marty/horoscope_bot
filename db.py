from peewee import Model, IntegerField, TextField, SqliteDatabase
from playhouse.shortcuts import model_to_dict


db = SqliteDatabase('db.sqlite')


class User(Model):
    user_id = IntegerField(primary_key=True)
    zodiac_sign = TextField(default='')

    class Meta:
        table_name = 'User'
        database = db


# class Horoscope(Model):
#     zodiac_sign = TextField(primary_key=True)
#     today_horoscope = TextField(default='')
#
#     class Meta:
#         table_name = 'Horoscope'
#         database = db


cursor = db.cursor()
User.create_table()
# Horoscope.create_table()


def create_user(chat_id):
    user, creation_status = User.get_or_create(user_id=chat_id)
    return creation_status


def change_sign(chat_id, new_sign):
    User.update({User.zodiac_sign: new_sign}).where(User.user_id == chat_id).execute()


# def create_horoscope_data(horoscope: dict):
#     try:

# def wallet_in_database(chat_id):
#     return False if model_to_dict(User.get(User.user_id == chat_id))['wallet_number'] == '' else True


def get_wallet_number(chat_id):
    wallet_number = model_to_dict(User.get(User.user_id == chat_id))['wallet_number']
    return wallet_number if wallet_number != '' else None


def get_notifier_status(chat_id):
    return model_to_dict(User.get(User.user_id == chat_id))['status']


def get_transaction_id(chat_id):
    return model_to_dict(User.get(User.user_id == chat_id))['transaction_id']


def get_date_of_last_claim(chat_id):
    return model_to_dict(User.get(User.user_id == chat_id))['date_of_last_claim']


def change_wallet_number(chat_id, new_wallet_number):
    User.update(
        {User.wallet_number: new_wallet_number}
    ).where(
        User.user_id == chat_id
    ).execute()


def change_notifier_status(chat_id):
    if get_notifier_status(chat_id) == 1:
        new_status = 0
    else:
        new_status = 1

    User.update(
        {User.status: new_status}
    ).where(User.user_id == chat_id).execute()


def change_transaction_id(chat_id, new_transaction_id):
    User.update(
        {User.transaction_id: new_transaction_id}
    ).where(
        User.user_id == chat_id
    ).execute()


def change_last_claim_date(chat_id, new_date_of_last_claim):
    User.update(
        {User.date_of_last_claim: new_date_of_last_claim}
    ).where(
        User.user_id == chat_id
    ).execute()


def change_dm_status(chat_id, new_dm_status):
    if new_dm_status:
        new_dm_status = 1
    else:
        new_dm_status = 0

    User.update(
        {User.dm_status: new_dm_status}
    ).where(
        User.user_id == chat_id
    ).execute()


def print_all_table():
    query = User.select()
    for user_data in query:
        print(model_to_dict(user_data))
    print()


db.close()
