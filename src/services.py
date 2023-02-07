from fastapi import HTTPException
from pydantic import UUID4, PositiveInt
from sqlalchemy import select, Row
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Balance, Reserved


class BalanceService:
    def __init__(self, session: AsyncSession, user_id: UUID4):
        self.session = session
        self.user_id = user_id
        self.balance = None

    async def _get_balance(self, money: PositiveInt):
        select_balance = (
            select(Balance).filter(Balance.user_id == self.user_id, Balance.money >= money).with_for_update()
        )
        raw = await self.session.execute(select_balance)
        balance = raw.scalar_one_or_none()
        self.balance = balance

    async def _reserve_money_in_db(self, money: PositiveInt, service_id: UUID4, order_id: UUID4) -> Row:
        self.balance.money -= money
        self.session.add(self.balance)

        values = {
            'money': money,
            'order_id': order_id,
            'service_id': service_id,
            'balance_id': self.balance.user_id,
        }
        insert_reserve = insert(Reserved).values(values).returning(*Reserved.returning())
        reserve = (await self.session.execute(insert_reserve)).fetchone()
        return reserve

    async def add_money(self, money: PositiveInt) -> Row:
        values = {'user_id': self.user_id, 'money': money}

        insert_q = insert(Balance).values(values)
        do_update_q = insert_q.on_conflict_do_update(
            constraint='balance_pkey', set_={'money': Balance.money + money}
        ).returning(*Balance.returning())

        result = await self.session.execute(do_update_q)
        row = result.fetchone()

        return row

    async def reserve_money(self, money: PositiveInt, service_id: UUID4, order_id: UUID4) -> Row:
        await self._get_balance(money)
        if not self.balance:
            raise HTTPException(
                status_code=404,
                detail='Balance пользователя не найден или на нем недостаточно средств для резервирования',
            )

        reserve = await self._reserve_money_in_db(money=money, service_id=service_id, order_id=order_id)
        return reserve
