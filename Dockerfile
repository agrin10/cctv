ARG PYTHON_VERSION=3.9.13
FROM docker.arvancloud.ir/python:${PYTHON_VERSION} as base

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flask-migrate
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0


EXPOSE 8080

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV FLASK_DEBUG=True

# Run database migration and start Flask app
CMD ["bash", "-c", "flask db upgrade && flask run"]
