# Dockerfile

FROM python:3.6.3

ADD requirements.txt /requirements.txt

RUN cd / && pip install -r requirements.txt

RUN mkdir -p /opt/project_name
WORKDIR /opt/project_name

add . .

EXPOSE 5000

# If Flask project
# ENV FLASK_APP=/opt/project_name/app.py
# CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000", "--debugger", "--reload"]
