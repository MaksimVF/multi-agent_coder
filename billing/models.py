

from datetime import datetime
import uuid
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class TariffPlan(Base):
    __tablename__ = 'tariff_plan'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price_per_month = Column(Float, nullable=False)
    included_credits = Column(Float, default=0.0)
    max_team_members = Column(Integer, default=1)
    member_price = Column(Float, default=0.0)
    discounts = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    components = relationship('TariffComponent', secondary='tariff_components', backref='tariffs')

class OrganizationBalance(Base):
    __tablename__ = 'organization_balance'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), nullable=False)  # Would be ForeignKey in a full implementation
    tariff_plan_id = Column(String(36), ForeignKey('tariff_plan.id'), nullable=False)
    balance = Column(Float, default=0.0)
    team_members = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tariff_plan = relationship('TariffPlan')

class TariffComponent(Base):
    __tablename__ = 'tariff_component'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    unit_type = Column(String(50), nullable=False)  # tokens, calls, etc.
    price_per_unit = Column(Float, nullable=False)
    is_premium = Column(Boolean, default=False)
    is_exclusive = Column(Boolean, default=False)
    exclusive_tariffs = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Association table for tariff components
tariff_components = Table('tariff_components', Base.metadata,
    Column('tariff_id', String(36), ForeignKey('tariff_plan.id'), primary_key=True),
    Column('component_id', String(36), ForeignKey('tariff_component.id'), primary_key=True),
    Column('included_units', Integer, default=0)
)

