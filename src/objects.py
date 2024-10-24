class Employer:
    """Data object for employer"""

    name: str
    id: str
    url: str | None
    alternate_url: str | None
    description: str | None
    accredited_it: bool | None
    vacancies_url: str

    __slots__ = ("name", "id", "url", "alternate_url", "description", "accredited_it", "vacancies_url")

    def __init__(
        self,
        name: str,
        e_id: str,
        url: str | None,
        alternate_url: str | None,
        description: str | None,
        accredited_it: bool | None,
        vacancies_url: str,
    ):
        if not isinstance(name, str) or not isinstance(e_id, str) or not isinstance(vacancies_url, str):
            raise TypeError
        if url and not isinstance(url, str):
            raise TypeError
        if alternate_url and not isinstance(alternate_url, str):
            raise TypeError
        if description and not isinstance(description, str):
            raise TypeError
        if accredited_it is not None and not isinstance(accredited_it, bool):
            raise TypeError

        self.name = name
        self.id = e_id
        self.url = url
        self.alternate_url = alternate_url
        self.description = description
        self.accredited_it = accredited_it
        self.vacancies_url = vacancies_url

    @staticmethod
    def from_dict(data: dict) -> "Employer":
        """Creates Employer object out of dictionary

        :param data:
        {
            'name': str (required),
            'id': str (required),
            'url': str,
            'alternate_url': str,
            'description': str,
            'accredited_it_employer': bool,
            'vacancies url': str (required)
        }
        :return: Employer object"""
        if not isinstance(data, dict):
            raise TypeError("Dict expected for Employer init")
        try:
            name = data["name"]
            e_id = data["id"]
            url = data.get("url")
            alternate_url = data.get("alternate_url")
            description = data.get("description")
            accredited_it = data.get("accredited_it_employer")
            vacancies_url = data["vacancies_url"]
            return Employer(name, e_id, url, alternate_url, description, accredited_it, vacancies_url)
        except KeyError:
            raise KeyError("Bad dict for Employer")


class Vacancy:
    """Data object for vacancy"""

    url: str | None
    alternate_url: str | None
    id: str
    name: str
    area_name: str | None
    requirement: str | None
    responsibility: str | None
    currency: str | None
    salary_from: int | None
    salary_to: int | None

    __slots__ = (
        "url",
        "alternate_url",
        "id",
        "name",
        "area_name",
        "requirement",
        "responsibility",
        "currency",
        "salary_from",
        "salary_to",
    )

    def __init__(
        self,
        url: str | None,
        alternate_url: str | None,
        v_id: str,
        name: str,
        area_name: str | None,
        requirement: str | None,
        responsibility: str | None,
        currency: str | None,
        salary_from: int | None,
        salary_to: int | None,
    ):
        if not isinstance(v_id, str) or not isinstance(name, str):
            raise TypeError
        if url and not isinstance(url, str):
            raise TypeError
        if alternate_url and not isinstance(alternate_url, str):
            raise TypeError
        if area_name and not isinstance(area_name, str):
            raise TypeError
        if requirement and not isinstance(requirement, str):
            raise TypeError
        if responsibility and not isinstance(responsibility, str):
            raise TypeError
        if currency and not isinstance(currency, str):
            raise TypeError
        if salary_from and not isinstance(salary_from, int):
            raise TypeError
        if salary_to and not isinstance(salary_to, int):
            raise TypeError

        self.name = name
        self.id = v_id
        self.url = url
        self.alternate_url = alternate_url
        self.area_name = area_name
        self.requirement = requirement
        self.responsibility = responsibility
        self.currency = currency
        self.salary_from = salary_from
        self.salary_to = salary_to

    @staticmethod
    def from_dict(data: dict) -> "Vacancy":
        """
        Creates Vacancy object out of dictionary
        :param data:
        {
            'id': str (required),
            'name': str (required),
            'url': str,
            'alternate_url': str,
            'area': {
                'name': str
            },
            'snippet': {
                'requirement': str,
                'responsibility': str
            },
            'salary': {
                'currency': str,
                'from': int,
                'to': int
            }
        }
        :return: Vacancy object
        """
        if not isinstance(data, dict):
            raise TypeError("Dict expected for Vacancy init")
        try:
            v_id = data["id"]
            name = data["name"]

            url = data.get("url")
            alternate_url = data.get("alternate_url")

            try:
                area_name = data["area"]["name"]
            except Exception:
                area_name = None

            try:
                snippet: dict = data["snippet"]
                requirement = snippet.get("requirement")
                responsibility = snippet.get("responsibility")
            except Exception:
                requirement = None
                responsibility = None

            try:
                salary: dict = data["salary"]
                currency = salary.get("currency")
                salary_from = salary.get("from")
                salary_to = salary.get("to")
            except Exception:
                currency = None
                salary_from = None
                salary_to = None

            return Vacancy(
                url,
                alternate_url,
                v_id,
                name,
                area_name,
                requirement,
                responsibility,
                currency,
                salary_from,
                salary_to,
            )

        except KeyError:
            raise KeyError("Bad dict for Vacancy")
