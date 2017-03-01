import re
from os import getenv

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = automap_base()
engine = create_engine(getenv('DB_URI'))
Base.prepare(engine, reflect=True)
Orders = Base.classes.orders
session = Session(engine)


def format_phone_number(number, region='RU'):
    # returns a number in the format: 9291112233
    _number = ''.join(re.findall(r'\d+', number))
    return _number[1:] if len(_number) == 11 else _number


def format_phones_in_db(flag=False):
    orders = session.query(Orders).all()
    for order in orders:
        phone = format_phone_number(order.contact_phone)
        order.contact_phone_formatted = phone
    session.commit()


def run_db_query(func, attempts=2):
    while attempts > 0:
        attempts -= 1
        try:
            return func()
        except sqlalchemy.exc.DBAPIError as exc:
            if attempts and exc.connection_invalidated:
                session.rollback()
            else:
                raise


if __name__ == '__main__':
    run_db_query(format_phones_in_db)
