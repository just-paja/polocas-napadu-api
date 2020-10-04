FROM alpine

WORKDIR /usr/local/app

COPY dist/polocas-napadu-api-*.tar.gz ./app.tar.gz
RUN tar -xf app.tar.gz --strip-components=1 -C .
RUN rm app.tar.gz
ADD requirements.txt requirements.txt

RUN \
  apk add --update py-pip jpeg-dev zlib-dev libjpeg && \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
  pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

EXPOSE 80

CMD [ "gunicorn", "-b 0.0.0.0:80", "api.wsgi" ]
