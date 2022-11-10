import os
import psycopg2
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

POSTGRES_NAME = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

ELASTIC = Elasticsearch(hosts=f"http://elastic:{ELASTIC_PASSWORD}@elasticsearch:9200/")

CONN_POSTGRES = psycopg2.connect(
    database=POSTGRES_NAME,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host="postgres_db",
    port="5432",
)
