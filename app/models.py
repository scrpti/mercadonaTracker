from sqlalchemy import Column, String, Text, Numeric, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(String(20), primary_key=True)
    display_name = Column(Text, nullable=False)
    brand = Column(Text)
    packaging = Column(Text)
    unit_size = Column(Numeric)
    size_format = Column(String(20))
    share_url = Column(Text)
    thumbnail = Column(Text)
    slug = Column(Text)

class ProductPrice(Base):
    __tablename__ = "product_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(20), ForeignKey("products.id"), nullable=False)
    price_date = Column(Date, nullable=False)
    unit_price = Column(Numeric(10,2), nullable=False)
    reference_price = Column(Numeric(10,3))
    reference_format = Column(String(20))
    bulk_price = Column(Numeric(10,2))

    __table_args__ = (
        UniqueConstraint("product_id", "price_date", name="uq_product_price_date"),
    )


