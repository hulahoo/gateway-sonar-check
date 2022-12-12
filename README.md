# Syslog Gateway

Сервис для приема входящих сообщений от SIEM и маршрутизации их дальнейшей в Kafka (или в сервис обработки – опционально)

## Накатка миграций
Миграции можно запустить:
    1. Локально, запустив файл следующим образом:
        ```
        python3 src/apps/models/migrations.py
        ```

## Информация о протоколе SYSLOG в проекте
Для настройки порта и хоста по которым сервис должен быть доступным, указываем в .env файле следующее:
    ```
    EVENTS_PORT=your_port
    EVENTS_HOST=your_host
    ```

## Информаци о ENV-параметрах
Имеющиеся env-параметры в проекте:
    ```
    EVENTS_PORT=""  # порт по которому желаем развернуть сервис
    EVENTS_HOST=""  # хост на котором будет размещен сервис

    KAFKA_HOST=""
    EVENTS_COLLECTOR_TOPIC="" # topic куда будут отправлены данные полученные по SYSLOG
    ALLOW_ANONYMOUS_LOGIN=(yes/no) # для логина в zookeper
    ALLOW_PLAINTEXT_LISTENER=(yes/no)

    APP_POSTGRESQL_HOST=""
    APP_POSTGRESQL_PASSWORD=""
    APP_POSTGRESQL_USER=""
    APP_POSTGRESQL_NAME=""
    APP_POSTGRESQL_PORT=""
    ```

## Информация о файлах конфигурации
Все конфигурции можно найти в директории:
```
    src/apps/config
```

## Локальный запуск

Для запуска локально нужно:
1. Активировать виртуальное окружение: 
```
. venv/bin/activate
```
2. Установить зависимости: 
```
pip3 install -r requirements.txt
```

4. Запустить консюмер: 
``` 
python3 main.py
```
5. Запустить тестовый клиент для отправки сообщения:
```
python3 client.py
```