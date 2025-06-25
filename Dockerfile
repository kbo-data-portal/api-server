FROM python:3.12-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password kbouser
RUN chown -R kbouser:kbouser /app

USER kbouser
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
