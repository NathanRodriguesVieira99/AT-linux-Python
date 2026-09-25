# Relatorio - Exercicio 12

## 1. Objetivo

O programa do Exercicio 11 foi reutilizado e preparado para execucao dentro de um container Docker. A aplicacao mantem as versoes serial e paralela da simulacao Monte Carlo, o chunking, o logging continuo, as 20 tarefas asyncio e o monitoramento de processos.

## 2. Arquitetura de containerizacao

A imagem foi definida pelo seguinte `Dockerfile`:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY main.py .
COPY codigo ./codigo
RUN pip install --no-cache-dir psutil
CMD ["python", "main.py"]
```

A imagem `python:3.13-slim` fornece um ambiente Linux com Python. O codigo e copiado para `/app`, e a dependencia `psutil` e instalada durante o build.

## 3. Execucao do container

A imagem foi construida com:

```powershell
docker build . -t monte-carlo
```

A execucao paralela com persistencia dos logs foi realizada com:

```powershell
docker run --rm -v "${PWD}\codigo\logs:/app/codigo/logs" monte-carlo python main.py --n-tasks 2 --chunk-size 1000000
```

O volume conecta a pasta local `codigo/logs` ao diretorio `/app/codigo/logs` dentro do container. Assim, os arquivos gerados pela aplicacao permanecem no host depois do encerramento do container.

## 4. Resultado da execucao containerizada

Resultado obtido (exemplo pois os valores não são fixos):

```text
20 tarefas de monitoramento concluidas

Versao serial:
Valor estimado de PI: 3.143446
Tempo: 0.8281 segundos

Versao paralela:
Valor estimado de PI: 3.143918
Tempo: 0.5001 segundos
```

| Versao   | PI estimado |     Tempo total |
| -------- | ----------: | --------------: |
| Serial   |    3.143446 | 0.8281 segundos |
| Paralela |    3.143918 | 0.5001 segundos |

O ganho aproximado da execucao paralela foi:

```text
ganho = 0.8281 / 0.5001
 ganho aproximado = 1,66x
```

As pequenas diferencas entre os valores de PI ocorrem porque os pontos sao gerados aleatoriamente.

## 5. Paralelismo dentro do container

O programa paralelo continua utilizando `multiprocessing.Pool`. O processo principal do container cria os workers Python, e cada worker executa um bloco com `chunk_size` amostras.

Com os parametros usados:

```text
n_tasks = 2
chunk_size = 1.000.000
total = 2.000.000 amostras
```

O container nao elimina os processos criados pelo Python. Eles continuam sendo processos do sistema operacional, mas ficam dentro do namespace do container e sao administrados pelo Docker Engine.

As 20 tarefas `asyncio` continuam executando durante a simulacao paralela. A chamada bloqueante do `Pool` e executada com `asyncio.to_thread()`, permitindo que o event loop continue executando as tarefas de monitoramento.

## 6. Monitoramento a partir do host

Para manter o container ativo durante a observacao, foi utilizada uma execucao em segundo plano:

```powershell
docker run -d --name monte-carlo-ex12 -v "${PWD}\codigo\logs:/app/codigo/logs" monte-carlo python main.py --n-tasks 4 --chunk-size 5000000
```

Os comandos de monitoramento utilizados foram:

```powershell
docker ps
docker top monte-carlo-ex12
docker stats --no-stream monte-carlo-ex12
```

`docker ps` identifica o container ativo. `docker top` exibe o processo principal e os workers associados ao container. `docker stats` apresenta o consumo de CPU, memoria, rede e I/O.

O arquivo `process_monitor.log` tambem registra os workers observados pela aplicacao, com PID, status e percentual de CPU:

```text
timestamp | parent_pid | worker_pid | cpu_percent | status
```

### Evidencias coletadas

Durante uma execucao com quatro workers e 20.000.000 amostras por bloco, o host registrou:

```text
CONTAINER ID   NAME               CPU %    MEM USAGE / LIMIT   MEM %   PIDS
31c304126d4e   monte-carlo-ex12   352.30%  31.11MiB / 7.715GiB 0.39%   13
```

O valor de `352.30%` indica utilizacao simultanea de varios nucleos pelo container. O campo `PIDS=13` confirma que havia multiplos processos ativos.

O comando `docker top monte-carlo-ex12` identificou o processo principal do container:

```text
UID   PID  PPID  C   TIME       CMD
root  853  829   97  00:00:11   python main.py --n-tasks 4 --chunk-size 20000000
```

Nesta execucao, o `docker top` do Docker Desktop listou o processo principal. Os workers foram identificados pelo monitor da aplicacao no arquivo persistido:

```text
2026-09-25T19:31:25 | 1 | 9  | 99.1 | running
2026-09-25T19:31:25 | 1 | 10 | 97.1 | running
2026-09-25T19:31:25 | 1 | 11 | 98.3 | running
2026-09-25T19:31:26 | 1 | 8  | 117.0 | running
2026-09-25T19:31:26 | 1 | 9  | 98.5 | running
2026-09-25T19:31:26 | 1 | 10 | 118.2 | running
2026-09-25T19:31:26 | 1 | 11 | 98.7 | running
```

Esses registros comprovam a existencia de quatro workers distintos dentro do container, com uso elevado de CPU durante a simulacao. O log foi persistido no host por meio do volume Docker.

## 7. Diferencas entre host e container

Na execucao nativa, o Python e iniciado diretamente pelo sistema operacional do host. Os workers aparecem diretamente na lista de processos do sistema.

Na execucao containerizada, o Python e iniciado dentro de `/app`, usando a imagem Linux `python:3.13-slim`. Os workers continuam existindo, mas sao associados ao container e podem ser observados pelo host por meio de comandos Docker, como `docker top` e `docker stats`.

O container acrescenta uma camada de isolamento e gerenciamento. Por isso, pode haver pequeno custo adicional de inicializacao, montagem do volume e gerenciamento do ambiente. O calculo em si continua sendo executado por processos Python e utiliza os recursos do kernel e da CPU do host.

## 8. Impactos do Docker

### Isolamento

O Docker isola o sistema de arquivos, os processos e o ambiente de execucao da aplicacao. O programa usa a imagem definida e nao depende diretamente da instalacao local de Python ou `psutil`.

### Monitoramento

O host consegue monitorar o container com `docker ps`, `docker top` e `docker stats`. Dentro da aplicacao, `psutil` registra os workers e o uso de CPU no arquivo `process_monitor.log`.

### Consumo de recursos

Os workers continuam consumindo CPU e memoria reais do host. O Docker organiza e exibe esse consumo, mas nao torna o processamento gratuito. A criacao do container, os processos do `Pool`, as tarefas de monitoramento e as escritas nos logs geram custos adicionais.

O volume evita a perda dos logs quando o container e removido. O logging ocorre por bloco concluido, reduzindo o custo de I/O em comparacao com escrever uma linha para cada amostra.

## 9. Conclusao

O programa do Exercicio 11 foi executado com sucesso dentro de um container Linux. A execucao paralela produziu uma estimativa de PI e apresentou menor tempo que a versao serial no teste realizado.

O `multiprocessing.Pool` manteve o paralelismo por processos dentro do container, enquanto `asyncio` executou as tarefas de monitoramento. O volume persistiu os arquivos de log no host, e os comandos Docker permitiram observar os processos e o consumo de recursos.
