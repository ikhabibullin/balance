import json
import uuid


URL = 'http://localhost:8000'


async def test_add_money_create(async_client, session):
    data = {'user_id': str(uuid.uuid4()), 'money': 5}

    response = await async_client.post('/add-money', data=json.dumps(data))
    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get('user_id') == data['user_id']
    assert response_data.get('money') == data['money']


async def test_add_money_fail(async_client):
    data = {'user_id': str(uuid.uuid4()), 'money': -1}

    response = await async_client.post('/add-money', data=json.dumps(data))

    assert response.status_code == 422


async def test_reserve(async_client, session, balance):
    data = {
        'user_id': str(balance.user_id),
        'money': 1,
        'order_id': str(uuid.uuid4()),
        'service_id': str(uuid.uuid4()),
    }

    response = await async_client.post('/reserves', data=json.dumps(data))
    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get('money') == data['money']
    assert response_data.get('balance_id') == data['user_id']


async def test_reserve_fail(async_client, session, balance):
    data1 = {
        'user_id': str(uuid.uuid4()),
        'money': 1,
        'order_id': str(uuid.uuid4()),
        'service_id': str(uuid.uuid4()),
    }
    data2 = {**data1, 'money': -1}
    data3 = {**data1, 'money': balance.money + 1}

    response1 = await async_client.post('/reserves', data=json.dumps(data1))
    response2 = await async_client.post('/reserves', data=json.dumps(data2))
    response3 = await async_client.post('/reserves', data=json.dumps(data3))

    assert response1.status_code == 404
    assert response2.status_code == 422
    assert response3.status_code == 404


async def test_get_balance(async_client, session, balance):
    response = await async_client.get(f'/{balance.user_id}')
    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get('user_id') == str(balance.user_id)
    assert response_data.get('money') == balance.money


async def test_get_balance_fail(async_client, session):
    response = await async_client.get(f'/{uuid.uuid4()}')

    assert response.status_code == 404
