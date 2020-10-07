FROM python:3.8

RUN apt-get update \
    && apt-get install -y --no-install-recommends default-mysql-client \
	;

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 8000
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]