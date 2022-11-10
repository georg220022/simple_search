import unittest
import requests
import json
from settings import ELASTIC, CONN_POSTGRES


class SimpleSearcher(unittest.TestCase):
    def test_search_result(self):
        """Тест на правильность поиска по слову 'труба'"""
        response = requests.get("http://localhost:8000/search/труба")
        self.assertEqual(response.status_code, 200)  # Статус код 200
        self.assertEqual(
            "труба" in response.text, True
        )  # Слово 'труба' присутствует в ответе
        self.assertEqual(
            len(json.loads(response.text)), 1
        )  # Должна быть 1 запись по слову 'труба'

    def test_delete_result(self):
        """Удаляем объекты по слову 'труба'"""
        id_object = json.loads(requests.get("http://localhost:8000/search/труба").text)
        for ids in id_object.keys():
            response = requests.delete(f"http://localhost:8000/id/{ids}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual("Объект удален" in response.text, True)

    def test_not_found_result(self):
        """Теперь по слову 'труба' нет совпадений"""
        response = requests.get("http://localhost:8000/search/труба")
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Совпадений не найдено" in response.text, True)


def suite():
    """Очередь выполнения тестов"""
    suite = unittest.TestSuite()
    suite.addTest(SimpleSearcher("test_search_result"))
    suite.addTest(SimpleSearcher("test_delete_result"))
    suite.addTest(SimpleSearcher("test_not_found_result"))
    return suite

def back_up_record():
    # Сохраним данные, которые будут удалены при запуске тестов
    response = json.loads(requests.get("http://localhost:8000/search/труба").text)
    for obj in response.values():
        data = [obj["text"], obj["created_date"], obj["rubrics"]]
    return data

def write_back_record_postgres(data):
    # Возвращаем удаленную запись в PostgreSQL
    with CONN_POSTGRES:
        with CONN_POSTGRES.cursor() as cur:
            # Записываем данные в PostgreSQL, что бы получить уникальный id записи который добавится в Elastic
            query = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s)" % (
                "directors",
                "text, created_date, rubrics",
            )
            cur.execute(query, data)
            CONN_POSTGRES.commit()

def write_back_record_elastic():
    # Возвращаем удаленную запись в ElasticSearch
    with CONN_POSTGRES:
        with CONN_POSTGRES.cursor() as cur:
            # Берем последнюю запись из PostgreSQL вместе с новым id
            cur.execute(
                """
                SELECT id, text
                FROM directors
                ORDER BY id DESC
                LIMIT 1;
                """
            )
            for obj in cur:
                # Запиcываем индекс, теперь id в обеих базах одинаковы
                ELASTIC.index(
                    index="directors",
                    id=obj[0],
                    document={"id": obj[0], "text": obj[1]},
                )

def runners():
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())

if __name__ == "__main__":

    data = back_up_record()
    runners()
    write_back_record_postgres(data)
    write_back_record_elastic()
