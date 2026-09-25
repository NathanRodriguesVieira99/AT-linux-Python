import asyncio
import os
from datetime import datetime
import psutil

# Coleta o percentual da CPU e o status do worker
async def read_worker_metrics(worker: psutil.Process) -> tuple[float, str] | None:
    try:
        cpu_percent = await asyncio.to_thread(
            worker.cpu_percent,
            0.05
        )
        return cpu_percent, worker.status()
    except psutil.NoSuchProcess:
        return None

# monitora os processos, registra PID, CPU, status e salva no arquivo de log
async def monitor_processes(
    monitor_file_path: str,
    stop_event: asyncio.Event,
    interval: float = 0.1
) -> None:
    parent = psutil.Process(os.getpid())

    with open(monitor_file_path, "w", encoding="utf-8") as monitor_file:
        monitor_file.write(
            "timestamp | parent_pid | worker_pid | cpu_percent | status\n"
        )

        while not stop_event.is_set():
            timestamp = datetime.now().isoformat(timespec="seconds")
            workers = parent.children(recursive=True)

            if not workers:
                monitor_file.write(
                    f"{timestamp} | {parent.pid} | nenhum | 0.0 | aguardando\n"
                )
            else:
                metrics = await asyncio.gather(*(
                    read_worker_metrics(worker)
                    for worker in workers
                ))

                for worker, worker_metrics in zip(workers, metrics):
                    if worker_metrics is not None:
                        cpu_percent, status = worker_metrics
                        monitor_file.write(
                            f"{timestamp} | {parent.pid} | "
                            f"{worker.pid} | {cpu_percent:.1f} | {status}\n"
                        )

            monitor_file.flush()
            await asyncio.sleep(interval)

        # Registra o resultado final após o término do cálculo.
        timestamp = datetime.now().isoformat(timespec="seconds")
        monitor_file.write(
            f"{timestamp} | {parent.pid} | nenhum | 0.0 | finalizado\n"
        )
