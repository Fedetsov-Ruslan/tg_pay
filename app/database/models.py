from sqlalchemy import DateTime,Date, String, func, Integer,  ForeignKey, Enum, ARRAY, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date



class Base(DeclarativeBase):
    # created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    # updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
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