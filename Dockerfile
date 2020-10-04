FROM alpine

WORKDIR /usr/local/app

COPY dist/polocas-napadu-api-*.tar.gz ./app.tar.gz
RUN tar -xf app.tar.gz --strip-components=1 -C .
RUN rm app.tar.gz

COPY crontab /etc/cron.d/transaction-parser
COPY requirements.txt requirements.txt
COPY gunicorn.py gunicorn.py

RUN \
  apk add --update py-pip jpeg-dev zlib-dev libjpeg openrc busybox-initscripts && \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
  pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

RUN rc-update add crond

EXPOSE 80

CMD python3 ./manage.py collectstatic --no-input && python3 ./manage.py migrate && gunicorn -c gunicorn.py api.wsgi
