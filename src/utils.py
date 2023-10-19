from src.work_api import HeadHunter, SuperJob
from src.work_file import ReadWriteToJSON
from src.work_vacancies import VacanciesHH, VacanciesSJ, VacanciesSort


class WorkToUser:
    """Взаимодействие с пользователем"""

    def __init__(self):
        self.site = None
        self.request = None
        self.city = None
        self.quantity = None

    def __str__(self):
        return f"Ваш запрос:" \
               f"\nСайт - {self.site}" \
               f"\nЗапрос - {self.request}" \
               f"\nГород - {self.city}" \
               f"\nКоличество вакансий - {self.quantity}"

    def choice_site(self):
        """Выбирает платформу для поиска вакансий"""

        site_list = ['hh.ru', 'superjob.ru']
        while True:
            try:
                choice_user = int(
                    input(f'1 - {site_list[0]}\n2 - {site_list[1]}\nВыбирите платформу для поиска вакансий: '))
                if choice_user in [1, 2]:
                    self.site = site_list[choice_user - 1]
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Некорректный ввод")

    def get_request(self):
        """Получает запрос пользователя"""

        self.request = input("\nВведите Ваш зопрос по поиску вакансий: ")

    def choice_city(self):
        """Выбирает город для поиска вакансий"""

        city_list = ['Россия', 'Москва', 'Санкт-Петербург']
        while True:
            try:
                choice_user = int(input(
                    f'1 - {city_list[0]}\n2 - {city_list[1]}\n3 - {city_list[2]}\nВыбирите регион для поиска вакансий: '))
                if choice_user in [1, 2, 3]:
                    self.city = city_list[choice_user - 1]
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Некорректный ввод")

    def quantity_vacancies(self):
        """Получает количество искомых вакансий от пользователя"""

        if self.site == 'superjob.ru':
            self.quantity = 20
            print(f'Количество вакансий будет - {self.quantity}')
        else:
            while True:
                try:
                    choice_user = int(input("\nДиапазон от 1 до 100\nВведите количество вакансий для вывода в топ: "))
                    if 0 < choice_user < 101:
                        self.quantity = choice_user
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Некорректный ввод")

    def work_api(self, number: int):
        """Выполняет работу API по запросу пользователя"""

        total = []
        if self.site == 'hh.ru':
            city = {'Россия': 1, 'Москва': 1, 'Санкт-Петербург': 2}
            info = HeadHunter(self.request, self.quantity, city[self.city]).get_info()
            for item in info:
                total.append(VacanciesHH(item).__dict__)
        else:
            city = {'Россия': 1, 'Москва': 4, 'Санкт-Петербург': 14}
            if self.city == 'Россия':
                info = SuperJob(self.request, c=city[self.city]).get_info()
            else:
                info = SuperJob(self.request, t=city[self.city]).get_info()
            for item in info:
                total.append(VacanciesSJ(item).__dict__)
        if number == 0:
            ReadWriteToJSON.write_json(total)
        else:
            ReadWriteToJSON.add_json(total)

    @staticmethod
    def sort_all():
        """Сортирует полученные вакансии"""

        all_vacancies = ReadWriteToJSON.read_json()
        total_vacancies = []
        for i in all_vacancies:
            total_vacancies.append(VacanciesSort(i['url'], i['title'], i['city'], i['salary_int'], i['salary'], i['requirements'], i['date']))
        total_vacancies.sort()
        info = []
        for i in total_vacancies:
            info.append(i.__dict__)
        ReadWriteToJSON.write_json(info)

    def find_word(self, find_words: str):
        """Выполняет поиск по ключевым словам пользователя"""

        info = ReadWriteToJSON.read_json()
        total = []
        for i in info:
            try:
                for iii in i.values():
                    try:
                        if find_words in iii:
                            if i['url'][:14] == 'https://hh.ru/':
                                total.append(i['url'])
                            else:
                                total.append(i['url'])
                    except TypeError:
                        continue
            except AttributeError:
                continue
        if total == []:
            return f'Ваш запрос: {find_words} не найден!'
        else:
            return f'Ваш запрос: {find_words} встречается в следующих вакансиях\n{total}'