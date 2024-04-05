import psycopg2
from config import config


class DbManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = psycopg2.connect(dbname=self.db_name, **config())

    def get_companies_and_vacancies_count(self):
        """
        Метод для получения списка всех компаний и количество вакансий у каждой компании
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute('select distinct employer_name, count(vacancy_name) vacancy_count '
                               'from vacancies '
                               'join employer '
                               'on employer.employer_id=vacancies.company_id '
                               'group by employer_name '
                               'order by count(vacancy_name) desc')
                data = cursor.fetchall()
                print(data)

    def get_all_vacancies(self):
        """
        Метод для получения списка всех вакансий с указанием названия компании, названия вакансии, зарплаты
        и ссылки на вакансию
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute('select employer_name, vacancy_name, salary_from, salary_to, url '
                               'from vacancies '
                               'join employer on employer.employer_id=vacancies.company_id '
                               'order by employer_name')
                data = cursor.fetchall()
                print(data)

    def get_avg_salary(self):
        """
        Метод для получения средней зарплаты по вакансиям
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute('select vacancy_name, avg(salary_from) as avg_salary '
                               'from vacancies '
                               'group by vacancy_name')
                data = cursor.fetchall()
                print(data)

    def get_vacancies_with_higher_salary(self):
        """
        Метод для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute('select vacancy_name, avg(salary_from) avg_salary '
                               'from vacancies '
                               'where salary_from > (select avg(salary_from) as avg_salary '
                               'from vacancies) '
                               'group by vacancy_name '
                               'order by avg(salary_from)')
                data = cursor.fetchall()
                print(data)

    def get_vacancies_with_keyword(self, keyword):
        """
        Метод для получения списка всех вакансий, в названии которых содержатся переданные в метод слова, например python
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(f"select * from vacancies where vacancy_name like '%{keyword}%'")
                data = cursor.fetchall()
                print(data)
