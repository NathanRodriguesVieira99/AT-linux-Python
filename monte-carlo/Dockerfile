FROM python:3.13-slim
WORKDIR /app
COPY main.py .
COPY codigo ./codigo
RUN pip install --no-cache-dir psutil
CMD ["python", "main.py"]
