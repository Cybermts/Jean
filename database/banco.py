import os
import psycopg
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def conectar():

    return psycopg.connect(DATABASE_URL)