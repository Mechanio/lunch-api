import os
from dotenv import load_dotenv

# project_root = os.getcwd()
# load_dotenv(os.path.join(project_root, '.env'))
load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv("KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or os.getenv("DB_STRING")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']