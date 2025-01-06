FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file to leverage Docker cache
COPY requirements.txt /app

# Install dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Set environment variables
ENV FLASK_APP=app.py

# Expose the application port
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
