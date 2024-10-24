import psycopg2

from src.api import HH
from src.objects import Employer


class DBManager:
    """Postgres database connector"""

    __host: str
    __database: str
    __user: str
    __password: str

    def __init__(self, host: str, database: str, user: str, password: str):
        if (
            not isinstance(host, str)
            or not isinstance(database, str)
            or not isinstance(user, str)
            or not isinstance(password, str)
        ):
            raise TypeError("Invalid DBManager init")

        self.__host = host
        self.__database = database
        self.__user = user
        self.__password = password

        self.create()

    def __exec(self, *args, **kwargs) -> list[tuple] | None:
        """Provides query (private for security reasons)"""
        with psycopg2.connect(
            host=self.__host, database=self.__database, user=self.__user, password=self.__password
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(*args, **kwargs)
                try:
                    res = cur.fetchall()
                except Exception:
                    res = None
        return res

    def create(self) -> None:
        """Creates necessary tables"""
        self.__exec(
            """
            CREATE TABLE IF NOT EXISTS employers (
                employer_local_id serial,
                
                name varchar NOT NULL,
                id varchar NOT NULL UNIQUE,
                url varchar,
                alternate_url varchar,
                description varchar,
                accredited_it bool,
                vacancies_url varchar NOT NULL,
                
                CONSTRAINT pk_employers_employer_local_id PRIMARY KEY (employer_local_id)
            );
            CREATE TABLE IF NOT EXISTS vacancies (
                  vacancy_local_id serial,
                  employer_local_id integer,
                  
                  url varchar,
                  alternate_url varchar,
                  id varchar NOT NULL UNIQUE,
                  name varchar NOT NULL,
                  area_name varchar,
                  requirement varchar,
                  responsibility varchar,
                  currency varchar,
                  salary_from integer,
                  salary_to integer,
                  
                  salary_mean integer,
                  
                  CONSTRAINT pk_vacancies_vacancy_local_id PRIMARY KEY (vacancy_local_id),
                  CONSTRAINT fk_vacancies_employers FOREIGN KEY (employer_local_id) 
                  REFERENCES employers (employer_local_id)
            );
            """
        )

    def add_employers(self, employers: list[Employer]) -> None:
        """Adds employers to DB"""
        if not isinstance(employers, list):
            raise TypeError("A list expected to add_employers")
        for e in employers:
            try:
                tpl: tuple = e.name, e.id, e.url, e.alternate_url, e.description, e.accredited_it, e.vacancies_url
                self.__exec(
                    """
                    INSERT INTO 
                    employers (name, id, url, alternate_url, description, accredited_it, vacancies_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    tpl,
                )
            except Exception:
                pass

    def truncate(self) -> None:
        """Clears tables"""
        self.__exec(
            """
            TRUNCATE TABLE employers CASCADE;
            """
        )

    def drop(self) -> None:
        """Deletes tables"""
        self.__exec(
            """
            DROP TABLE employers CASCADE;
            """
        )

    def truncate_vacancies(self) -> None:
        """Clears vacancies table"""
        self.__exec(
            """
            TRUNCATE TABLE vacancies RESTART IDENTITY
            """
        )

    def drop_vacancies(self) -> None:
        """Deletes vacancies table"""
        self.__exec(
            """
            DROP TABLE vacancies
            """
        )

    def refresh_vacancies(self) -> None:
        """Searches vacancies by employers table and writes to vacancies table"""
        self.truncate_vacancies()
        employers_res = self.__exec(
            """
            SELECT * FROM employers
            """
        )

        employers = []
        for e_data in employers_res:
            employers.append((e_data[0], Employer(*e_data[1:])))

        for e in employers:
            vacancies = HH.get_vacancies(e[1])
            for v in vacancies:
                try:
                    if v.salary_from and v.salary_to:
                        salary_mean = (v.salary_from + v.salary_to) // 2
                    elif v.salary_from or v.salary_to:
                        salary_mean = v.salary_from or v.salary_to
                    else:
                        salary_mean = None
                    tpl: tuple = (
                        e[0],
                        v.url,
                        v.alternate_url,
                        v.id,
                        v.name,
                        v.area_name,
                        v.requirement,
                        v.responsibility,
                        v.currency,
                        v.salary_from,
                        v.salary_to,
                        salary_mean,
                    )
                    self.__exec(
                        """
                        INSERT INTO
                        vacancies (
                            employer_local_id, url, alternate_url,
                            id, name, area_name, requirement, responsibility,
                            currency, salary_from, salary_to, salary_mean
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        tpl,
                    )
                except Exception:
                    pass

    def get_companies_and_vacancies_count(self) -> list[tuple] | None:
        """Gets list of employers and counts its vacancies"""
        return self.__exec(
            """
            SELECT name, volume 
            FROM employers 
            LEFT JOIN (
                SELECT employer_local_id, COUNT(*) as volume
                FROM vacancies GROUP BY employer_local_id
            ) 
            USING(employer_local_id)
            """
        )

    def get_all_vacancies(self) -> list[tuple] | None:
        """Returns all vacancies with employers names"""
        return self.__exec(
            """
            SELECT employers.name, vacancies.name, 
            vacancies.currency, vacancies.salary_from, vacancies.salary_to, 
            vacancies.alternate_url
            FROM vacancies 
            JOIN employers
            USING(employer_local_id)
            ORDER BY salary_mean DESC NULLS LAST
            """
        )

    def get_avg_salary(self) -> int | None:
        """Returns average salary for all vacancies"""
        res = self.__exec(
            """
            SELECT AVG(salary_mean) FROM vacancies
            """
        )
        try:
            return int(float(str(res[0][0])))
        except Exception:
            return None

    def get_vacancies_with_higher_salary(self) -> list[tuple] | None:
        """Returns all vacancies with salary higher than average with employers names"""
        return self.__exec(
            """
            SELECT employers.name, vacancies.name, 
            vacancies.currency, vacancies.salary_from, vacancies.salary_to, 
            vacancies.alternate_url
            FROM vacancies 
            JOIN employers
            USING(employer_local_id)
            WHERE salary_mean > (SELECT AVG(salary_mean) FROM vacancies)
            ORDER BY salary_mean DESC NULLS LAST
            """
        )

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple] | None:
        """Returns vacancies searched in DB by the keyword in name, requirement or responsibility"""
        if not isinstance(keyword, str):
            raise TypeError
        return self.__exec(
            f"""
            SELECT employers.name, vacancies.name, 
            vacancies.currency, vacancies.salary_from, vacancies.salary_to, 
            vacancies.alternate_url
            FROM vacancies 
            JOIN employers
            USING(employer_local_id)
            WHERE
            (vacancies.name LIKE '%{keyword}%') OR
            (requirement LIKE '%{keyword}%') OR
            (responsibility LIKE '%{keyword}%')
            ORDER BY salary_mean DESC NULLS LAST
            """
        )
