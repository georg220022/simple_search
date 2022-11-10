# simple_searcher

##### Запускаем docker:  
P.s Запускать без флага '-d', что бы наглядно видеть когда закончится инициализация ElasticSearch  
```docker-compose up```  

##### Когда контейнеры запустились, ждем окончания иницилизации ElasticSerach, после загружаем данные в базы:  
```docker exec -it web python3 load_from_csv.py```  

##### По желанию можно запустить тесты:  
```docker exec -it web python3 test.py```  

##### Поиск по тексту через url (GET запрос):  
```http://localhost:8000/search/труба```  

##### Удаление по id через url (DELETE запрос):  
```http://localhost:8000/id/1```  

##### Остановка и удаление ```всех``` контейнеров и образов после проверки:  
```docker stop $(docker ps -a -q)```  
```docker system prune -a --volumes```  

#### Стек:  
- FastAPI, PostgreSQL, Docker(compose), ElasticSearch, Python, Unittest, SQL  
#### Остальное:  
- Старался использовать минимум сторонних библиотек. Не использвал ORM, все запросы на SQL.  
