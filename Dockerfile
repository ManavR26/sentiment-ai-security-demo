# 🚨 VULNERABILITY 4: Extremely outdated base image packed with CVEs
FROM python:3.7-buster

WORKDIR /app
COPY app.py .

RUN pip install flask

CMD ["python", "app.py"]
