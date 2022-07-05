# """
# Cookie database as per the Jason Myers presentation -- straight copy
#     https://www.youtube.com/watch?v=51RpDZKShiw&t=1535s&ab_channel=NextDayVideo
#     https://www.slideshare.net/jamdatadude/introduction-to-sqlalchemy-orm
#
# Automap -- for converting database into SQLAlchemy classes
#     https://docs.sqlalchemy.org/en/14/orm/extensions/automap.html
# """
#
# from sqlalchemy import\
#     create_engine,\
#     func, desc, cast,\
#     and_, or_, not_,\
#     ForeignKey, Column, Integer, Numeric, String, DateTime, Boolean
# from sqlalchemy.orm import sessionmaker, relationship, backref
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime
#
# Base = declarative_base()
#
#
# class Cookie(Base):
#     __tablename__ = 'cookies'
#
#     cookie_id = Column(Integer, primary_key=True)
#     cookie_name = Column(String(50), index=True)
#     cookie_recipe_url = Column(String(255))
#     cookie_sku = Column(String(55))  # stock-keeping unit
#     quantity = Column(Integer())
#     unit_cost = Column(Numeric(12, 2))
#
#
#
#
# engine = create_engine('sqlite:///:memory:')
# Session = sessionmaker(bind=engine)
# Base.metadata.create_all(engine)
#
# session = Session()
#
#
#
# cc_cookie = Cookie(
#     cookie_name='chocolate chip',
#     cookie_recipe_url='https://some.aweso.me/cookie/recipe.html',
#     cookie_sku='CC01',
#     quantity=12,
#     unit_cost=0.50
# )
# session.add(cc_cookie)
# session.commit()
# print(cc_cookie.cookie_id)  # 1
#
#
# # Bulk Insert
#
# c1 = Cookie(
#     cookie_name='peanut butter',
#     cookie_recipe_url='https://some.aweso.me/cookie/peanut.html',
#     cookie_sku='PB01',
#     quantity=24,
#     unit_cost=0.25
# )
# c2 = Cookie(
#     cookie_name='oatmeal raisin',
#     cookie_recipe_url='https://some.okay.me/cookie/raisin.html',
#     cookie_sku='EWW01',
#     quantity=100,
#     unit_cost=1.00
# )
# session.bulk_save_objects([c1, c2])
# session.commit()
# print(c1.cookie_id)
#
#
# # Queries
#
# cookies = session.query(Cookie).all()
# print(cookies)
# # [
# #     Cookie(
# #         cookie_name='chocolate chip',
# #         cookie_recipe_url='https://some.aweso.me/cookie/recipe.html',
# #         cookie_sku='CC01',
# #         quantity=12,
# #         unit_cost=0.50
# #     ),
# #     Cookie(
# #         cookie_name='peanut butter',
# #         cookie_recipe_url='https://some.aweso.me/cookie/peanut.html',
# #         cookie_sku='PB01',
# #         quantity=24,
# #         unit_cost=0.25
# #     ),
# #     Cookie(
# #         cookie_name='oatmeal raisin',
# #         cookie_recipe_url='https://some.okay.me/cookie/raisin.html',
# #         cookie_sku='EWW01',
# #         quantity=100,
# #         unit_cost=1.00
# #     )
# # ]
#
#
# for cookie in session.query(Cookie):
#     print(cookie)
# # Cookie(
# #     cookie_name='chocolate chip',
# #     cookie_recipe_url='https://some.aweso.me/cookie/recipe.html',
# #     cookie_sku='CC01',
# #     quantity=12,
# #     unit_cost=0.50
# # )
# # Cookie(
# #     cookie_name='peanut butter',
# #     cookie_recipe_url=r'https://some.aweso.me/cookie/peanut.html',
# #     cookie_sku='PB01',
# #     quantity=24,
# #     unit_cost=0.25
# # )
# # Cookie(
# #     cookie_name='oatmeal raisin',
# #     cookie_recipe_url='https://some.okay.me/cookie/raisin.html',
# #     cookie_sku='EWW01',
# #     quantity=100,
# #     unit_cost=1.00
# # )
#
# print(session.query(Cookie.cookie_name, Cookie.quantity).first())
# # ('chocolate chip', 12)
#
#
# for cookie in session.query(Cookie).order_by(Cookie.quantity):
#     print('{:3} - {}'.format(cookie.quantity, cookie.cookie_name))
# #  12 - chocolate chip
# #  24 - peanut butter
# # 100 - oatmeal raisin
#
#
# for cookie in session.query(Cookie).order_by(desc(Cookie.quantity)):
#     print('{:3} - {}'.format(cookie.quantity, cookie.cookie_name))
#
# query = session.query(Cookie).order_by(Cookie.quantity).limit(2)
# print([result.cookie_name for result in query])
# # ['chocolate chip', 'peanut butter']
#
#
# # Database Functions
# inv_count = session.query(func.sum(Cookie.quantity)).scalar()
# print(inv_count)
# # 136
#
#
# rec_count = session.query(func.count(Cookie.cookie_name)).first()
# print(rec_count)
# # (3, 0)
#
#
# rec_count = session.query(func.count(Cookie.cookie_name).label('inventory_count')).first()
# print(rec_count.keys())
# print(rec_count.inventory_count)
# # ['inventory_count']
# # 5
#
#
# record = session.query(Cookie).filter_by(cookie_name='chocolate chip').first()
# print(record)
# # Cookie(
# #     cookie_name='chocolate chip',
# #     cookie_recipe_url='https://some.aweso.me/cookie/recipe.html',
# #     cookie_sku='CC01',
# #     quantity=12,
# #     unit_cost=0.50
# # )
#
#
# record = session.query(Cookie).filter(Cookie.cookie_name == 'chocolate chip').first()
# print(record)
#
#
# query = session.query(Cookie).filter(Cookie.cookie_name.like('%chocolate%'))
# for record in query:
#     print(record.cookie_name)
# # chocolate chip
#
#
# query = session.query(Cookie.cookie_name, cast((Cookie.quantity * Cookie.unit_cost), Numeric(12, 2)).label('inv_cost'))
# for result in query:
#     print('{} - {}'.format(result.cookie_name, result.inv_cost))
# # chocolate chip - 6.00 peanut butter - 6.00 oatmeal raisin - 100.00
#
#
#
# query = session.query(Cookie).filter(
#     or_(
#         Cookie.quantity.between(10, 50),
#         Cookie.cookie_name.contains('chip')
#     )
# )
# for result in query:
#     print(result.cookie_name)
# # chocolate chip
# # peanut butter
#
#
# # Updating Cookies
#
# query = session.query(Cookie)
# cc_cookie = query.filter(Cookie.cookie_name == "chocolate chip").first()
# cc_cookie.quantity = cc_cookie.quantity + 120
# session.commit()
# print(cc_cookie.quantity)
# # 132
#
#
# # Deleting Cookies
#
# query = session.query(Cookie)
# query = query.filter(Cookie.cookie_name == "peanut butter")
# dcc_cookie = query.one()
# session.delete(dcc_cookie)
# session.commit()
# dcc_cookie = query.first()
# print(dcc_cookie)
# # None
#
#
# # Relationships
#
# class User(Base):
#     __tablename__ = 'users'
#
#     user_id = Column(Integer(), primary_key=True)
#     username = Column(String(15), nullable=False, unique=True)
#     email_address = Column(String(255), nullable=False)
#     phone = Column(String(20), nullable=False)
#     password = Column(String(25), nullable=False)
#     created_on = Column(DateTime(), default=datetime.now)
#     updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
#
#
# class Order(Base):
#     __tablename__ = 'orders'
#
#     order_id = Column(Integer(), primary_key=True)
#     user_id = Column(Integer(), ForeignKey('users.user_id'))
#     shipped = Column(Boolean(), default=False)
#
#     user = relationship("User", backref=backref('orders', order_by=order_id))
#
#
# class LineItem(Base):
#     __tablename__ = 'line_items'
#
#     line_item_id = Column(Integer(), primary_key=True)
#     order_id = Column(Integer(), ForeignKey('orders.order_id'))
#     cookie_id = Column(Integer(), ForeignKey('cookies.cookie_id'))
#     quantity = Column(Integer())
#     extended_cost = Column(Numeric(12, 2))
#
#     order = relationship("Order", backref=backref('line_items', order_by=line_item_id))
#     cookie = relationship("Cookie", uselist=False)
#
#
# Base.metadata.create_all(engine)
#
#
# cookiemon = User(
#     username='cookiemon',
#     email_address='mon@cookie.com',
#     phone='111-111-1111',
#     password='password'
# )
# session.add(cookiemon)
# session.commit()
#
# o1 = Order()
# o1.user = cookiemon
# session.add(o1)
#
# cc = session.query(Cookie).filter(Cookie.cookie_name == "chocolate chip").one()
# line1 = LineItem(cookie=cc, quantity=2, extended_cost=1.00)
# pb = session.query(Cookie).filter(Cookie.cookie_name == "oatmeal raisin").one()
# line2 = LineItem(quantity=12, extended_cost=3.00)
# line2.cookie = pb
#
# o1.line_items.append(line1)
# o1.line_items.append(line2)
# session.commit()
#
# query = session.query(Order.order_id, User.username, User.phone, Cookie.cookie_name, LineItem.quantity, LineItem.extended_cost)
# query = query.join(User).join(LineItem).join(Cookie)
# results = query.filter(User.username == 'cookiemon').all()
# print(results)
# # [
# #     (1, 'cookiemon', '111-111-1111', 'chocolate chip', 2, Decimal('1.00')),
# #     (1, 'cookiemon', '111-111-1111', 'oatmeal raisin', 12, Decimal('3.00'))
# # ]
#
# query = session.query(User.username, func.count(Order.order_id))
# query = query.outerjoin(Order).group_by(User.username)
# for row in query:
#     print(row)
# # ('cookiemon', 1)
