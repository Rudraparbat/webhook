FROM python:3.13.2-slim-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt 

COPY . /app

ENV DJANGO_SETTINGS_MODULE=webhooks.settings

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

CMD ["python" , "manage.py" , "runserver" , "0.0.0.0:8001"]