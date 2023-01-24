# balance

## Запустить локально
~~~
poetry install
poetry shell
uvicorn src.main:app --reload
~~~

## Запустить анализаторы кода
~~~
flake8 src && black --check src && autoflake --check -r src
~~~

## Форматировать код
~~~
autoflake -r src && black src
~~~

## Запустить тесты
~~~
pytest -v
~~~
