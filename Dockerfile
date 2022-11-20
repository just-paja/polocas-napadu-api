FROM alpine:3.16

WORKDIR /usr/local/app

COPY dist/polocas_napadu_api-*.tar.gz ./app.tar.gz
RUN tar -xf app.tar.gz --strip-components=1 -C .
RUN rm app.tar.gz

COPY requirements.txt requirements.txt
COPY gunicorn.py gunicorn.py

RUN \
  apk add --no-cache "python3=3.10.8-r0" "py3-pip=22.1.1-r0" libjpeg libwebp zlib postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
  pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

EXPOSE 80

CMD gunicorn -c gunicorn.py api.wsgi
