import pytest

from app.core.config import Settings


@pytest.mark.parametrize("url", [
    "postgres://u:p@host:5432/agridb",
    "postgresql://u:p@host:5432/agridb",
    "postgresql+psycopg://u:p@host:5432/agridb",
])
def test_database_url_usa_psycopg(url):
    assert Settings(DATABASE_URL=url).DATABASE_URL == "postgresql+psycopg://u:p@host:5432/agridb"
