"""
Playing around with some basic features of the SQLalchemy ORM model
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///orm.db')
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return f'<User(id={self.id}, name={self.name}, fullname={self.fullname}, nickname={self.nickname})>'


def add_users():
    """
    The bulk method does not 'respect' the database:
        * no PKs are generated
        * objects are not added to the session
        * related tables are not updated
    The only advantage is increased speed
    """
    user_bill = User(name='William', fullname='William W', nickname='Bill')
    user_dan = User(name='Daniel', fullname='Daniel N', nickname='Dan')
    user_anto = User(name='Antonia', fullname='Antonia GA', nickname='Anto')

    session.add(user_bill)
    session.add_all([user_dan, user_anto])
    # session.bulk_save_objects([user_bill, user_dan, user_anto])

    # session.commit()
    # print(user_bill)
    # print(user_dan)
    # print(user_anto)


def get_users():
    # get_bill = session.query(User).filter_by(name='William').first()
    # get_dan = session.query(User).filter_by(name='Daniel').first()
    # get_anto = session.query(User).filter_by(name='Antonia').first()

    get_bill = session.query(User).filter(User.name == 'William').first()
    get_dan = session.query(User).filter(User.name == 'Daniel').first()
    get_anto = session.query(User).filter(User.name == 'Antonia').first()
    print(get_bill)
    print(get_dan)
    print(get_anto)


def del_users():
    get_bill = session.query(User).filter_by(name='William').first()
    get_dan = session.query(User).filter_by(name='Daniel').first()
    get_anto = session.query(User).filter_by(name='Antonia').first()

    session.delete(get_bill)
    session.delete(get_dan)
    session.delete(get_anto)
    session.commit()


def print_users():
    for name, fullname in session.query(User.name, User.fullname):
        print(f'{name}, {fullname}')


def print_all_users():
    users = session.query(User).all()
    print(users)


def print_users_ordered():
    for user in session.query(User).order_by(User.name):
        print(user.name)


def print_like():
    # Potentially case sensitive
    for user in session.query(User).filter(User.name.like('%an%')):
        print(user.name)

    # Case insensitive
    for user in session.query(User).filter(User.name.ilike('%an%')):
        print(user.name)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()

    add_users()
    # get_users()
    # del_users()
    # print_users()
    # print_all_users()
    # print_users_ordered()
    print_like()
