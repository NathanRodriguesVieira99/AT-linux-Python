import asyncio
import os
from pathlib import Path
from codigo.etapa_02_paralelismo.arguments import parse_arguments
from codigo.etapa_04_asyncio.monitoring import run_parallel_with_monitoring


def main_paralelo() -> None:
    arguments = parse_arguments()
    n_tasks = arguments.n_tasks
    chunk_size = arguments.chunk_size
    total = n_tasks * chunk_size
    total_cpu=os.cpu_count()
    logs_path = Path(__file__).parent / "codigo" / "logs"
    log_file_path = str(logs_path / "monte_carlo.log")
    monitor_file_path = str(logs_path / "process_monitor.log")

    # Versao paralela com 20 tarefas.
    parallel_hits, parallel_time = asyncio.run(
        run_parallel_with_monitoring(
            chunk_size,
            n_tasks,
            log_file_path,
            monitor_file_path
        )
    )
    parallel_pi = 4 * parallel_hits / total

    print("\nVersao paralela:")
    print("Número de nucleos: ",total_cpu)
    print(f"Valor estimado de PI: {parallel_pi}")
    print(f"Tempo: {parallel_time}s")


if __name__ == "__main__":
    main_paralelo()
