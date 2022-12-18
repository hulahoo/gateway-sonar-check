# Events Gateway

Сервис для приема входящих сообщений от SIEM и маршрутизации их дальнейшей в Kafka

## Информация о протоколе SYSLOG в проекте
Для настройки порта и хоста по которым сервис должен быть доступным, указываем в .env файле следующее:
    ```
    EVENTS_PORT=your_port
    EVENTS_HOST=your_host
    ```

## Информаци о ENV-параметрах
Имеющиеся env-параметры в проекте:
    ```
    EVENTS_PORT  # порт по которому желаем развернуть сервис
    EVENTS_HOST  # хост на котором будет размещен сервис
    APP_POSTGRESQL_HOST
    APP_POSTGRESQL_PASSWORD
    APP_POSTGRESQL_USER
    APP_POSTGRESQL_NAME
    APP_POSTGRESQL_PORT
    KAFKA_BOOSTRAP_SERVER
    EVENTS_COLLECTOR_TOPIC # topic куда будут отправлены данные полученные по SYSLOG
    ALLOW_ANONYMOUS_LOGIN=(yes/no) # для логина в zookeper
    ALLOW_PLAINTEXT_LISTENER=(yes/no)
    ```

## Информация о файлах конфигурации
Все конфигурции можно найти в директории:
```
    src/events_gateway/config
```

## Локальный запуск

Для запуска локально нужно:
1. Активировать виртуальное окружение: 
```
source venv/bin/activate
```
2. Собрать приложение: 
``` 
python3 -m pip install .
```
3. Запустить приложение: 
``` 
events-gateway
```
4. Запустить тестовый клиент для отправки сообщения:
```
python3 test.py
```

## Накатка миграций происходит во время запуска консольной команды events-gateway.
