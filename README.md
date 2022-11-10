# simple_searcher  

#### Требования для запуска: Docker  
#### 1) Клонировать или скачать репозиторий  
#### 2) В терминале открыть папку проекта (simple search)  

##### Запускаем docker:  
P.s Запускать БЕЗ флага '-d', что бы наглядно видеть когда закончится инициализация ElasticSearch  
```docker-compose up```  

##### Когда контейнеры запустились, ждем окончания иницилизации ElasticSerach, после открываем новый терминал и загружаем данные в базы:  
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
- Все запросы синхронны
