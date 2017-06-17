import re
from os import getenv
from time import sleep

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from config import DB_CHECK_INTERVAL

base = automap_base()
engine = create_engine(getenv('DB_URI'))
base.prepare(engine, reflect=True)
orders = base.classes.orders
session = Session(engine)


def format_phone_number(number):
    # returns a number in the format: 9291112233
    _number = ''.join(re.findall(r'\d+', number))
    return _number[1:] if len(_number) == 11 else _number


def format_phones_in_db(query):
    for order in query.yield_per(100):
        phone = format_phone_number(order.contact_phone)
        order.contact_phone_formatted = phone
    session.commit()


def run_db_query(func, *args, attempts=2):
    for _ in range(attempts):
        try:
            return func(*args)
        except sqlalchemy.exc.DBAPIError as exc:
            if attempts and exc.connection_invalidated:
                session.rollback()
            else:
                raise


if __name__ == '__main__':
    run_db_query(format_phones_in_db, session.query(orders))
    while True:
        sleep(int(DB_CHECK_INTERVAL))
        query = session.query(orders).filter(orders.contact_phone_formatted == None)
        run_db_query(format_phones_in_db, query)
