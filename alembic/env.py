from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from settings import settings
from alembic import context
from app.models import *
config = context.config

section = config.config_ini_section
config.set_section_option(section, "HOST", settings.HOST)
config.set_section_option(section, "PORT", settings.PORT)
config.set_section_option(section, "DB", settings.DB)
config.set_section_option(section, "USER", settings.USER)
config.set_section_option(section, "PASSWORD", settings.PASSWORD)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
