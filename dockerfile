FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=gps_project.settings
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "gps_project.wsgi", "--bind", "0.0.0.0:8000"]