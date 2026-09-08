from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session per request."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def check_database_connection() -> None:
    """Verify the database is reachable, failing fast with a clear message.

    Meant to be called once at application startup (see the FastAPI
    lifespan in app.main) so a missing/unreachable database stops the app
    with one short message instead of crashing on the first request with
    a raw SQLAlchemy traceback.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except OperationalError:
        raise SystemExit(
            f"Startup failed: could not connect to the database at "
            f"'{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_database}'. "
            "Check that the database exists and is reachable."
        ) from None
