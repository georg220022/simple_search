from settings import ELASTIC, CONN_POSTGRES


class ElasicModels:

    @staticmethod
    def search_directors(user_text):
        res = ELASTIC.search(
            index="directors",
            size=2000,
            explain=False,
            _source_excludes="text",
            query={"match": {"text": user_text}},
        )
        return res

    @staticmethod
    def delete_id(id):
        if ELASTIC.exists(index="directors", id=id):
            ELASTIC.delete(index="directors", id=id)
            return True


class PostgresModels:

    @staticmethod
    def search_directors(data_id):
        with CONN_POSTGRES:
            with CONN_POSTGRES.cursor() as cur:
                query = f"""SELECT * FROM directors WHERE id IN {data_id} ORDER BY created_date ASC LIMIT 20;"""
                if len(data_id) == 1:
                    query = f"""SELECT * FROM directors WHERE id = {data_id[0]} ORDER BY created_date ASC LIMIT 20;"""
                cur.execute(query)
                json_data = {}
                for obj in cur:
                    json_data[str(obj[0])] = {
                        "id": obj[0],
                        "rubrics": obj[1],
                        "text": obj[2],
                        "created_date": obj[3],
                    }
                return json_data

    @staticmethod
    def delete_id(id):
        with CONN_POSTGRES:
            with CONN_POSTGRES.cursor() as cur:
                query = f"""DELETE FROM directors WHERE id={id}"""
                cur.execute(query)
                return True
