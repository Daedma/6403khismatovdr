# Задание на лабораторную работу №1
## Подготовка
- Создать приватной репозиторий на GitHub.
- Наименовать репозиторий по следующим правилам: группафамилияио на латинице. Например, репозиторий Иванова Алексея Петровича из группы 6409 будет `6409ivanovap`.
- Добавить в Settings → Collaborators → Add people профиль `amacomm`.
- Результирующий код разметить в своем репозитории на GitHub.
- Под выполнение каждой лабораторной работы необходимо создавать отдельную ветку.
- После выполнения задания создать PullRequest, в качестве проверяющего установить пользователя `amacomm`.
- Установить пакет виртуального окружения python – `pipenv`.
- В проекте сделать виртуальное окружение `python -m venv .venv`
- Папку `.venv` добавить в `.gitignore`.
- Пакеты проекта должны ставиться в виртуальное окружение с помощью `pipenv`.

Необязательное:

В глобальное окружение установить линтер и его расширения: ```flake8 flake8-builtins flake8-bugbear flake8-commas flake8-eradicate flake8-variables-names pep8-naming flake8-docstring-checker flake8-annotations flake8-nb flake8-import-order flake8-docstrings-complete flake8-clean-block```
В конфиг файле flake8 прописать: ```max-line-length = 120```

## Задание
Вычислить значение функции y в диапазоне x = [от n0, с шагом h, до nk], результаты записать в файл results. Переменны должны считываться из файла config, формат файла определяется согласно варианту задания. Для считывания данных из config реализовать парсер файла. Предусмотреть возможность задание параметров как аргументов запускаемого py файла через консоль.

Считываемые данные из конфиг файла: n0, h, nk, a, b, c. Можете дополнить по своему усмотрению.

## Вариант задания
|№|Функция y| Формат конфига|
|-| ------- | ------------- |
|2|$a(\sin{bx} - \cos^2{cx})$|json|