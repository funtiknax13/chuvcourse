# Api приложения для самообучения

Технологии
```
* Python
* Django, DRF
* JWT, DRF-YASG
* PostgreSQL
```

Для запуска необходимо создать файл .env в папке проекта и задать следующие переменные:
```
SECRET_KEY=
DEBUG=
DB_PASSWORD=
```

Документация:
```
/swagger/
/redoc/
```

Фильтрация, сортировка:
```
/lesson/?course=1 - фильтрация уроков по курсу
/lesson/?ordering=course - сортировка уроков по курсу
```

Для создания образа из Dockerfile и запуска контейнера:
```
docker compose up --build
```

Для запуска приложения:
```
python3 manage.py runserver
```

Для тестирования проекта:
```
python3 manage.py test
```

Для запуска подсчета покрытия и вывода отчета запустить команды:
```
coverage run --source='.' manage.py test
coverage report
```


