# # pull official base image
# FROM python:3.10-alpine as build-python

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     APPLICATION_PATH=/usr/src/app/ \
#     PATH=/root/.local/bin:${PATH}

# RUN apk update \
#     && apk add --virtual .build-deps \
#     && apk add --no-cache librdkafka \
#     curl \
#     postgresql-dev \
#     librdkafka-dev \
#     libffi-dev \
#     libxml2-dev \
#     libxslt-dev \
#     build-base

# COPY ./requirements.txt ${APPLICATION_PATH}

# # set work directory
# WORKDIR ${APPLICATION_PATH}


# # Allow installing dev dependencies to run tests
# RUN pip3 install -r requirements.txt


# # use alpline image. final image
# FROM python:3.10-alpine

# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWIRTEBYTECODE=1 \
#     APPLICATION_PATH=/usr/src/app/

# ENV PYTHONPATH /app:$PYTHONPATH

# WORKDIR ${APPLICATION_PATH}

# COPY --from=build-python /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
# COPY --from=build-python /usr/local/bin/ /usr/local/bin/

# COPY . ${APPLICATION_PATH}

# ARG PORT
# ENV PORT ${PORT:-8000}

FROM python:3.11-slim as deps
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


FROM python:3.11-slim as runtime
COPY --from=build /app/dist/*.whl /app/
RUN apt-get update -y && apt-get -y install gcc python3-dev
RUN pip --no-cache-dir install /app/*.whl
#USER app
ENTRYPOINT ["events-gateway"]