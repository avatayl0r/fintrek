from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os
import json

import fintrek_config as config



class EnvInit:
    def __init__(self) -> None:
        self.engine_url = None

        if self.setup_env():
            conn = DBConn(self.engine_url)
            print(conn.get_existing_tables())
            pretty_print(conn.get_selected_table("finances"))

    def setup_env(self):
        if not os.path.exists(config.APP_LOCAL_PATH):
            print("App cache not found. Creating App cache...")
            os.makedirs(config.APP_LOCAL_PATH)

        if not os.path.exists(f"{config.APP_LOCAL_PATH}/.env"):
            print("Environment file not found. Please create an environment file.")

        load_dotenv(f"{config.APP_LOCAL_PATH}/.env", override=True)

        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASS")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")

        self.engine_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        return True


class ToDictFunc:
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

class DBConn:
    def __init__(self, engine_url) -> None:
        self.sql_engine = create_engine(
            engine_url, pool_size=10, max_overflow=20, pool_timeout=30)
        self.base = self.init_base()
        self.session = sessionmaker(bind=self.sql_engine)

    def init_base(self):
        base = automap_base()
        base.prepare(autoload_with=self.sql_engine, schema="public")
        self.apply_todict_functionality(base)
        return base

    def apply_todict_functionality(self, base):
        for class_ in base.classes:
            class_.__bases__ = (ToDictFunc,) + class_.__bases__

    def get_existing_tables(self):
        return self.base.classes.keys()

    def get_selected_table(self, table_name):
        try:
            session = self.session()
            table = getattr(self.base.classes, table_name)
            results = session.query(table).all()
            return [result.to_dict() for result in results][0]
        except Exception as e:
            print(f"Exception occurred while getting {table_name}: {e}")
        finally:
            session.close()


def pretty_print(d):
   for key, value in d.items():
      print(f"{key} >>> {value}")


if __name__ == "__main__":
    EnvInit()
