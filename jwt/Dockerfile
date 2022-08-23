FROM python:3.11-rc-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
ENTRYPOINT ["python3", "/app/jwt.py"]