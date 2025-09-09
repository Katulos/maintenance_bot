from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm


class CreatedAtMixin:
    """Mixin adding created_at timestamp column."""

    __abstract__ = True

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
        doc="Timestamp of when the record was created",
    )


class UpdatedAtMixin:
    """Mixin adding updated_at timestamp column."""

    __abstract__ = True

    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        doc="Timestamp of when the record was last updated",
    )


class CreatedUpdatedAtMixin(CreatedAtMixin, UpdatedAtMixin):
    """Mixin combining both created_at and updated_at timestamps."""

    __abstract__ = True

    pass
