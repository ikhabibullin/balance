from pydantic import UUID4, PositiveInt
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.models import ReserveIn
from db import async_session
from models import Balance, Reserved


async def add_money(user_id: UUID4, money: PositiveInt, session: AsyncSession):
    values = {'user_id': user_id, 'money': money}

    insert_q = insert(Balance).values(values)
    do_update_q = insert_q.on_conflict_do_update(
        constraint='balance_user_id_key', set_={'money': Balance.money + money}
    ).returning(*Balance.returning())

    result = await session.execute(do_update_q)
    return result.fetchone()


async def reserve_money(data: ReserveIn):
    # TODO: можно объект сессии получать в Depend в route, что лучше
    async with async_session() as session:
        async with session.begin():
            select_balance = select(Balance).filter(Balance.user_id == data.user_id).with_for_update()
            raw = await session.execute(select_balance)
            balance = raw.scalar_one_or_none()
            if not balance:
                # TODO: переделать
                return 'Нет баланса такого пользователя'

            if balance.money >= data.money:
                balance.money -= data.money
                session.add(balance)

                values = {
                    'money': data.money,
                    'order_id': data.order_id,
                    'service_id': data.service_id,
                    'balance_id': balance.id,
                }
                insert_reserve = (
                    insert(Reserved)
                    .values(values)
                    .returning(Reserved.id, Reserved.money, Reserved.balance_id, Reserved.service_id, Reserved.order_id)
                )
                reserve = (await session.execute(insert_reserve)).fetchone()
                return reserve
            else:
                # TODO: переделать
                return 'Недостаточно средств'
