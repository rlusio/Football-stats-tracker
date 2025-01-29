FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000

CMD ["sh", "-c", "python down_from_google_drive.py && python manage.py migrate && gunicorn FootballStatsTrackerProject.wsgi:application -b 0.0.0.0:${PORT:-8000}"]
