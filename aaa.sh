#! /bin/bash
rm -rf app/migrations app/__pycache__/ ask_paul/__pycache db.sqlite3;
python3 manage.py makemigrations app;
python3 manage.py migrate;
python3 manage.py fill_db --users 100 --questions 10000 --tags 100 --qlikes 10000 --alikes 10000
