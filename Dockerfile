# Dockerfile

FROM python:3.7.0

ADD requirements.txt /requirements.txt

RUN cd / && pip install -r requirements.txt

RUN mkdir -p /opt/project_name
WORKDIR /opt/project_name

add . .

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

EXPOSE 5000

ENV FLASK_APP=/opt/project_name/app.py
CMD ["flask", "run", "--host", "0.0.0.0"]
