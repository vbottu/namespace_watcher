FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.11-alpine
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
 # Create a non-root user with UID 1000
RUN adduser -D -u 1000 watcher 
# Switch to the non-root user
USER watcher                   
CMD ["python", "main.py"]
