import psycopg2
from src.hh_vacancy_parser import VacancyParsing
from src.db_module import DbModule
from config import config


def user_interaction(value, db_name):
    """
    Взаимодействия с пользователем, получает данные от пользователя, записывает в базу даннных
    и сортирует.
    :return: None
    """
    VacancyParsing(value)
    module = DbModule(db_name)
    module.create_tables()
    module.fill_tables(value)


def delete_database(db_name):
    """
    Удаление базы данных
    """
    conn = psycopg2.connect(dbname='postgres', **config())
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f'DROP DATABASE {db_name}')
    cursor.close()
    conn.close()


def create_database(db_name):
    """
    Создание базы данных и таблиц для сохранения данных о каналах и видео
    """
    conn = psycopg2.connect(dbname='postgres', **config())
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cursor.execute(f'CREATE DATABASE {db_name}')
    cursor.close()
    conn.close()
