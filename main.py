import argparse
import os

#Функция, для того, что бы проверить положительны ли числа при вводе количества подстрок фильтрации

def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"Глубина анализа должна быть положительным числом, получено: {value}")
    return ivalue

#Функция для поиска ошибок при вводе агрументов

def errors_check(args):

    errors = []

    if args.repo_path and not os.path.exists(args.repo_path):
        errors.append(f"Указанный путь к репозиторию не существует: {args.repo_path}")

    if args.repo_path and not os.path.isdir(args.repo_path):
        errors.append(f"Указанный путь не является директорией: {args.repo_path}")

    return errors

#Создание парсера и настройка его аргументов
#python main.py lalala  --repo-url "ссылка на lalala" --test --tree

parser = argparse.ArgumentParser(description='Анализ пакетов на Python')

parser.add_argument('package_name', type=str, help='Имя анализируемого пакета')

source_group = parser.add_mutually_exclusive_group(required=True)

source_group.add_argument('--repo-url', '-u', type=str, help='URL-адресс анализируемого пакета')
source_group.add_argument('--repo-path', '-p', type=str, help='Путь к локальной копии тестового репозитория')

parser.add_argument('--test', '-t', action='store_true', help='Включить режим работы с тестовым репозиторием')
parser.add_argument('--tree', action='store_true', help='Вывести зависимости в формате ASCII-дерева')
parser.add_argument('--max-depth', '-d', type=positive_int, default=3, help='Максимальная глубина анализа зависимостей')
parser.add_argument('--filter', '-f', type=str, default='', help='Подстрока для фильтрации пакетов (только пакеты, содержащие эту подстроку)')


args = parser.parse_args()

#Вывод ошибок в аргументах, если они есть

errors = errors_check(args)
if errors:
    print("Ошибки валидации аргументов:")
    for error in errors:
        print(f"  - {error}")
    exit(1)

#Вывод параметров

print("!!! НАСТРОЙКИ !!!")
print(f"Имя анализируемого пакета: {args.package_name}")

if args.repo_url:
    print(f"URL-ссылка на пакет: {args.repo_url}")
else:
    print(f"Путь к пакету: {args.repo_path}")

print(f"Режим тестового репозитория: {'Включен' if args.test else 'Выключен'}")
print(f"Режим вывода в виде дерева: {'Включен' if args.tree else 'Выключен'}")
print(f"Максимальная глубина анализа: {args.max_depth}")
print(f"Подстрока для фильтрации: '{args.filter}'" if args.filter else "Подстрока для фильтрации: не задана")