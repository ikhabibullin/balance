import json
import uuid

import httpx


def test_add_money_create():
    data = {
        'user_id': str(uuid.uuid4()),
        'money': 5
    }

    response = httpx.post('http://127.0.0.1:8000/add-money', data=json.dumps(data))
    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get('id') is not None
    assert response_data.get('user_id') == data['user_id']
    assert response_data.get('money') == data['money']


def test_add_money_increment():
    data = {
        "user_id": str(uuid.uuid4()),
        'money': 1
    }
    _range = 2

    for i in range(_range):
        response = httpx.post('http://127.0.0.1:8000/add-money', data=json.dumps(data))
        response_data = response.json()

    assert response_data.get('money') == data['money'] * _range


def test_add_money_fail():
    data = {
        "user_id": str(uuid.uuid4()),
        'money': -1
    }

    response = httpx.post('http://127.0.0.1:8000/add-money', data=json.dumps(data))

    assert response.status_code == 422
