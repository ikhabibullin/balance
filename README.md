# balance

## Поднять сервисы и Запустить локально
~~~
sh scripts/prepare_for_launch.sh
uvicorn src.main:app --reload
~~~

## Поднять сервисы (postgresql, rabbitmq, redis, celery, flower), конфиги в .env
~~~
docker-compose up -d --build
~~~

## Запустить анализаторы кода
~~~
sh scripts/lint.sh
~~~

## Форматировать код
~~~
sh scripts/format.sh
~~~

## Запустить тесты
~~~
pytest -v
~~~
