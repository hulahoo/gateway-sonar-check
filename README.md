# Events Gateway

Сервис для приема входящих сообщений от SIEM и маршрутизации их дальнейшей в Kafka

## Информация о протоколе SYSLOG в проекте
Для настройки порта и хоста по которым сервис должен быть доступным, указываем в .env файле следующее(пример):
    ```
    EVENTS_PORT=5000
    EVENTS_HOST=localhost
    ```

## Информаци о ENV-параметрах
Имеющиеся env-параметры в проекте(пример):
    ```
    EVENTS_PORT=500
    EVENTS_HOST=localhost
    SESSION_COOKIE_SECURE=True
    CSRF_ENABLED=True
    APP_POSTGRESQL_HOST=localhost
    APP_POSTGRESQL_PASSWORD=password
    APP_POSTGRESQL_USER=postgres
    APP_POSTGRESQL_NAME=db
    APP_POSTGRESQL_PORT=5432
    KAFKA_BOOSTRAP_SERVER=localhost:9092
    EVENTS_COLLECTOR_TOPIC=collector
    ```

## Информация о файлах конфигурации
Все конфигурции можно найти в директории:
```
    src/events_gateway/config
```

## Локальный запуск

Для запуска локально нужно:

1. Создать виртуальное окружение:

```bash
python3 -m venv venv
```

2. Активировать виртуальное окружение: 
```bash
source venv/bin/activate
```
3. Собрать приложение: 

```bash
python3 -m pip install .
```

4. Запустить приложение: 

```bash
events-gateway
```

5. Запустить тестовый клиент для отправки сообщения:
```bash
python3 test.py
```

### Требования к инфраструктуре
1. Минимальная версия Kafka:
  ```yaml
    wurstmeister/kafka:>=2.13-2.7.2
  ```
2. Минимальная версия Postgres:
  ```yaml
    postgres:>=14-alpine
  ```
3. Минимальная версия zookeper:
  ```yaml
    wurstmeister/zookeeper
  ```

### Запуск с помощью докера

1. Dockerfile:
```dockerfile
FROM python:3.10.8-slim as deps
WORKDIR /app
COPY . ./
RUN apt-get update -y && apt-get -y install gcc python3-dev
RUN pip --no-cache-dir install -r requirements.txt 
RUN pip --no-cache-dir install -r requirements.setup.txt 
RUN pip install -e .

FROM deps as build
ARG ARTIFACT_VERSION=local
RUN python setup.py sdist bdist_wheel
RUN ls -ll /app/
RUN ls -ll /app/dist/


FROM python:3.10.8-slim as runtime
COPY --from=build /app/dist/*.whl /app/
RUN apt-get update -y && apt-get -y install gcc python3-dev
RUN pip --no-cache-dir install /app/*.whl
ENTRYPOINT ["events-gateway"]
```

2. docker-compose.yml
```yaml
version: '3'


services:
  zookeeper:
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"
  kafka:
    image: wurstmeister/kafka:latest
    ports:
      - target: 9094
        published: 9094
        protocol: tcp
        mode: host
    environment:
      HOSTNAME_COMMAND: "docker info | grep ^Name: | cut -d' ' -f 2"
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: INSIDE://:9092,OUTSIDE://_{HOSTNAME_COMMAND}:9094
      KAFKA_LISTENERS: INSIDE://:9092,OUTSIDE://:9094
      KAFKA_INTER_BROKER_LISTENER_NAME: INSIDE
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  postgres_db:
    image: postgres:14-alpine
    container_name: db
    restart: unless-stopped
    expose:
      - 5432 
    environment:
      POSTGRES_DB: db
      POSTGRES_USER: dbuser
      POSTGRES_PASSWORD: test

  gateway:
    restart: always
    build: ./
    ports:
    - "8080:8080"
    environment:
      EVENTS_PORT: 9000
      EVENTS_HOST: 0.0.0.0
      KAFKA_GROUP_ID: main
      KAFKA_BOOTSTRAP_SERVER: kafka:9092
      EVENTS_COLLECTOR_TOPIC: syslog

      APP_POSTGRESQL_USER: dbuser
      APP_POSTGRESQL_PASSWORD: test
      APP_POSTGRESQL_NAME: db
      APP_POSTGRESQL_HOST: postgres_db
      APP_POSTGRESQL_PORT: 5432
    depends_on:
      - postgres_db

 
networks:
    external:
      name: kafka_net
```

3. Запуск контейнеров:
```bash
docker-compose up --build
```

4. Применить дамп файла для бд в контейнере:
```bash
cat restore.sql | docker exec -i db psql -U dbuser -d db
```

5. Перзапустить контейнер worker
