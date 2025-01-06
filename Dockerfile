FROM python:3.9-slim

WORKDIR /app

COPY . /app

# Copy requirements first to cache dependencies
COPY requirements.txt /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ENV Bearst Cancerr_Flask_App=app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
