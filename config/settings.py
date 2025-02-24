import os

from dotenv import load_dotenv

load_dotenv()


DEBUG = os.environ.get("DEBUG", True)


DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


DB_TEST_HOST = os.environ.get("DB_TEST_HOST")
DB_TEST_PORT = os.environ.get("DB_TEST_PORT")
DB_TEST_NAME = os.environ.get("DB_TEST_NAME")
DB_TEST_USER = os.environ.get("DB_TEST_USER")
DB_TEST_PASSWORD = os.environ.get("DB_TEST_PASSWORD")
DATABASE_TEST_URL = f"postgresql+asyncpg://{DB_TEST_USER}:{DB_TEST_PASSWORD}@{DB_TEST_HOST}:{DB_TEST_PORT}/{DB_TEST_NAME}"


SECRET_KEY = os.environ.get("SECRET_KEY")
# 60 minutes * 24 hours * 30 days = 30 days
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
JWT_ALGORITHM = "HS256"


ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", ["*"]).split(",")
ALLOWED_METHODS = os.environ.get("ALLOWED_METHODS", ["*"]).split(",")
ALLOWED_HEADERS = os.environ.get("ALLOWED_HEADERS", ["*"]).split(",")
ALLOW_CREDENTIALS = os.environ.get("ALLOW_CREDENTIALS", True)
