import requests


def get_user_data():
    """Запрос данных пользователей с Codeforces API"""
    try:
        req = requests.get(
            'https://codeforces.com/api/user.ratedList?activeOnly=false&includeRetired=false')
        if req.status_code == 200 and 'json' in req.headers['content-type']:
            return req.json()["result"]
        else:
            print('Ошибка: Не удалось получить корректный ответ от API.')
            return None
    except:
        print('Ошибка при запросе к Codeforces API.')
        return None


def get_contest_data(user_handle):
    """Получение информации о контестах для указанного пользователя"""
    try:
        req = requests.get(f'https://codeforces.com/api/user.rating?handle={user_handle}')
        if req.status_code == 200 and 'json' in req.headers['content-type']:
            return req.json()["result"]
        else:
            print(f'Ошибка: Не удалось получить данные о контестах для пользователя {user_handle}.')
            return None
    except:
        print(f'Ошибка при запросе контестов для пользователя {user_handle}.')
        return None


def get_contest_problems(contest_id):
    """Получение списка задач из контеста"""
    try:
        req = requests.get(f'https://codeforces.com/api/contest.standings?contestId={contest_id}')
        if req.status_code == 200 and 'json' in req.headers['content-type']:
            problems = req.json()["result"]["problems"]
            return problems
        else:
            print(f'Ошибка: Не удалось получить задачи для контеста {contest_id}.')
            return None
    except:
        print(f'Ошибка при запросе задач для контеста {contest_id}.')
        return None


def count_users_by_rank(users):
    """Подсчет пользователей по рангам"""
    ranks = {}
    for user in users:
        rank = user["rank"]
        if rank not in ranks:
            ranks[rank] = 0
        ranks[rank] += 1

    for rank, count in ranks.items():
        print(f'{rank}: {count}')


def count_newbies_above_rating(users, cur_rating):
    """Подсчет новичков с рейтингом выше заданного"""
    newbies_count = sum(1 for user in users if user["rank"] == 'newbie' and user["rating"] >= cur_rating)
    print(f'Количество новичков с рейтингом выше {cur_rating}: {newbies_count}')


def filter_users_by_rating_range(users, min_rating, max_rating):
    """Фильтрация пользователей по диапазону рейтинга"""
    filtered_users = [user for user in users if min_rating <= user["rating"] <= max_rating]
    print(f'Пользователи с рейтингом от {min_rating} до {max_rating}:')
    for user in filtered_users:
        print(f'Handle: {user["handle"]}, Rating: {user["rating"]}, Rank: {user["rank"]}')


def search_user_by_handle(users, handle):
    """Поиск пользователя по handle"""
    for user in users:
        if user["handle"] == handle:
            print(f'Найден пользователь: {user["handle"]}, Rating: {user["rating"]}, Rank: {user["rank"]}')
            return
    print(f'Пользователь с handle {handle} не найден.')


def display_contests_with_problems(user_handle, problem_rating):
    """Вывод контестов, в которых были задачи с рейтингом равным введённому"""
    contests = get_contest_data(user_handle)
    if not contests:
        return

    print(f'\nContests for user {user_handle} with problems rated {problem_rating}:')
    for contest in contests:
        contest_id = contest['contestId']
        contest_name = contest['contestName']

        # Получаем список задач контеста
        problems = get_contest_problems(contest_id)
        if not problems:
            continue

        # Фильтруем задачи по рейтингу
        filtered_problems = [p for p in problems if p.get('rating') == problem_rating]
        if filtered_problems:
            print(f'\nContest ID: {contest_id}, Contest Name: {contest_name}')
            for problem in filtered_problems:
                print(f"Problem: {problem['name']}, Rating: {problem['rating']}, Index: {problem['index']}")


def main():
    users = get_user_data()
    if not users:
        return

    while True:
        print("\nВыберите функцию:")
        print("1. Подсчет пользователей в каждом ранге")
        print("2. Подсчет новичков с рейтингом выше заданного")
        print("3. Фильтрация по диапазону рейтинга")
        print("4. Поиск пользователя по handle")
        print("5. Получение информации о контестах для пользователя с задачами по рейтингу")
        print("6. Выход")
        choice = input("Введите номер функции: ")

        if choice == '1':
            count_users_by_rank(users)
        elif choice == '2':
            cur = int(input('Введите минимальный рейтинг: '))
            count_newbies_above_rating(users, cur)
        elif choice == '3':
            min_rating = int(input('Введите минимальный рейтинг: '))
            max_rating = int(input('Введите максимальный рейтинг: '))
            filter_users_by_rating_range(users, min_rating, max_rating)
        elif choice == '4':
            handle = input('Введите handle пользователя: ')
            search_user_by_handle(users, handle)
        elif choice == '5':
            handle = input('Введите handle пользователя: ')
            problem_rating = int(input('Введите рейтинг задачи: '))
            display_contests_with_problems(handle, problem_rating)
        elif choice == '6':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите от 1 до 6.")


if __name__ == "__main__":
    main()
