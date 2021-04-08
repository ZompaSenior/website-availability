FROM python:3.9-alpine

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /opt/monitor

# VOLUME /usr/src/app/public
WORKDIR /opt/monitor

# RUN apk update \
# 	&& apk add --no-cache --virtual build-deps gcc g++ python3-dev musl-dev \
# 	&& apk add --no-cache postgresql-dev \
# 	&& apk add --no-cache jpeg-dev zlib-dev \
# 	&& apk add --no-cache libffi-dev openssl-dev \
# 	&& apk add --no-cache pcre-dev

COPY . /opt/monitor/

RUN pip install --no-cache-dir -r requirements.txt

# RUN apk del build-deps

CMD ["python3", "-m", "main", \
	"/opt/monitor/config/url_list.txt", \
	"/opt/monitor/config/monitor.ini"]