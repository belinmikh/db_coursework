import requests

from src.objects import Employer, Vacancy


class HH:
    """API-requests to hh.ru object"""

    last_employer_search: str | None
    employer_iter: int

    def __init__(self):
        self.last_employer_search = None
        self.employer_iter = 0

    def find_employer(self, data: str) -> Employer | None:
        """
        Tries to search an employer and research if it gets the same input next time
        :param data: str search keyword
        :return: Employer object or None
        """
        if not isinstance(data, str):
            raise TypeError("String expected to find employer")

        if data == self.last_employer_search:
            self.employer_iter += 1
        else:
            self.employer_iter = 0

        self.last_employer_search = data

        search_response: requests.Response = requests.get(
            f"https://api.hh.ru/employers?text={data}&page={self.employer_iter}&per_page=1"
        )

        if search_response.status_code != 200:
            return None

        try:
            employer_id = search_response.json()["items"][0]["id"]
            result_response: requests.Response = requests.get(f"https://api.hh.ru/employers/{employer_id}")
            return Employer.from_dict(result_response.json())
        except Exception:
            return None

    @staticmethod
    def get_vacancies(e: Employer) -> list[Vacancy]:
        """
        Search employer's vacancies
        :param e: Employer object
        :return: list of Vacancy objects
        """
        if not isinstance(e, Employer):
            raise TypeError("Employer object expected to get vacancies")
        rq0 = requests.Response = requests.get(e.vacancies_url + "&per_page=100")
        try:
            to_return: list = rq0.json()["items"]
            for n in range(1, rq0.json()["pages"]):
                rq: requests.Response = requests.get(e.vacancies_url + f"&per_page=100&page={n}")
                to_return.extend(rq.json()["items"])
            return [Vacancy.from_dict(v) for v in to_return]
        except Exception:
            return []

    def erase(self):
        """Forgets last employer search"""
        self.last_employer_search = None
        self.employer_iter = 0
