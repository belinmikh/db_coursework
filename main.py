import json
import os
import sys
import time

from dotenv import load_dotenv
from rich import print as rprint
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from src.api import HH
from src.db import DBManager
from src.objects import Employer


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def user_interact() -> None:
    print(
        "Нажатие Enter очистит экран и начнёт выполнение программы:\n"
        "для лучшего опыта установите удобную ширину консоли\n"
        "(при не-консольном запуске могут быть проблемы с отображением)"
    )
    input()
    clear()

    hh = HH()

    rprint(Panel("Читаю .env...\n\n", title="[bold yellow]hh.ru super duper ultra mega parser!!1!!1!1"))

    try:
        time.sleep(1)

        with open(".env", "r"):
            pass
        load_dotenv()

        clear()
        rprint(
            Panel(
                "Читаю .env ...                        [bold green]OK[/bold green]\n" "Подключаюсь к PostgreSQL...\n",
                title="[bold yellow]hh.ru super duper ultra mega parser!!1!!1!1",
            )
        )
    except Exception as ex:
        clear()
        rprint(
            Panel(
                "Читаю .env ...                        [bold red]FAIL[/bold red]\n\n",
                title="[bold yellow]hh.ru super duper ultra mega parser!!1!!1!1",
            )
        )
        rprint("Проверьте наличие файла [yellow].env[/yellow]\n" f"[grey50]{ex}[/grey50]")
        sys.exit()

    try:
        time.sleep(1)

        dbm = DBManager(os.getenv("host"), os.getenv("database"), os.getenv("user"), os.getenv("password"))

        clear()
        rprint(
            Panel(
                "Читаю .env ...                        [bold green]OK[/bold green]\n"
                "Подключаюсь к PostgreSQL...           [bold green]OK[/bold green]\n"
                "Ещё одно ожидание для важного вида... ",
                title="[bold yellow]hh.ru super duper ultra mega parser!!1!!1!1",
            )
        )
    except Exception as ex:
        clear()
        rprint(
            Panel(
                "Читаю .env ...                        [bold green]OK[/bold green]\n"
                "Подключаюсь к PostgreSQL...           [bold red]FAIL[/bold red]\n",
                title="[bold yellow]hh.ru super duper ultra mega parser!!1!!1!1",
            )
        )
        rprint(
            "Проверьте корректность данных в файле [yellow].env[/yellow]\n"
            "и соответствие файла предоставленному образцу [yellow].example[/yellow]\n"
            f"[grey50]{ex}[/grey50]"
        )
        sys.exit()

    time.sleep(1)

    clear()
    rprint(
        Panel(
            "Читаю .env ...                        [bold green]OK[/bold green]\n"
            "Подключаюсь к PostgreSQL...           [bold green]OK[/bold green]\n"
            "Ещё одно ожидание для важного вида... [bold green]OK[/bold green]",
            title="[bold yellow]hh.ru super duper ultra mega parser!!1!!1!1",
        )
    )
    time.sleep(0.3)

    while True:
        try:
            user_input = Prompt.ask(
                "Добавить работодателей по умолчанию?\n"
                "[grey50](необходимо наличие файла [bold]default.json[/bold])[/grey50]",
                default="Y",
                choices=["Y", "N"],
                case_sensitive=False,
            )
            break
        except Exception as ex:
            rprint("Что-то пошло не так...\n" f"[gray50]{ex}[/gray50]")
    clear()

    if user_input.strip().lower() == "y":
        try:
            with open("default.json") as file:
                employers_dicts = json.load(file)
            employers = [Employer.from_dict(e) for e in employers_dicts]
            dbm.add_employers(employers)
            rprint(
                "Работодатели по умолчанию [green]успешно загружены![/green]\n"
                "Обновляю список вакансий...\n"
                "[grey50]Это может быть долго - программа не глючит[/grey50]"
            )
            try:
                dbm.refresh_vacancies()
                rprint("Список вакансий [green]успешно обновлён![/green]")
            except Exception as ex:
                rprint(
                    "[red bold]Проблемы с добавлением вакансий, работа может быть продолжена[/red bold]\n"
                    f"[grey50]{ex}[/grey50]"
                )
        except FileNotFoundError:
            rprint("[red][bold]default.json[/bold] не найден![/red]")
        except Exception as ex:
            rprint(
                "[red bold]Проблемы с добавлением работодателей, работа может быть продолжена[/red bold]\n"
                f"[grey50]{ex}[/grey50]"
            )
        time.sleep(1.5)
    time.sleep(0.5)

    while True:
        clear()
        rprint(
            "[deep_sky_blue2]0. Добавить работодателя[/deep_sky_blue2]\n"
            "[hot_pink]1. Обновить вакансии[/hot_pink]\n"
            "[deep_sky_blue2]2. Текущий список работодателей с количеством вакансий[/deep_sky_blue2]\n"
            "[hot_pink]3. Вывести вакансии[/hot_pink]\n"
            "[deep_sky_blue2]4. Вывести среднюю з/п по всем вакансиям[/deep_sky_blue2]\n"
            "[hot_pink]5. Вывести вакансии с з/п выше средней[/hot_pink]\n"
            "[deep_sky_blue2]6. Вывести вакансии по ключевому слову[/deep_sky_blue2]\n"
            "[hot_pink]7. Очистить вакансии[/hot_pink]\n"
            "[deep_sky_blue2]8. Очистить вакансии и работодателей[/deep_sky_blue2]\n"
            "[hot_pink]9. УДАЛИТЬ таблицу вакансий (завершит работу программы)[/hot_pink]\n"
            "[deep_sky_blue2]10. УДАЛИТЬ таблицы вакансий и работодателей (завершит работу программы)[/deep_sky_blue2]\n"
        )
        while True:
            try:
                user_input = Prompt.ask(
                    "[grey50]< ? > [/grey50] ", choices=[*map(str, range(11)), "EXIT"], case_sensitive=False
                )
                clear()
                break
            except Exception as ex:
                rprint("Что-то пошло не так...\n" f"[grey50]{ex}\nНажмите Enter для возвращения в меню[/grey50]")
                input()

        if user_input == "0":
            rprint(
                "[bright_red bold]0. Добавить работодателя[/bright_red bold]\n"
                "[hot_pink]1. Обновить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]2. Текущий список работодателей с количеством вакансий[/deep_sky_blue2]\n"
                "[hot_pink]3. Вывести вакансии[/hot_pink]\n"
                "[deep_sky_blue2]4. Вывести среднюю з/п по всем вакансиям[/deep_sky_blue2]\n"
                "[hot_pink]5. Вывести вакансии с з/п выше средней[/hot_pink]\n"
                "[deep_sky_blue2]6. Вывести вакансии по ключевому слову[/deep_sky_blue2]\n"
                "[hot_pink]7. Очистить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]8. Очистить вакансии и работодателей[/deep_sky_blue2]\n"
                "[hot_pink]9. УДАЛИТЬ таблицу вакансий (завершит работу программы)[/hot_pink]\n"
                "[deep_sky_blue2]10. УДАЛИТЬ таблицы вакансий и работодателей (завершит работу программы)[/deep_sky_blue2]\n"
            )
            time.sleep(0.5)
            clear()

            while True:
                try:
                    name = Prompt.ask("Введите название работодателя для поиска")
                    break
                except Exception as ex:
                    rprint("Что-то пошло не так...\n" f"[grey50]{ex}[/grey50]")

            while True:
                try:
                    employer = hh.find_employer(name)
                    rprint(employer.name)
                    user_input = Prompt.ask(
                        "Это похоже на то, что вы ищете?", choices=["Y", "N", "CANCEL"], case_sensitive=False
                    )
                except Exception:
                    rprint(
                        "Похоже, вы просмотрели все возможные варианты\n"
                        "[grey50]Нажмите Enter для возвращения в меню[/grey50]"
                    )
                    input()
                    hh.erase()
                    break
                clear()
                if user_input.lower() == "y":
                    try:
                        dbm.add_employers([employer])
                        rprint(
                            "Работодатель добавлен в базу, обновляю вакансии...\n"
                            "[grey50]Это может быть долго - программа не глючит[/grey50]"
                        )
                        dbm.refresh_vacancies()
                    except Exception as ex:
                        rprint(
                            "Что-то пошло не так...\n" f"[grey50]{ex}\nНажмите Enter для возвращения в меню[/grey50]"
                        )
                    break
                elif user_input.lower() == "n":
                    clear()
                else:
                    break

        elif user_input == "1":
            rprint(
                "[deep_sky_blue2]0. Добавить работодателя[/deep_sky_blue2]\n"
                "[bright_red bold]1. Обновить вакансии[/bright_red bold]\n"
                "[deep_sky_blue2]2. Текущий список работодателей с количеством вакансий[/deep_sky_blue2]\n"
                "[hot_pink]3. Вывести вакансии[/hot_pink]\n"
                "[deep_sky_blue2]4. Вывести среднюю з/п по всем вакансиям[/deep_sky_blue2]\n"
                "[hot_pink]5. Вывести вакансии с з/п выше средней[/hot_pink]\n"
                "[deep_sky_blue2]6. Вывести вакансии по ключевому слову[/deep_sky_blue2]\n"
                "[hot_pink]7. Очистить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]8. Очистить вакансии и работодателей[/deep_sky_blue2]\n"
                "[hot_pink]9. УДАЛИТЬ таблицу вакансий (завершит работу программы)[/hot_pink]\n"
                "[deep_sky_blue2]10. УДАЛИТЬ таблицы вакансий и работодателей (завершит работу программы)[/deep_sky_blue2]\n"
            )
            time.sleep(0.5)
            clear()

            try:
                rprint("Обновляю вакансии...\n" "[grey50]Это может быть долго - программа не глючит[/grey50]")
                dbm.refresh_vacancies()
            except Exception as ex:
                rprint("Что-то пошло не так...\n" f"[grey50]{ex}\nНажмите Enter для возвращения в меню[/grey50]")
                input()

        elif user_input == "2":
            rprint(
                "[deep_sky_blue2]0. Добавить работодателя[/deep_sky_blue2]\n"
                "[hot_pink]1. Обновить вакансии[/hot_pink]\n"
                "[bright_red bold]2. Текущий список работодателей с количеством вакансий[/bright_red bold]\n"
                "[hot_pink]3. Вывести вакансии[/hot_pink]\n"
                "[deep_sky_blue2]4. Вывести среднюю з/п по всем вакансиям[/deep_sky_blue2]\n"
                "[hot_pink]5. Вывести вакансии с з/п выше средней[/hot_pink]\n"
                "[deep_sky_blue2]6. Вывести вакансии по ключевому слову[/deep_sky_blue2]\n"
                "[hot_pink]7. Очистить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]8. Очистить вакансии и работодателей[/deep_sky_blue2]\n"
                "[hot_pink]9. УДАЛИТЬ таблицу вакансий (завершит работу программы)[/hot_pink]\n"
                "[deep_sky_blue2]10. УДАЛИТЬ таблицы вакансий и работодателей (завершит работу программы)[/deep_sky_blue2]\n"
            )
            time.sleep(0.5)
            clear()

            try:
                employers = dbm.get_companies_and_vacancies_count()
                table = Table(title="Работодатели")

                table.add_column("Название", style="cyan")
                table.add_column("Количество вакансий", style="magenta")

                for employer in employers:
                    table.add_row(employer[0], str(employer[1]) if employer[1] else "0")

                rprint(table)
                rprint("[grey50]Нажмите Enter для возвращения в меню[/grey50]")
                input()

            except Exception as ex:
                rprint("Что-то пошло не так...\n" f"[grey50]{ex}\nНажмите Enter для возвращения в меню[/grey50]")
                input()

        elif user_input == "3":
            rprint(
                "[deep_sky_blue2]0. Добавить работодателя[/deep_sky_blue2]\n"
                "[hot_pink]1. Обновить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]2. Текущий список работодателей с количеством вакансий[/deep_sky_blue2]\n"
                "[bright_red bold]3. Вывести вакансии[/bright_red bold]\n"
                "[deep_sky_blue2]4. Вывести среднюю з/п по всем вакансиям[/deep_sky_blue2]\n"
                "[hot_pink]5. Вывести вакансии с з/п выше средней[/hot_pink]\n"
                "[deep_sky_blue2]6. Вывести вакансии по ключевому слову[/deep_sky_blue2]\n"
                "[hot_pink]7. Очистить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]8. Очистить вакансии и работодателей[/deep_sky_blue2]\n"
                "[hot_pink]9. УДАЛИТЬ таблицу вакансий (завершит работу программы)[/hot_pink]\n"
                "[deep_sky_blue2]10. УДАЛИТЬ таблицы вакансий и работодателей (завершит работу программы)[/deep_sky_blue2]\n"
            )
            time.sleep(0.5)
            clear()

            try:
                vacancies = dbm.get_all_vacancies()
                n = len(vacancies)
                if len(vacancies) > 10:
                    rprint(f"Кажется, вакансий много для вывода: [yellow bold]{len(vacancies)}[/yellow bold]")
                    user_input = Prompt.ask("Хотите ограничить вывод?", choices=["Y", "N"], case_sensitive=False)
                    if user_input.lower() == "y":
                        rprint("Сколько вывести?")
                        while True:
                            try:
                                n = int(input())
                                assert 1 <= n <= len(vacancies)
                                break
                            except Exception:
                                rprint("Ввод не может быть интерпретирован как число вакансий, повторите")

                table = Table(title="Вакансии по убыванию з/п")

                table.add_column("Работодатель", style="cyan")
                table.add_column("Название", style="magenta")
                table.add_column("Валюта", style="green")
                table.add_column("От", style="cyan")
                table.add_column("До", style="magenta")
                table.add_column("Ссылка", style="green")

                for i in range(n):
                    table.add_row(
                        vacancies[i][0],
                        vacancies[i][1],
                        vacancies[i][2] or "N/A",
                        str(vacancies[i][3]) if vacancies[i][3] else "N/A",
                        str(vacancies[i][4]) if vacancies[i][4] else "N/A",
                        vacancies[i][5] or "N/A",
                    )

                rprint(table)
                rprint("[grey50]Нажмите Enter для возвращения в меню[/grey50]")
                input()

            except Exception as ex:
                rprint("Что-то пошло не так...\n" f"[grey50]{ex}\nНажмите Enter для возвращения в меню[/grey50]")
                input()

        elif user_input == "4":
            rprint(
                "[deep_sky_blue2]0. Добавить работодателя[/deep_sky_blue2]\n"
                "[hot_pink]1. Обновить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]2. Текущий список работодателей с количеством вакансий[/deep_sky_blue2]\n"
                "[hot_pink]3. Вывести вакансии[/hot_pink]\n"
                "[bright_red bold]4. Вывести среднюю з/п по всем вакансиям[/bright_red bold]\n"
                "[hot_pink]5. Вывести вакансии с з/п выше средней[/hot_pink]\n"
                "[deep_sky_blue2]6. Вывести вакансии по ключевому слову[/deep_sky_blue2]\n"
                "[hot_pink]7. Очистить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]8. Очистить вакансии и работодателей[/deep_sky_blue2]\n"
                "[hot_pink]9. УДАЛИТЬ таблицу вакансий (завершит работу программы)[/hot_pink]\n"
                "[deep_sky_blue2]10. УДАЛИТЬ таблицы вакансий и работодателей (завершит работу программы)[/deep_sky_blue2]\n"
            )
            time.sleep(0.5)
            clear()

            try:
                rprint(f"Средняя з/п по всем вакансиям: [yellow bold]{dbm.get_avg_salary()}[/yellow bold]")
                rprint("[grey50]Нажмите Enter для возвращения в меню[/grey50]")
                input()

            except Exception as ex:
                rprint("Что-то пошло не так...\n" f"[grey50]{ex}\nНажмите Enter для возвращения в меню[/grey50]")
                input()

        elif user_input == "5":
            rprint(
                "[deep_sky_blue2]0. Добавить работодателя[/deep_sky_blue2]\n"
                "[hot_pink]1. Обновить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]2. Текущий список работодателей с количеством вакансий[/deep_sky_blue2]\n"
                "[hot_pink]3. Вывести вакансии[/hot_pink]\n"
                "[deep_sky_blue2]4. Вывести среднюю з/п по всем вакансиям[/deep_sky_blue2]\n"
                "[bright_red bold]5. Вывести вакансии с з/п выше средней[/bright_red bold]\n"
                "[deep_sky_blue2]6. Вывести вакансии по ключевому слову[/deep_sky_blue2]\n"
                "[hot_pink]7. Очистить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]8. Очистить вакансии и работодателей[/deep_sky_blue2]\n"
                "[hot_pink]9. УДАЛИТЬ таблицу вакансий (завершит работу программы)[/hot_pink]\n"
                "[deep_sky_blue2]10. УДАЛИТЬ таблицы вакансий и работодателей (завершит работу программы)[/deep_sky_blue2]\n"
            )
            time.sleep(0.5)
            clear()

            try:
                vacancies = dbm.get_vacancies_with_higher_salary()
                n = len(vacancies)
                if len(vacancies) > 10:
                    rprint(f"Кажется, вакансий много для вывода: [yellow bold]{len(vacancies)}[/yellow bold]")
                    user_input = Prompt.ask("Хотите ограничить вывод?", choices=["Y", "N"], case_sensitive=False)
                    if user_input.lower() == "y":
                        rprint("Сколько вывести?")
                        while True:
                            try:
                                n = int(input())
                                assert 1 <= n <= len(vacancies)
                                break
                            except Exception:
                                rprint("Ввод не может быть интерпретирован как число вакансий, повторите")

                table = Table(title="Вакансии с з/п выше средней по убыванию")

                table.add_column("Работодатель", style="cyan")
                table.add_column("Название", style="magenta")
                table.add_column("Валюта", style="green")
                table.add_column("От", style="cyan")
                table.add_column("До", style="magenta")
                table.add_column("Ссылка", style="green")

                for i in range(n):
                    table.add_row(
                        vacancies[i][0],
                        vacancies[i][1],
                        vacancies[i][2] or "N/A",
                        str(vacancies[i][3]) if vacancies[i][3] else "N/A",
                        str(vacancies[i][4]) if vacancies[i][4] else "N/A",
                        vacancies[i][5] or "N/A",
                    )

                rprint(table)
                rprint("[grey50]Нажмите Enter для возвращения в меню[/grey50]")
                input()

            except Exception as ex:
                rprint("Что-то пошло не так...\n" f"[grey50]{ex}\nНажмите Enter для возвращения в меню[/grey50]")
                input()

        elif user_input == "6":
            rprint(
                "[deep_sky_blue2]0. Добавить работодателя[/deep_sky_blue2]\n"
                "[hot_pink]1. Обновить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]2. Текущий список работодателей с количеством вакансий[/deep_sky_blue2]\n"
                "[hot_pink]3. Вывести вакансии[/hot_pink]\n"
                "[deep_sky_blue2]4. Вывести среднюю з/п по всем вакансиям[/deep_sky_blue2]\n"
                "[hot_pink]5. Вывести вакансии с з/п выше средней[/hot_pink]\n"
                "[bright_red bold]6. Вывести вакансии по ключевому слову[/bright_red bold]\n"
                "[hot_pink]7. Очистить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]8. Очистить вакансии и работодателей[/deep_sky_blue2]\n"
                "[hot_pink]9. УДАЛИТЬ таблицу вакансий (завершит работу программы)[/hot_pink]\n"
                "[deep_sky_blue2]10. УДАЛИТЬ таблицы вакансий и работодателей (завершит работу программы)[/deep_sky_blue2]\n"
            )
            time.sleep(0.5)
            clear()

            rprint("Введите выражение для поиска")

            try:
                keyword = input()
                vacancies = dbm.get_vacancies_with_keyword(keyword)
                n = len(vacancies)
                if len(vacancies) > 10:
                    rprint(f"Кажется, вакансий много для вывода: [yellow bold]{len(vacancies)}[/yellow bold]")
                    user_input = Prompt.ask("Хотите ограничить вывод?", choices=["Y", "N"], case_sensitive=False)
                    if user_input.lower() == "y":
                        rprint("Сколько вывести?")
                        while True:
                            try:
                                n = int(input())
                                assert 1 <= n <= len(vacancies)
                                break
                            except Exception:
                                rprint("Ввод не может быть интерпретирован как число вакансий, повторите")

                table = Table(title=f"Вакансии по запросу {keyword} по убыванию з/п")

                table.add_column("Работодатель", style="cyan")
                table.add_column("Название", style="magenta")
                table.add_column("Валюта", style="green")
                table.add_column("От", style="cyan")
                table.add_column("До", style="magenta")
                table.add_column("Ссылка", style="green")

                for i in range(n):
                    table.add_row(
                        vacancies[i][0],
                        vacancies[i][1],
                        vacancies[i][2] or "N/A",
                        str(vacancies[i][3]) if vacancies[i][3] else "N/A",
                        str(vacancies[i][4]) if vacancies[i][4] else "N/A",
                        vacancies[i][5] or "N/A",
                    )

                rprint(table)
                rprint("[grey50]Нажмите Enter для возвращения в меню[/grey50]")
                input()

            except Exception as ex:
                rprint("Что-то пошло не так...\n" f"[grey50]{ex}\nНажмите Enter для возвращения в меню[/grey50]")
                input()

        elif user_input == "7":
            rprint(
                "[deep_sky_blue2]0. Добавить работодателя[/deep_sky_blue2]\n"
                "[hot_pink]1. Обновить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]2. Текущий список работодателей с количеством вакансий[/deep_sky_blue2]\n"
                "[hot_pink]3. Вывести вакансии[/hot_pink]\n"
                "[deep_sky_blue2]4. Вывести среднюю з/п по всем вакансиям[/deep_sky_blue2]\n"
                "[hot_pink]5. Вывести вакансии с з/п выше средней[/hot_pink]\n"
                "[deep_sky_blue2]6. Вывести вакансии по ключевому слову[/deep_sky_blue2]\n"
                "[bright_red bold]7. Очистить вакансии[/bright_red bold]\n"
                "[deep_sky_blue2]8. Очистить вакансии и работодателей[/deep_sky_blue2]\n"
                "[hot_pink]9. УДАЛИТЬ таблицу вакансий (завершит работу программы)[/hot_pink]\n"
                "[deep_sky_blue2]10. УДАЛИТЬ таблицы вакансий и работодателей (завершит работу программы)[/deep_sky_blue2]\n"
            )
            time.sleep(0.5)
            clear()

            try:
                rprint("Вы собираетесь очистить таблицу вакансий")
                user_input = Prompt.ask("Уверены?", choices=["Y", "N"], default="N", case_sensitive=False)
                if user_input == "Y":
                    dbm.truncate_vacancies()
            except Exception as ex:
                rprint("Что-то пошло не так...\n" f"[grey50]{ex}\nНажмите Enter для возвращения в меню[/grey50]")
                input()

        elif user_input == "8":
            rprint(
                "[deep_sky_blue2]0. Добавить работодателя[/deep_sky_blue2]\n"
                "[hot_pink]1. Обновить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]2. Текущий список работодателей с количеством вакансий[/deep_sky_blue2]\n"
                "[hot_pink]3. Вывести вакансии[/hot_pink]\n"
                "[deep_sky_blue2]4. Вывести среднюю з/п по всем вакансиям[/deep_sky_blue2]\n"
                "[hot_pink]5. Вывести вакансии с з/п выше средней[/hot_pink]\n"
                "[deep_sky_blue2]6. Вывести вакансии по ключевому слову[/deep_sky_blue2]\n"
                "[hot_pink]7. Очистить вакансии[/hot_pink]\n"
                "[bright_red bold]8. Очистить вакансии и работодателей[/bright_red bold]\n"
                "[hot_pink]9. УДАЛИТЬ таблицу вакансий (завершит работу программы)[/hot_pink]\n"
                "[deep_sky_blue2]10. УДАЛИТЬ таблицы вакансий и работодателей (завершит работу программы)[/deep_sky_blue2]\n"
            )
            time.sleep(0.5)
            clear()

            try:
                rprint("Вы собираетесь очистить таблицу вакансий и работодателей")
                user_input = Prompt.ask("Уверены?", choices=["Y", "N"], default="N", case_sensitive=False)
                if user_input == "Y":
                    dbm.truncate()
            except Exception as ex:
                rprint("Что-то пошло не так...\n" f"[grey50]{ex}\nНажмите Enter для возвращения в меню[/grey50]")
                input()

        elif user_input == "9":
            rprint(
                "[deep_sky_blue2]0. Добавить работодателя[/deep_sky_blue2]\n"
                "[hot_pink]1. Обновить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]2. Текущий список работодателей с количеством вакансий[/deep_sky_blue2]\n"
                "[hot_pink]3. Вывести вакансии[/hot_pink]\n"
                "[deep_sky_blue2]4. Вывести среднюю з/п по всем вакансиям[/deep_sky_blue2]\n"
                "[hot_pink]5. Вывести вакансии с з/п выше средней[/hot_pink]\n"
                "[deep_sky_blue2]6. Вывести вакансии по ключевому слову[/deep_sky_blue2]\n"
                "[hot_pink]7. Очистить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]8. Очистить вакансии и работодателей[/deep_sky_blue2]\n"
                "[bright_red bold]9. УДАЛИТЬ таблицу вакансий (завершит работу программы)[/bright_red bold]\n"
                "[deep_sky_blue2]10. УДАЛИТЬ таблицы вакансий и работодателей (завершит работу программы)[/deep_sky_blue2]\n"
            )
            time.sleep(0.5)
            clear()

            try:
                rprint("Вы собираетесь УДАЛИТЬ таблицу вакансий")
                user_input = Prompt.ask("Уверены?", choices=["Y", "N"], default="N", case_sensitive=False)
                if user_input == "Y":
                    dbm.drop_vacancies()
                    break
            except Exception as ex:
                rprint("Что-то пошло не так...\n" f"[grey50]{ex}\nНажмите Enter для возвращения в меню[/grey50]")
                input()
        elif user_input == "10":
            rprint(
                "[deep_sky_blue2]0. Добавить работодателя[/deep_sky_blue2]\n"
                "[hot_pink]1. Обновить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]2. Текущий список работодателей с количеством вакансий[/deep_sky_blue2]\n"
                "[hot_pink]3. Вывести вакансии[/hot_pink]\n"
                "[deep_sky_blue2]4. Вывести среднюю з/п по всем вакансиям[/deep_sky_blue2]\n"
                "[hot_pink]5. Вывести вакансии с з/п выше средней[/hot_pink]\n"
                "[deep_sky_blue2]6. Вывести вакансии по ключевому слову[/deep_sky_blue2]\n"
                "[hot_pink]7. Очистить вакансии[/hot_pink]\n"
                "[deep_sky_blue2]8. Очистить вакансии и работодателей[/deep_sky_blue2]\n"
                "[hot_pink]9. УДАЛИТЬ таблицу вакансий (завершит работу программы)[/hot_pink]\n"
                "[bright_red bold]10. УДАЛИТЬ таблицы вакансий и работодателей (завершит работу программы)[/bright_red bold]\n"
            )
            time.sleep(0.5)
            clear()

            try:
                rprint("Вы собираетесь УДАЛИТЬ таблицы вакансий и работодателей")
                user_input = Prompt.ask("Уверены?", choices=["Y", "N"], default="N", case_sensitive=False)
                if user_input == "Y":
                    dbm.drop()
                    break
            except Exception as ex:
                rprint("Что-то пошло не так...\n" f"[grey50]{ex}\nНажмите Enter для возвращения в меню[/grey50]")
                input()
        else:
            break

    goodbye = "ДО НОВЫХ ВСТРЕЧ!"
    for n in range(len(goodbye) + 1):
        clear()
        rprint(f"[magenta1]{goodbye[:n]}[/magenta1]{goodbye[n:]}")
        time.sleep(0.15)
    time.sleep(0.85)
    clear()
    sys.exit()


if __name__ == "__main__":
    user_interact()
