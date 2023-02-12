import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models import Balance, Reserved, StatusEnum
from services import BalanceService


async def test_add_money_create(session):
    bs = BalanceService(session=session, user_id=uuid.uuid4())
    money_to_add = 1

    await bs.add_money(money_to_add)

    stmt = select(Balance).filter(Balance.user_id == bs.user_id)
    balance = (await session.execute(stmt)).scalar_one_or_none()

    assert balance is not None
    assert balance.money == money_to_add


async def test_add_money(session, balance):
    bs = BalanceService(session=session, user_id=balance.user_id)
    money_to_add = 1

    await bs.add_money(money_to_add)

    stmt = select(Balance).filter(Balance.user_id == bs.user_id)
    new_balance = (await session.execute(stmt)).scalar_one_or_none()

    assert new_balance.money == balance.money + money_to_add


async def test_add_money_fail(session):
    bs = BalanceService(session=session, user_id=uuid.uuid4())
    money_to_add = -1

    with pytest.raises(IntegrityError):
        await bs.add_money(money_to_add)


async def test_reserve(session, balance):
    bs = BalanceService(session=session, user_id=balance.user_id)
    money_to_reserve = 1

    await bs.reserve_money(money=money_to_reserve, service_id=uuid.uuid4(), order_id=uuid.uuid4())

    stmt = select(Balance).filter(Balance.user_id == bs.user_id)
    new_balance = (await session.execute(stmt)).scalar_one_or_none()
    stmt = select(Reserved).filter(Reserved.balance_id == bs.user_id)
    reserved = (await session.execute(stmt)).scalar_one_or_none()

    assert new_balance.money == balance.money - money_to_reserve
    assert reserved is not None
    assert reserved.money == money_to_reserve


async def test_reserve_fail(session, balance):
    bs = BalanceService(session=session, user_id=balance.user_id)
    money_to_reserve1 = -1
    money_to_reserve2 = balance.money + 1

    with pytest.raises(IntegrityError):
        await bs.reserve_money(money=money_to_reserve1, service_id=uuid.uuid4(), order_id=uuid.uuid4())
        await bs.reserve_money(money=money_to_reserve2, service_id=uuid.uuid4(), order_id=uuid.uuid4())


async def test_get_balance(session, balance):
    bs = BalanceService(session=session, user_id=balance.user_id)

    b = await bs.get_balance()

    assert b is not None
    assert b.user_id == balance.user_id


async def test_get_balance_fail(session, balance):
    bs = BalanceService(session=session, user_id=uuid.uuid4())

    b = await bs.get_balance()

    assert b is None


async def test_accept_reserved(session, reserved):
    bs = BalanceService(session=session, user_id=reserved.balance_id)

    row = await bs.accept_reserved(reserved.id)

    assert row.status == StatusEnum.accepted


async def test_reject_reserved(session, reserved):
    bs = BalanceService(session=session, user_id=reserved.balance_id)

    row = await bs.reject_reserved(reserved.id)

    assert row.status == StatusEnum.rejected
