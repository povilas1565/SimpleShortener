Simple Shortener

Работает на Python 3.9.x и Django 3.1.13.

Цели проекта
------------

Данный проект выполнялся в рамках тестового задания.
Формулировка задания:

*Наша компания отправляет СМС с трекинговой ссылкой, но ссылка достаточно длинная и из-за этого СМС выходит за 70 символов (длина 1 СМС).Необходимо спроектировать сервис-укорачиватель ссылок, чтобы сэкономить деньги компании.*

Ключевые моменты разработки проекта
-----------------------------------

1. **Структура приложения**.

Элементарный микросервис. Короткую ссылку можно получить GET запросом из другого сервиса.

2. **Основной инструмент**

Фреймворк Django 3.

Django выбран в качестве рабочего фреймворка в целях демонстрации потенциальному работодателю своих навыков разработки на Django.
Под указанную структуру приложения лучше подошли бы минималистичные Flask или FastAPI.

3. **Структура данных и хранилище**.

Выбрана реляционная СУБД (конкретно - PostgreSQL), так как предполагается, что структура данных будет однородна, а, значит, схема данных может быть заранее определена и жестко зафиксирована.

P.S При выбранном механизме укорачивания ссылок можно было бы обойтись без базы данных, просто формировав id и сохраняя его в кэш, а затем генерируя из него строку для короткой ссылки.

4. **Механизм укорачивания ссылок**.

Рассматривалось 2 варианта.
- 1 вариант.

Просто использовать хэширование длинной строки в короткую.

*Плюсы*: просто, ссылки непоследовательны, а значит, приватны.

*Минусы*: есть вероятность возникновения коллизий, в этом случае можно предварительно проверять существование короткой ссылки в БД и генерировать новую, в случае существования. Однако при увеличении числа записей в БД, вероятность коллизий будет увеличиваться, соответственно, увеличится общее время на проверку и создание новой уникальной строки.

- 2 вариант.

Использовать id ссылки, который формируется в БД, и конвертировать его в строку с определенной минимальной длиной.

*Плюсы*: для уникального id создается уникальная ссылка, не нужно дополнительно проверять в БД; в случае утери данных БД, можно легко сгенерировать заново по созданному алгоритму; для получения длинной ссылки можно переводить ссылку обратно в id БД и обращаться к нему, т.е индексы БД занимают меньше места.

*Минусы*: без соли ссылки не приватны, их можно конвертировать обратно в id, таким образом, получив доступ к любой ссылке.
Выбран 2 вариант, т.к его использование не предусматривает возникновения коллизий в случае одинаковой соли для каждой сгенерированной строки.

5. **Деплой.**

Приложение разворачивается в контейнерах Docker.

Настройки проекта
-----------------

Чтобы запустить проект локально и на продакшене, нужно чтобы были заполнены .env файлы с настройками Django и БД Postgres.

    $ cd .envs

    $ tree -a

      $ ├── .local
      $ └── .postgres
      $ └── .production
      $     ├── .django
      $     └── .postgres

Запуск проекта локально (в среде разработки)
--------------------------------------------

1.  Убедитесь,чтобы  PostgreSQL, Docker, Docker-compose, Git были установлены на вашей машине.

2.  В установленной и активированной среде окружения Python выполните:

        $ pip install -r requirements/local.txt

3.  Выполните миграции Django:

        $ docker-compose -f local.yml run --rm django python manage.py migrate

4.  Разверните и запустите проект через docker-compose:

        $ docker-compose -f local.yml up --build -d

Запуск проекта на продакшене
----------------------------

1.  Убедитесь,чтобы  PostgreSQL, Docker, Docker-compose, Git были установлены на вашей машине.

2.  Перенесите на сервер файл с настройками .envs/.production

3.  Выполните миграции Django:

        $ docker-compose -f production.yml run --rm django python manage.py migrate

4.  Разверните и запустите проект через docker-compose:

        $ docker-compose -f production.yml up --build -d
