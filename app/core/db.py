import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./data/test.db"  # SQLite 数据库文件路径

database = databases.Database(DATABASE_URL)  # 创建数据库连接
metadata = sqlalchemy.MetaData()  # 创建元数据对象，它将包含所有的表和模型信息

users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True,
                      index=True),  # 用户ID
    sqlalchemy.Column("nickname", sqlalchemy.String, index=True,
                      unique=True),  # 用户昵称
    sqlalchemy.Column("avatar_url", sqlalchemy.String, nullable=True),  # 用户头像
    sqlalchemy.Column("city", sqlalchemy.String, nullable=True),  # 用户城市
    sqlalchemy.Column("coins", sqlalchemy.Integer, default=0),  # 用户金币数量，默认为0
)

items_table = sqlalchemy.Table(
    "items", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Float))

engine = sqlalchemy.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":
                  False})  # 创建数据库引擎，`check_same_thread` 参数是 SQLite 的特定设置
metadata.create_all(bind=engine)  # 创建表
