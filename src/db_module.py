import psycopg2
from src.hh_vacancy_parser import VacancyParsing
from config import config


class DbModule:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = psycopg2.connect(dbname=self.db_name, **config())

    def create_tables(self):
        """
        Создание таблиц employer и vacancies
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    'CREATE TABLE employer('
                    'employer_id int PRIMARY KEY,'
                    'employer_name varchar(150));'

                    'CREATE TABLE vacancies('
                    'vacancy_id int PRIMARY KEY,'
                    'company_id int REFERENCES employer(employer_id),'
                    'vacancy_name varchar(250) NOT NULL,'
                    'salary_from int,'
                    'salary_to int,'
                    'url varchar(250));'
                )

    def fill_tables(self, value):
        """
        Заполнение таблиц
        """
        head_hunter = VacancyParsing(value)
        employers = head_hunter.get_employers_sort()
        vacancies = head_hunter.filter_vacancies()
        with self.conn:
            with self.conn.cursor() as cursor:
                for employer in employers:
                    cursor.execute(
                        """
                            INSERT INTO employer VALUES (%s, %s)
                            """, (employer["id"], employer["name"])
                    )

                for vacancy in vacancies:
                    cursor.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                                   (vacancy["id"], vacancy["employer"], vacancy["name"], vacancy["salary_from"],
                                    vacancy["salary_to"], vacancy["url"],))
