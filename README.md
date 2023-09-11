# Библиотека фильмов и сериалов

-Реализована админ панель для управления сервисом

-Загрузка из mysql базы данных в postgres

-Локализация на русский средствами  django gettext_lazy

-Простое api, возвращающее информацию о кинопроизведении, участниках и жанрах

-postman тесты для api

-Nginx сервер для раздачи статических файлов

-ETL процесс для переноса данных из postgres в elastic

-postman тесты для проверки для данные в elastic

-docker-compose для запуска елементов системы

# Инструкция для запуска

docker-compose up -d build

docker-compose up

docker-compose exec -ti serv  python manage.py migrate

docker-compose exec -ti cron python load_data.py для загрузки из sqllite

cron etl с переносом постгрес срабатывает каждую минуту
