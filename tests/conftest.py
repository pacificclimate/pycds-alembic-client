from pytest import fixture
import testing.postgresql

from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema

from alembic.config import Config
from alembic import command
import alembic.config
import alembic.command

import importlib_resources

import pycds
import pycds.alembic


@fixture(scope='session')
def schema_name():
    return pycds.get_schema_name()


@fixture(scope='session')
def database_uri():
    """Test-session scoped base database.
    """
    with testing.postgresql.Postgresql() as pg:
        yield pg.url()


@fixture(scope='session')
def base_engine(database_uri, schema_name):
    """Test-session scoped base database engine.
    "Base" engine indicates that it has no ORM content created in it.
    """
    engine = create_engine(database_uri)
    engine.execute('CREATE EXTENSION postgis')
    engine.execute('CREATE EXTENSION plpythonu')
    engine.execute(CreateSchema(schema_name))
    yield engine


@fixture(scope='session')
def alembic_script_location():
    """
    This fixture extracts the filepath to the installed pycds Alembic content.
    The filepath is typically like
    `/usr/local/lib/python3.6/dist-packages/pycds/alembic`.
    """
    source = importlib_resources.files(pycds.alembic)
    # print(f"alembic_script_location: {source}")
    yield str(source)


@fixture(scope='session')
def pycds_engine(database_uri, base_engine, alembic_script_location):
    alembic_config = alembic.config.Config()
    alembic_config.set_main_option("script_location", alembic_script_location)
    alembic_config.set_main_option("sqlalchemy.url", database_uri)
    alembic.command.upgrade(alembic_config, 'head')
    yield base_engine


@fixture(scope='session')
def get_schema_item_names():
    def f(executor, item_type, schema_name):
        if item_type == "routines":
            r = executor.execute(
                f"""
                SELECT routine_name 
                FROM information_schema.routines 
                WHERE specific_schema = '{schema_name}'
            """
            )
        elif item_type == "tables":
            r = executor.execute(
                f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = '{schema_name}';
            """
            )
        elif item_type == "views":
            r = executor.execute(
                f"""
                SELECT table_name 
                FROM information_schema.views 
                WHERE table_schema = '{schema_name}';
            """
            )
        else:
            raise ValueError("invalid item type")
        return {x[0] for x in r.fetchall()}

    return f
