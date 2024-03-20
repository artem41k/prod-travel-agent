FROM python:3.12.1-alpine3.19

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080
ENV PYTHONUNBUFFERED 1

CMD sh -c "python3 manage.py migrate --noinput && python3 manage.py runserver 0.0.0.0:8080"