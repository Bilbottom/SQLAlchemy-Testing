"""
Cookie database as per the Jason Myers presentation -- straight copy
    https://www.youtube.com/watch?v=51RpDZKShiw&t=1535s&ab_channel=NextDayVideo
    https://www.slideshare.net/jamdatadude/introduction-to-sqlalchemy-orm

Automap -- for converting database into SQLAlchemy classes
    https://docs.sqlalchemy.org/en/14/orm/extensions/automap.html
"""

from sqlalchemy import\
    create_engine,\
    func, desc, or_,\
    ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Cookie(Base):
    __tablename__ = 'cookies'

    cookie_id = Column(Integer, primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))  # stock-keeping unit
    quantity = Column(Integer())
    unit_cost = Column(Integer())

    def __repr__(self):
        # return f"Cookie(cookie_id={self.cookie_id}, cookie_name='{self.cookie_name}', " \
        #        f"cookie_recipe_url='{self.cookie_recipe_url}', cookie_sku='{self.cookie_sku}', " \
        #        f"quantity={self.quantity}, unit_cost={self.unit_cost})"
        return f"Cookie(cookie_id={self.cookie_id}, cookie_name='{self.cookie_name}', " \
               f"cookie_sku='{self.cookie_sku}', quantity={self.quantity}, unit_cost={self.unit_cost})"


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        # return f"Cookie(user_id={self.user_id}, username='{self.username}', " \
        #        f"email_address='{self.email_address}', phone='{self.phone}', password='{self.password}', " \
        #        f"created_on={self.created_on}, updated_on={self.updated_on})"
        return f"User(user_id={self.user_id}, username='{self.username}', " \
               f"email_address='{self.email_address}', phone='{self.phone}')"


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.user_id'))
    shipped = Column(Boolean(), default=False)

    user = relationship("User", backref=backref('orders', order_by=order_id))

    def __repr__(self):
        return f"Order(order_id={self.order_id}, user_id='{self.user_id}', shipped={self.shipped})"


class LineItem(Base):
    __tablename__ = 'line_items'

    line_item_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.order_id'))
    cookie_id = Column(Integer(), ForeignKey('cookies.cookie_id'))
    quantity = Column(Integer())
    extended_cost = Column(Integer())

    order = relationship("Order", backref=backref('line_items', order_by=line_item_id))
    cookie = relationship("Cookie", uselist=False)

    def __repr__(self):
        return f"LineItem(line_item_id={self.line_item_id}, order_id='{self.order_id}', " \
               f"cookie_id='{self.cookie_id}', quantity={self.quantity}, extended_cost={self.extended_cost})"


def add_cookies(session, verbose: bool = False):
    chocolate_chip = Cookie(
        cookie_name='chocolate chip',
        cookie_recipe_url='https://some.aweso.me/cookie/chocolate.html',
        cookie_sku='CC01',
        quantity=12,
        unit_cost=50
    )
    peanut_butter = Cookie(
        cookie_name='peanut butter',
        cookie_recipe_url='https://some.aweso.me/cookie/peanut.html',
        cookie_sku='PB01',
        quantity=24,
        unit_cost=25
    )
    oatmeal_raisin = Cookie(
        cookie_name='oatmeal raisin',
        cookie_recipe_url='https://some.okay.me/cookie/raisin.html',
        cookie_sku='EWW01',
        quantity=100,
        unit_cost=100
    )

    session.add_all([
        chocolate_chip,
        peanut_butter,
        oatmeal_raisin
    ])
    session.commit()

    if verbose:
        print(
            chocolate_chip.cookie_id,
            peanut_butter.cookie_id,
            oatmeal_raisin.cookie_id
        )


def check_cookies(session):
    # Simple print
    print('\nCookie objects')
    for cookie in session.query(Cookie):
        print('\t', cookie)

    # Ordered print
    print('\nCookies by quantity, descending')
    for cookie in session.query(Cookie).order_by(desc(Cookie.quantity)):
        print('\t{:3} - {}'.format(cookie.quantity, cookie.cookie_name))

    # Database Functions SUM and COUNT
    print('\nSUM and COUNT')
    print('\t', session.query(func.sum(Cookie.quantity)).scalar())
    print('\t', session.query(func.count(Cookie.cookie_name)).first())

    # COUNT with label
    print('\nCOUNT with label')
    rec_count = session.query(func.count(Cookie.cookie_name).label('inventory_count')).first()
    print(f'\tkeys={rec_count.keys()}, inv_count={rec_count.inventory_count}')

    # WHERE statement
    print('\nWHERE statement')
    print(
        '\t',
        session.query(Cookie).filter(
            Cookie.cookie_name == 'chocolate chip'
        ).first()
    )

    # LIKE statement
    print('\nLIKE statement')
    query = session.query(Cookie).filter(Cookie.cookie_name.like('%chocolate%'))
    for record in query:
        print('\t', record.cookie_name)

    # WHERE ... OR
    print('\nWHERE ... OR')
    query = session.query(Cookie).filter(
        or_(
            Cookie.quantity.between(10, 50),
            Cookie.cookie_name.contains('chip')
        )
    )
    for result in query:
        print('\t', result.cookie_name)


def update_cookie(session):
    query = session.query(Cookie)
    cc_cookie = query.filter(Cookie.cookie_name == "chocolate chip").first()
    print('Before:', cc_cookie)
    cc_cookie.quantity = cc_cookie.quantity + 120
    session.commit()
    print('After: ', cc_cookie)


def delete_cookie(session, verbose: bool = False):
    query = session.query(Cookie).filter(Cookie.cookie_name == "peanut butter")
    dcc_cookie = query.one()
    session.delete(dcc_cookie)
    session.commit()
    if verbose:
        print(query.first())


def add_all_objects(session):
    cookie_monster = User(
        username='cookie-monster',
        email_address='mon@cookie.com',
        phone='111-111-1111',
        password='password'
    )
    session.add(cookie_monster)

    order = Order()
    order.user = cookie_monster
    session.add(order)

    line1 = LineItem(
        cookie=session.query(Cookie).filter(
            Cookie.cookie_name == 'chocolate chip'
        ).one(),
        quantity=2,
        extended_cost=1
    )

    line2 = LineItem(quantity=12, extended_cost=3.00)
    line2.cookie = session.query(Cookie).filter(
        Cookie.cookie_name == 'oatmeal raisin'
    ).one()

    order.line_items.append(line1)
    order.line_items.append(line2)
    session.commit()


def check_all_objects(session):
    cookie_monster = session.query(User).filter(User.username == 'cookie-monster').one()
    order = session.query(Order).filter(Order.order_id == 1).one()

    print(cookie_monster)
    print(order)
    [print(line) for line in order.line_items]
    print()

    query = session.query(
        Order.order_id,
        User.username,
        User.phone,
        Cookie.cookie_name,
        LineItem.quantity,
        LineItem.extended_cost
    )
    query = query.join(User).join(LineItem).join(Cookie)
    results = query.filter(User.username == 'cookie-monster').all()
    [print(line) for line in results]

    query = session.query(User.username, func.count(Order.order_id))
    query = query.outerjoin(Order).group_by(User.username)
    [print(row) for row in query]


if __name__ == '__main__':
    engine = create_engine('sqlite:///cookies.db')
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    sess = Session()

    # add_cookies(session=sess, verbose=True)
    # check_cookies(session=sess)
    # update_cookie(session=sess)
    # delete_cookie(session=sess, verbose=True)
    # add_all_objects(session=sess)
    check_all_objects(session=sess)
