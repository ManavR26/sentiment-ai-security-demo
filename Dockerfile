# 🚨 VULNERABILITY: Extremely outdated base image packed with OS-level CVEs
FROM python:3.6-jessie

# 🚨 VULNERABILITY: Running as root user (No USER instruction)
WORKDIR /app
COPY app.py .

RUN pip install flask

CMD ["python", "app.py"]
