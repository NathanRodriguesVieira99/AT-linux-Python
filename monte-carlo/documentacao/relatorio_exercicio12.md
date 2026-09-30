# Exercício 2

Criei o Dockerfile com todos os requisitos solicitados, o problema é que meu Notebook não roda o Docker mesmo com a virtualização ativa, então rodei no meu Desktop, porém em uma configuração diferente dos primeiros testes fora do Docker.

```docker
FROM python:3.13-slim
WORKDIR /app
COPY main.py .
COPY codigo ./codigo
RUN pip install --no-cache-dir psutil
CMD ["python", "main.py"]

```
