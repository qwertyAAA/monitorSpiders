from sqlalchemy import Table, create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:123456@10.25.116.62:3306/monitor")
metadata = MetaData(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Article = Table('SpiderDB_article', metadata, autoload=True)
Author = Table('SpiderDB_author', metadata, autoload=True)
Source = Table('SpiderDB_rule', metadata, autoload=True)
metadata.create_all(engine)
