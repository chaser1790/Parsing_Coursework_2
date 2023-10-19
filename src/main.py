from src.utils import WorkToUser
from src.work_file import ReadWriteToJSON


def get_user(player: WorkToUser, count: int):
    """Запускает процесс выполнения пользовательского запроса"""

    player.choice_site()  # Пользователь определяет желаемую платформу для поиска
    player.get_request()  # Пользователь формулирует его запрос
    player.choice_city()  # Пользователь выбирает местоположение для поиска вакансий
    player.quantity_vacancies()  # Задаётся количество вакансий для поиска

    print(f'\n{player}')  # Вывод информации о пользовательском запросе

    player.work_api(count)  # Формирование запроса к внешнему API


def repeat_get(player: WorkToUser):
    """Определяет, будет ли пользовательский запрос повторяться"""

    while True:
        try:
            choice_user = int(input('\n1 - Да\n2 - Нет\nХотите повторить запрос?'))
            if choice_user == 1:
                get_user(player, 1)
            elif choice_user == 2:
                break
            else:
                raise ValueError
        except ValueError:
            print("Введено неправильное значение")


def find_get(player: WorkToUser):
    """Выясняет, нужно ли пользователю произвести дополнительный поиск в уже найденных вакансиях"""

    while True:
        try:
            choice_user = int(input('\n1 - Да\n2 - Нет\nХотите найти ключевое слово в вакансиях?'))
            if choice_user == 1:
                data = input('Введите Ваш запрос: ')
                print(player.find_word(data))
            elif choice_user == 2:
                break
            else:
                raise ValueError
        except ValueError:
            print("Введено неправильное значение")


def main():

    while input('Нажмите Enter, чтобы начать: ') != '':
        continue

    # Очищаем файл
    f = open('vacancies.json', 'w')
    f.close()

    print('\nПриветствую Вас! Подготовим Ваш запрос по поиску вакансий.')

    player = WorkToUser()

    get_user(player, 0)
    repeat_get(player)
    WorkToUser.sort_all()
    find_get(player)

    if not ReadWriteToJSON.read_json():
        print('\nПо Вашему запросу ничего не найдено')
    else:
        print('\nСписок вакансий отсортированных по зарплате Вы можете посмотреть в файле - vacancies.json')
    print('\nХорошего дня!')


if __name__ == "__main__":
    main()