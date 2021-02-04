# pull official base image
# FROM python:3.8.3-alpine
FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# Install postgres client
RUN apk add --update --no-cache postgresql-client

# Install individual dependencies
# so that we could avoid installing extra packages to the container
RUN python3 -m pip install --upgrade pip

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps \
	&& pip install -r /requirements.txt

# Remove dependencies
# RUN apk del .tmp-build-deps

RUN mkdir /CTHS
WORKDIR /CTHS
COPY ./CTHS /CTHS

# [Security] Limit the scope of user who run the docker image
RUN adduser -D iss01

USER iss01

# run entrypoint.sh
CMD ["/home/iss01/hospital_application/Clinic-Treatment-History-System/CTHS/entrypoint.sh"]