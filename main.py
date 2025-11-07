import argparse
import os
import urllib.request
import urllib.error
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

def url_to_raw(repo_url):
    possible_urls = [
        repo_url.replace("github.com", "raw.githubusercontent.com") + "/main/Cargo.toml",
        repo_url.replace("github.com", "raw.githubusercontent.com") + "/master/Cargo.toml",
    ]
    for test_url in possible_urls:
        try:
            with urllib.request.urlopen(test_url) as responce:
                if responce.getcode() == 200:
                    return test_url
        except:
            continue
    default_url = possible_urls[0]
    return default_url
def dowload_cargo_toml(raw_url):
    try:
        with urllib.request.urlopen(raw_url) as response:
            cargo_content = response.read().decode('utf-8')
            return cargo_content
    except urllib.error.URLError as e:
        print(f"Ошибка загрузки: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None
def extract_section_with_braces(content, start_pos):
    result = []
    brace_count = 0
    in_section = False


    lines = content[start_pos:].split('\n')

    for line in lines:
        stripped_line = line.strip()

        if not in_section and stripped_line == "[dependencies]":
            in_section = True
            result.append(line)
            continue

        if in_section:
            brace_count += line.count('{')
            brace_count -= line.count('}')

            if stripped_line.startswith('[') and brace_count == 0:
                break

        result.append(line)

    return '\n'.join(result)
            
def dependencies_find(cargo_content):
    deps_start = cargo_content.find("[dependencies]")
    if deps_start != -1:
#print("*Секция [dependencies] найдена!")
        deps_content = extract_section_with_braces(cargo_content, deps_start)
        print("---Прямые зависимости пакета:")
        print(deps_content)
    else:
        print("Секция [dependencies] не найдена")

def main():
    raw_url = url_to_raw(args.repo_url)
    cargo_content = dowload_cargo_toml(raw_url)
   
    print( dependencies_find(cargo_content))
main()