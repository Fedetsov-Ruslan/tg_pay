from sqlalchemy import Date, String, Integer,  ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date



class Base(DeclarativeBase):
    pass
    
class Category(Base):
    __tablename__ = "category"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    

class Subcategory(Base):
    __tablename__ = "subcategory"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    
    def __repr__(self):
        return f"<Subcategory {self.id} {self.name} {self.category_id}>"
    

class Good(Base):
    __tablename__ = "good"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(255), nullable=False)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategory.id"), nullable=False)
    
    def __repr__(self):
        return f"<Good {self.id} {self.name} {self.subcategory_id}>"


class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created: Mapped[Date] = mapped_column(Date, default=date.today())
    updated: Mapped[Date] = mapped_column(Date, default=date.today(), onupdate=date.today())
    
class Cart(Base):
    __tablename__ = "cart"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    good_id: Mapped[int] = mapped_column(ForeignKey("good.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    created: Mapped[Date] = mapped_column(Date, default=date.today())
    updated: Mapped[Date] = mapped_column(Date, default=date.today(), onupdate=date.today())