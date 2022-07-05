"""
Playing around with SQLalchemy ORM model

https://www.youtube.com/watch?v=399c-ycBvo4&ab_channel=NextDayVideoNextDayVideo
https://www.youtube.com/watch?v=51RpDZKShiw&ab_channel=NextDayVideo
https://docs.sqlalchemy.org/en/14/orm/tutorial.html
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


Base = declarative_base()
engine = create_engine('sqlite:///orm.db')
Session = sessionmaker(bind=engine)


class User(Base):
    """
    User object unique to an individual
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    forename = Column(String(64))
    surname = Column(String(64))
    nickname = Column(String(64))

    def __repr__(self):
        return f'<User(user_id={self.user_id}, forename={self.forename}, ' \
               f'surname={self.surname}, nickname={self.nickname})>'


class Address(Base):
    """
    Address object for each individual
        * Email address
        * Postal address
    """
    __tablename__ = 'addresses'

    address_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    address_type = Column(String(64))
    address = Column(String(64))

    user = relationship('User', back_populates='addresses')

    def __repr__(self):
        return f'<User(user_id={self.user_id}, address_id={self.address_id}, ' \
               f'address_type={self.address_type}, address={self.address})>'


def add_users():
    session.add_all(
        [
            User(forename='Richard', surname='Bacon', nickname='Dick'),
            User(forename='Jonathan', surname='Patty', nickname='Jon'),
            User(forename='Charlotte', surname='Lamb', nickname='Lottie')
        ]
    )
    # session.commit()


def del_users():
    [session.delete(user) for user in session.query(User)]
    # session.commit()


def print_users():
    for forename, surname in session.query(User.forename, User.surname):
        print(f'{surname}, {forename}')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()
    User.addresses = relationship(
        'Address',
        order_by=Address.address_id,
        back_populates='user'
    )

    add_users()
    # del_users()
    print_users()


""" 
https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying
https://www.youtube.com/watch?v=51RpDZKShiw&ab_channel=NextDayVideo  17:30
"""
