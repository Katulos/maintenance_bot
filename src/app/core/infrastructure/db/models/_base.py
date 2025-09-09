import sqlalchemy as sa
import sqlalchemy.schema as sh
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm.decl_api import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    __convention: dict[type[sh.Constraint | sh.Index], str] = {
        sh.Index: "ix__%(table_name)s__%(all_column_names)s",
        sh.UniqueConstraint: "uq__%(table_name)s__%(all_column_names)s",
        sh.CheckConstraint: "ck__%(table_name)s__%(constraint_name)s",
        sh.ForeignKeyConstraint: (
            "fk__%(table_name)s__%(all_column_names)s__"
            "%(referred_table_name)s"
        ),
        sh.PrimaryKeyConstraint: "pk__%(table_name)s",
    }

    __naming_convention = {  # type: ignore
        **__convention,
        "all_column_names": lambda constraint, table: "_".join(
            [column.name for column in constraint.columns.values()],
        ),
    }

    metadata = sa.MetaData(naming_convention=__naming_convention)


@sa.event.listens_for(sa.engine.Engine, "connect")
def _set_sqlite_pragma(dbapi, connection_record) -> None:
    if hasattr(dbapi.dbapi, "sqlite"):
        cursor = dbapi.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()
