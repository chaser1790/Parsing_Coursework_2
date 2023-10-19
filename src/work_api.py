from abc import ABC, abstractmethod
import requests as requests

# Функция для получения ключа API из локального файла
def get_api_key():
    # Открывает файл и возвращает ключ API, удаляя лишние пробелы
    with open('D:\\api_superjob.txt', 'r') as file:
        return file.read().strip()

# Абстрактный класс для работы с API различных платформ по поиску работы
class WorkApi(ABC):
    """Абстрактный класс для работы с API"""

    # В конструкторе абстрактного класса обычно нет кода
    @abstractmethod
    def __init__(self):
        pass

    # Абстрактный метод по умолчанию, который будет переопределен в дочерних классах
    @abstractmethod
    def get_info(self):
        pass

# Класс для работы с API платформы HeadHunter
class HeadHunter(WorkApi):

    # Ссылка для запросов
    url = 'https://api.hh.ru/vacancies'

    def __init__(self, text: str, per_page: int, city: int):
        # Инициализация атрибутов класса
        self.text = text
        self.per_page = per_page
        self.area = city

    # Метод для получения информации о вакансиях с сайта HeadHunter
    def get_info(self):
        """
        Извлекает список вакансий с помощью API
        :return: список вакансий (list)
        """
        # Отправка запроса и получение ответа API
        response = requests.get(self.url, params=self.__dict__)
        # Декодирование ответа JSON и получение списка вакансий
        info = response.json()['items']
        return info

# Класс для работы с API платформы SuperJob
class SuperJob(WorkApi):

    # Ссылка для запросов
    url = 'https://api.superjob.ru/2.0/vacancies/'

    # Создаем заголовки для запросов, включая ключ API, полученный из файла
    API_KEY = {'X-Api-App-Id': get_api_key()}

    def __init__(self, text: str, t=None, c=None):
        # Инициализация атрибутов класса
        self.keyword = text
        self.t = t
        self.c = c

    # Метод для получения информации о вакансиях с сайта SuperJob
    def get_info(self):
        """
        Извлекает список вакансий с помощью API
        :return: список вакансий (list)
        """
        # Отправляем запрос к API и получаем ответ
        response = requests.get(self.url, headers=self.API_KEY, params=self.__dict__)
        # Декодируем ответ JSON и извлекаем список вакансий
        info = response.json()['objects']
        return info
