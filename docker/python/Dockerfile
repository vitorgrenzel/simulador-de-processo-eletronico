FROM python:3.8-slim

# RUN apk update \
#     && apk add --no-cache bash \
#     && apk add gcc \
#     && apk add musl-dev \
#     && apk add linux-headers \
#     && apk add jpeg-dev \
#     && apk add zlib-dev \
#     && apk add mariadb-dev \
#     && apk add libffi-dev

RUN apt-get update && apt-get install -y --no-install-recommends\
    postgresql-client python3-psycopg2 python3-dev gcc && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y gettext libgettextpo-dev libyaml-dev

# install pypi packages
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt 
    # && python manage.py makemigrations \
    # && python manage.py migrate 
    # && rm /usr/bin/mysql*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
