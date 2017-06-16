# Microservice for Search Index of Phone Numbers

This project helps to normalize telephone numbers in the database.

## Installation

Edit dev.env and sqlalchemy.url in alembic.ini with your db connection details.
```
$ pip install -r requirements.txt
$ . dev.env
```

## Usage

##### Add column in db for normalized phone numbers
```
$ alembic upgrade head
```
##### Normalize phone numbers
```
$ python format_phones_in_db.py
```

## Requirements

- Python >= 3.5

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
