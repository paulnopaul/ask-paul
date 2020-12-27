#! /bin/bash
rm -rf app/migrations app/__pycache__/ ask_paul/__pycache db.sqlite3;
psql -c 'drop database if exists ASKME;' -u 'cheklin';
psql -c 'create database ASKME;' -u 'cheklin';
python3 manage.py makemigrations app;
python3 manage.py migrate;
python3 manage.py fill_db --users 10000 --questions 1000 --answers 10000 --tags 100 --qlikes 100000 --alikes 100000
