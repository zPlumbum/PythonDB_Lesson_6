import datetime
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


def make_connection():
    db_type = input('Укажите тип вашей БД (mysql, postgresql и т.д.): ')
    db_user = input('Укажите User-никнейм: ')
    db_password = input('Введите пароль: ')
    db_port = input('Укажите порт: ')
    db_title = input('Укажите название базы данных: ')

    db_path = f'{db_type}://{db_user}:{db_password}@localhost:{db_port}/{db_title}'

    engine = sq.create_engine(db_path)
    return engine


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String)

    books = relationship('Book', backref='publisher')


book_to_stock = sq.Table(
    'book_to_stock', Base.metadata,
    sq.Column('book_id', sq.Integer, sq.ForeignKey('book.id')),
    sq.Column('stock_id', sq.Integer, sq.ForeignKey('stock.id'))
)


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'))

    stocks = relationship('Stock', secondary=book_to_stock)


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('shop.id'))
    count = sq.Column(sq.Integer)

    book_id = relationship(Book, secondary=book_to_stock)
    sales = relationship('Sale', backref='stock')


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String)

    stocks = relationship(Stock, backref='shop')


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer)
    date_sale = sq.Column(sq.DateTime, default=datetime.date.today())
    stock_id = sq.Column(sq.Integer, sq.ForeignKey('stock.id'))
    count = sq.Column(sq.Integer)


if __name__ == '__main__':
    engine = make_connection()
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()

    input_name = input('Пожалуйста, введите имя издателя: ')

    result = session.query(Book.title).join(Publisher).join(book_to_stock).join(Stock).join(Shop).filter(Publisher.name == input_name).all()
    print(result)
