"""
Playing with SQLAlchemy Core
    * https://speakerdeck.com/pycon2014/an-introduction-to-sqlalchemy-core-by-jason-myers?slide=10
    * https://www.youtube.com/watch?v=0PSdzUxRYpA&ab_channel=PyCon2014
"""

from sqlalchemy import\
    create_engine,\
    MetaData, ForeignKey,\
    Table, Column, Integer, String, \
    select, func, and_, or_, not_


metadata = MetaData()
engine = create_engine('sqlite:///core.db')


##########
# Bind to tables (will create if they don't exist)
actors = Table(
    'actors',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
    Column('body_count', Integer)
)
roles = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('actor_id', None, ForeignKey('actors.id')),
    Column('character_name', String, nullable=False)
)


metadata.create_all(engine)


##########
# Check the columns in the 'actors' table
# [print(item) for item in actors.columns.items()]


##########
# Insert a value
conn = engine.connect()

# ins = actors.insert().values(
#     name='Graham', fullname='Graham Chapman', body_count=3
# )
# result = conn.execute(ins)
# print(result.inserted_primary_key)
# print(str(ins))
# print(ins.compile().params)

# results = conn.execute(
#     actors.insert(),
#     [
#         {'name': 'Graham', 'fullname': 'Graham Chapman', 'body_count': 3},
#         {'name': 'John',   'fullname': 'John Cleese',    'body_count': 0},
#         {'name': 'Terry',  'fullname': 'Terry Gilliam',  'body_count': 0}
#     ]
# )
# print(results.rowcount)

# results = conn.execute(
#     roles.insert(),
#     [
#         {'actor_id': 1, 'character_name': 'King Arthur'},
#         {'actor_id': 1, 'character_name': 'Voice of God'},
#         {'actor_id': 2, 'character_name': 'Sir Lancelot'},
#         {'actor_id': 2, 'character_name': 'Black Knight'},
#         {'actor_id': 3, 'character_name': 'Patsy'},
#         {'actor_id': 3, 'character_name': 'Sir Bors'}
#     ]
# )
# print(results.rowcount)


##########
# Update

# statement = actors.update().where(actors.c.name == 'Graham').values(name='Gram')
# result = conn.execute(statement)
# print(result.rowcount)


##########
# Delete

# result = conn.execute(actors.delete().where(actors.c.name == 'Terry'))
# print(result.rowcount)


##########
# Select

# result = conn.execute(select([actors.c.name, actors.c.fullname]))
# [print(row) for row in result]


##########
# Ordering

# statement = select([actors.c.name]).order_by(actors.c.name.desc())
# print(conn.execute(statement).fetchall())


##########
# Limiting

# statement = select([actors.c.name, actors.c.fullname]).limit(1).offset(1)
# print(conn.execute(statement).first())


##########
# Count

# statement = select([func.count()]).select_from(actors)
# print(conn.execute(statement).scalar())


##########
# Sum

# statement = select([func.count(actors.c.id), func.sum(actors.c.body_count)])
# print(conn.execute(statement).first())


##########
# Joins like a noob

# statement = select([actors, roles]).where(actors.c.id == roles.c.actor_id)
# [print(row) for row in conn.execute(statement)]


##########
# Grouping

# statement = select(
#     [
#         actors.c.name,
#         func.count(roles.c.id)
#     ]
# ).select_from(
#     actors.join(roles)
# ).group_by(
#     actors.c.name
# )
# [print(row) for row in conn.execute(statement).fetchall()]


##########
# Filtering

# statement = select(
#     [
#         actors.c.name,
#         roles.c.character_name
#     ]
# ).where(
#     and_(
#         actors.c.name.like('Gra%'),
#         roles.c.character_name.like('Vo%'),
#         actors.c.id == roles.c.actor_id
#     )
# )
# [print(row) for row in conn.execute(statement).fetchall()]


##########
# Chaining

statement = select(
    [
        actors.c.name,
        func.count(roles.c.character_name).label('character_count')
    ]
).select_from(
    actors.join(roles)
).where(
    and_(
        actors.c.name.like('%h%'),
        actors.c.body_count != 0
    )
).group_by(
    actors.c.id
).group_by(
    actors.c.id
)
[print(row) for row in conn.execute(statement).fetchall()]
