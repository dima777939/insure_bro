# Приложение "Застрахуй братуху"

Биржа продажи услуг страховых компаний

## Основной функционал
У нас есть два типа пользователей - страховые компании которые могут конфигурировать и размещать свои услуги,
и есть покупатели - люди которые хотят что-либо застраховать.
У страховых компаний есть личный кабинет где они могут конфигурировать свои продукты - указывать процентные ставки, сроки, категории(недвижимость, авто, жизнь).
А также просматривать данные по откликам на их продукты.
У покупателей(не авторизованные пользователи) есть грид с услугами всех компаний и всевозможными фильтрами по ним.
У покупателей есть возможность откликнуться на предложение страховой комании указав свою контактную информацию(ФИО, телефон, почту)

## Основные технологии
* Python
* Django
* Docker Compose
* Elasticsearch
* Celery
* RabbitMQ
* Redis

## Основные команды

Сборка образа Docker'a

```docker-compose build```

Запуск контейнеров Docker

```docker-compose up -d```

## Команды для первой инициализации приложения

Сборка миграций в базу данных

```docker-compose exec web  python /usr/src/insure_bro/manage.py makemigrations```

Применение миграций

```docker-compose exec web  python /usr/src/insure_bro/manage.py migrate```

Создание индексов elasticsearch

```docker-compose exec web /usr/src/insure_bro/manage.py search_index --rebuild```

##Тестирование

```docker-compose exec web  python /usr/src/insure_bro/manage.py test cabinet.tests```

```docker-compose exec web  python /usr/src/insure_bro/manage.py test account.tests```


## Дополнительно

Для тестирования функционала можно загрузить фикстуры в базу данных 

```docker-compose exec web  python /usr/src/insure_bro/manage.py loaddata mydata.json```

после загрузки фикстур необходимо добавить url на страницу просмотра информации продукта в Redis

```docker-compose exec web  python /usr/src/insure_bro/manage.py add_redis_url_key```

Также становятся доступными учётные записи с логином

* admin@admin.com (имеет доступ в админку)
* sity@sity.com

( пароль для всех ```qwerty``` )

_________________________________


Если не загружать фикстуры то необходимо сделать учетку aдминистратора 

```docker-compose exec web /usr/src/insure_bro/manage.py createsuperuser```

и в админке джанго в таблице ```Категории```  сделать несколько записей

