import uuid

from sqlalchemy import Column, CheckConstraint, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import Base


class Balance(Base):
    # todo: created_at, updated_at
    __tablename__ = 'balance'

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    money = Column(Integer, default=0, nullable=False)
    reserved = relationship('Reserved')

    __table_args__ = (CheckConstraint(money >= 0, name='balance_money_positive_constraint'),)

    @classmethod
    def returning(cls):
        return [cls.user_id, cls.money]


class Reserved(Base):
    # TODO: добавить create_at, update_at
    __tablename__ = 'reserved'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance_id = Column(UUID(as_uuid=True), ForeignKey('balance.user_id'), nullable=False)
    money = Column(Integer, nullable=False)
    service_id = Column(UUID(as_uuid=True), nullable=False)
    order_id = Column(UUID(as_uuid=True), nullable=False)

    __table_args__ = (CheckConstraint(money >= 0, name='reserved_money_positive_constraint'),)

    @classmethod
    def returning(cls):
        return [cls.id, cls.balance_id, cls.money, cls.service_id, cls.order_id]
