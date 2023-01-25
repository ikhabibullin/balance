# balance

## Запустить локально
~~~
poetry install
poetry shell
uvicorn src.main:app --reload
~~~

## Запустить анализаторы кода
~~~
sh lint.sh
~~~

## Форматировать код
~~~
sh format.sh
~~~

## Запустить тесты
~~~
pytest -v
~~~
