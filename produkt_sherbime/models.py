from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, Text
from datetime import datetime
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)          # Better than Float
    category = Column(String, nullable=False, index=True)    # e.g. IDE, Security, Utility
    version = Column(String, nullable=True)
    license_type = Column(String, default="lifetime")        # lifetime, subscription, one_time
    is_active = Column(Boolean, default=True)
    stock = Column(Integer, default=9999)                    # High default for digital
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
