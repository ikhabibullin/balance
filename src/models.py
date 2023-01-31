import uuid

from sqlalchemy import Column, CheckConstraint, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import Base


class Balance(Base):
    __tablename__ = 'balance'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    money = Column(Integer, default=0, nullable=False)
    reserved = relationship('Reserved')

    __table_args__ = (CheckConstraint(money >= 0, name='balance_money_positive_constraint'),)

    @classmethod
    def returning(cls):
        return [cls.id, cls.user_id, cls.money]


class Reserved(Base):
    __tablename__ = 'reserved'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance_id = Column(UUID(as_uuid=True), ForeignKey('balance.id'), nullable=False)
    money = Column(Integer, nullable=False)
    service_id = Column(UUID(as_uuid=True), nullable=False)
    order_id = Column(UUID(as_uuid=True), nullable=False)

    __table_args__ = (CheckConstraint(money >= 0, name='reserved_money_positive_constraint'),)
