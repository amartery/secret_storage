### Хранилище секретов  
## Запуск  
sudo docker-compose up  
## Тестирование  
http://127.0.0.1:8000/docs  
## Выполнено  
Данные сервиса хранятся во внешнем хранилище (MongoDB)  
Секреты и кодовые фразы не хранятся в базе в открытом виде (зашифрованы c помощью base64)  
Добавлена возможность задавать время жизни для секретов (с помощью TTL индексов)  
## TODO
Дописать тесты pytest (постараюсь добавить в ближайшее время)  
Асинхронность  
## Возможные ошибки
Возможна неточная работа TTL индексов (Из документации MongoDB: Warning: The TTL index does not guarantee that expired data will be deleted immediately. There may be a delay between the time a document expires and the time that MongoDB removes the document from the database.)
Также проблема может быть в использовании функции datetime.datetime.utcnow()
