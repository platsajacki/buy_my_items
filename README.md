# Веб-приложение "BUY MY ITEMS"

Автор: [Vyacheslav Menyukhov](https://github.com/platsajacki) | menyukhov@bk.ru

Спасибо за тестовое задние компании ООО "Ришат"! Сайт доступен по ссылке: [BUY MY ITEMS](https://bmi-rishat.ddns.net/)

Всем моим первым покупателя предоставляется скидка по купонам:
1. `first` - 11%
2. `second` - 1%

## Описание
Приложение дает возможность приобретать разнообразные товары. Данные о покупках записываются в базу, после проведения или отмены платежа данные обновляются с помощью webhook.

## Endpoints
1. **items/** - главная страница, на которой сразу можно приобрести несколько товаров. На странице доступны фильтрация по валюте и применение купопа скидки к заказу.

2. **items/int:id/** - отдельная страница товара с описанием, на которой можно применить купон скидки и купить товар.

3. **purchases/** - обрабатывает все покупки.

4. **succeed-order/** - страница, открывающаяся после успешной оплаты.

5. **coupons/str:discount_id/** - проверяет актуальность скидки и возвращает данные о ней.

6. **webhook/** - обрабатывает события по заказу и актуализирует базу.

## Запуск проекта
1. Склонируйте репозиторий `buy_my_items` на свой компьютер:
    ```bash
    git clone git@github.com:platsajacki/buy_my_items.git
    ```

2. Создайте и заполните файл `.env` по образцу `.env.example`, разместите его в директории проекта.

3. Из директории проекта запустите проект с помощью Docker Compose:
    ```bash
    sudo docker compose up -d
    ```

4. В контейнере с Django проведите миграцию и скопируйте статику:
    ```bash
    sudo docker compose exec bmi python manage.py migrate
    sudo docker compose exec bmi cp -r /app/staticfiles/. /static/
    ```

5. Заполните сайт данными:
    ```bash
    sudo docker compose exec bmi python manage.py import_csv
    ```

6. Для работы в административной панели создайте учетную запись суперпользователя:
    ```bash
    sudo docker compose exec bmi python manage.py createsuperuser
    ```

7. Теперь вы можете обращаться к сервису BMI по адресу: http://127.0.0.1/

## Анализ и тестирование кода
С помощью команды `make lint` можно проанализировать проект на потенциальные ошибки, стилистические несоответствия. А команда `make test` проведет тестирование проекта. P.S. Для этого потребуется установить зависимости из файла с `requirements.txt`.
