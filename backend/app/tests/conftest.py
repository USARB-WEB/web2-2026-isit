"""Shared pytest fixtures.

Tests must never run against the development database. This module points
the app at a dedicated ``learning_test_db`` database (see
``app.core.config.Settings.test_database_url``) and overrides FastAPI's
``get_db`` dependency so every request made through the test client uses it.

Import ``TestSessionLocal`` from this module in test files instead of
``app.db.session.SessionLocal`` when a test needs direct DB access (e.g. to
clean up tables in ``setup_function``).
"""
from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db

# Import all models so they're registered on Base.metadata before create_all.
from app.db.models.order import Order  # noqa: F401
from app.db.models.order_product import OrderProduct  # noqa: F401
from app.db.models.product import Product  # noqa: F401
from app.db.models.product_category import ProductCategory  # noqa: F401

from app.main import app

test_engine = create_engine(settings.test_database_url, pool_pre_ping=True)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def _get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _get_test_db


@pytest.fixture(scope="session", autouse=True)
def _test_database_schema():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
