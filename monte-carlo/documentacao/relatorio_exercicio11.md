# Relatório - Exercício 11

## 1. Aproximação de PI por Monte Carlo

Foram gerados pontos `(x, y)` com distribuição uniforme no intervalo `(-1, 1)`. Um ponto foi contado como `hit` quando:

```python
x**2 + y**2 <= 1
```

A estimativa foi calculada por:

```text
pi = 4 * hits / total
```

## 2. Versões serial e paralela

O programa possui duas versões:

- **Serial:** executa todas as amostras em um único processo.
- **Paralela:** usa `multiprocessing.Pool` para distribuir o cálculo entre workers.

Na versão paralela, o trabalho é dividido em blocos. Cada worker executa `chunk_size` amostras, e a quantidade de blocos/processos é definida por `n_tasks`.

Os parâmetros são configuráveis pela linha de comando:

```powershell
python .\main.py --n-tasks 2 --chunk-size 1000000
```

Nesse exemplo, o total processado é:

```text
total = n_tasks * chunk_size = 2 * 1.000.000 = 2.000.000 amostras
```

## 3. Comparação de execução

Resultado obtido com o comando anterior (exemplo, pois os valores não são fixos):

| Versão   | PI estimado |     Tempo total |
| -------- | ----------: | --------------: |
| Serial   |    3.140878 | 0.7701 segundos |
| Paralela |    3.142124 | 0.6119 segundos |

Os valores de PI são próximos porque as duas versões usam o mesmo método estatístico. As pequenas diferenças ocorrem devido à geração aleatória dos pontos.

O ganho aproximado foi:

```text
ganho = tempo_serial / tempo_paralelo
ganho = 0.7701 / 0.6119
ganho aproximado = 1,26x
```

## 4. Log e tarefas assíncronas

Durante a execução paralela, o programa gera dois arquivos locais:

- `monte_carlo.log`: registra horário, progresso e PID responsável pela escrita.
- `process_monitor.log`: registra PIDs dos workers, status e uso de CPU.

Além do cálculo, são executadas 20 tarefas assíncronas com `asyncio`. Elas simulam rotinas de monitoramento usando `await asyncio.sleep(0.1)` e não bloqueiam diretamente o cálculo principal.

A chamada bloqueante do `multiprocessing.Pool` é executada com `asyncio.to_thread()`, enquanto o event loop executa as tarefas de monitoramento.

## 5. Análise técnica

### 5.1 Evidências de múltiplos processos

O arquivo `process_monitor.log` registrou diferentes PIDs de workers, por exemplo:

```text
parent_pid=30048 | worker_pid=31336 | status=running
parent_pid=30048 | worker_pid=31876 | status=running
```

Os PIDs distintos comprovam que o `Pool` criou múltiplos processos Python. Os registros em horários próximos indicam execução simultânea.

### 5.2 Uso de CPU

Foram observadas amostras como:

```text
worker_pid=31336 | cpu_percent=92.5 | status=running
worker_pid=31876 | cpu_percent=93.0 | status=running
```

Os valores elevados indicam que os workers estavam executando uma tarefa CPU-bound. O uso de processos permite utilizar múltiplos núcleos sem a limitação do GIL que afetaria threads Python nesse tipo de cálculo.

### 5.3 Justificativa do chunking

O chunking reduz o overhead porque cada worker recebe uma quantidade significativa de amostras antes de retornar um resultado. Isso diminui a quantidade de operações de distribuição, comunicação e serialização entre o processo principal e os workers.

Blocos muito pequenos aumentam o custo de coordenação. Blocos muito grandes podem causar desequilíbrio, pois alguns workers podem terminar antes dos demais. O valor de `chunk_size` deve equilibrar overhead e distribuição do trabalho.

### 5.4 Computação, I/O e tarefas assíncronas

A simulação Monte Carlo utiliza intensivamente a CPU nos workers. Ao mesmo tempo, o processo principal realiza I/O ao atualizar os logs, e o event loop executa as 20 tarefas assíncronas de monitoramento.

O logging acrescenta um pequeno custo de I/O, pois ocorre quando os blocos terminam, e não a cada ponto gerado. As tarefas `asyncio` usam `await` para liberar o event loop durante a espera. Dessa forma, computação, I/O e monitoramento coexistem sem bloquear diretamente o cálculo principal.
