import os

from dotenv import load_dotenv

env_vars_to_clear = [
    'DB_NAME',
    'DB_USER',
    'DB_PASSWORD',
    'DB_HOST',
    'DB_PORT',
    'TG_TOKEN',
]

for var in env_vars_to_clear:
    os.environ.pop(var, None)

load_dotenv()

DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
TG_TOKEN=os.getenv("TG_TOKEN")
