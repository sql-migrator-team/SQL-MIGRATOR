from sqlalchemy import create_engine


def create_postgres_engine(username: str, password: str, host: str, port: str, database: str):
    """Create a SQLAlchemy engine for a PostgreSQL database using psycopg2."""
    connection_string = (
        f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
    )
    return create_engine(connection_string, pool_pre_ping=True)
