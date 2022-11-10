from fastapi import FastAPI
from models import ElasicModels, PostgresModels

app = FastAPI()


@app.get("/search/{user_text}", status_code=200)
def search_obj(user_text: str):
    elastic_res = ElasicModels.search_directors(user_text)
    elastic_data = elastic_res["hits"]["hits"]
    if len(elastic_data) >= 1:
        data_id = tuple([obj["_source"]["id"] for obj in elastic_data])
        postgres_data = PostgresModels.search_directors(data_id)
        if postgres_data:
            return postgres_data
    return {"info": "Совпадений не найдено"}


@app.delete("/id/{id}", status_code=200)
def delete_obj(id: int):
    if ElasicModels.delete_id(id):
        if PostgresModels.delete_id(id):
            return {"info": "Объект удален"}
        return {"error": "Ошибка удаления из PostreSQL, объекта не существует"}
    return {"error": "Ошибка удаления из Elastic, объекта не существует"}
