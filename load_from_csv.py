import os
import csv
from settings import ELASTIC, CONN_POSTGRES


path = os.path.abspath("posts.csv")

try:
    with open(path, "r", newline="") as f:
        file_reader = csv.reader(f, dialect="excel")
        fixed_csv_data = []
        # фиксим колонку из текста в нормальный формат
        for row in file_reader:
            fixed_row_2 = row[2][1:-2].replace("'", "").split(", ")
            fixed_csv_data.append((row[0], row[1], fixed_row_2))
        fixed_csv_data.pop(0)
        with CONN_POSTGRES:
            with CONN_POSTGRES.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS directors(
                        id SERIAL PRIMARY KEY,
                        rubrics TEXT [],
                        text TEXT,
                        created_date DATE
                    );
                """
                )
                CONN_POSTGRES.commit()
            with CONN_POSTGRES.cursor() as cur:
                query = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s)" % (
                    "directors",
                    "text, created_date, rubrics",
                )
                print("Начинаем заполнение PostgreSQL")
                cur.executemany(query, fixed_csv_data)
                CONN_POSTGRES.commit()
    print("Данные в PostgreSQL записаны")
except:
    print("Ошибка записи в PostgreSQL")

try:
    with CONN_POSTGRES.cursor() as cur:
        directors = {}
        cur.execute(
            """
            SELECT id, text
            FROM directors;
            """
        )
        print("Начинаем заполнение ElasticSearch")
        for obj in cur:
            ELASTIC.index(
                index="directors", id=obj[0], document={"id": obj[0], "text": obj[1]}
            )
    print("Данные в ElasticSearch записаны")
except:
    print("Ошибка записи в ElasticSearch")
finally:
    CONN_POSTGRES.close()
