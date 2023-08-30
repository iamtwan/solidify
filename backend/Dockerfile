# Official Python Image
FROM python:3.10-bullseye

# Update Package Installer
RUN python -m pip install --upgrade pip

# Env Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Working Directory
WORKDIR /app

# Dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Project
COPY . /app/


# Start Server - development
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
# Start Server - GCP deployment
EXPOSE 8080
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
