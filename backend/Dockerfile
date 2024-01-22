FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /backend
COPY . /backend/
RUN pip install -r requirements.txt
RUN python manage.py migrate
EXPOSE 8000
