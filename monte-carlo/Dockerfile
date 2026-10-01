FROM python:3.13-slim
WORKDIR /app
COPY main_serial.py main_paralelo.py ./
COPY codigo ./codigo
RUN pip install --no-cache-dir psutil
ENTRYPOINT ["python", "main_paralelo.py"]
