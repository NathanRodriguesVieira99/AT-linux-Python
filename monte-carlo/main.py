import asyncio
import time
from pathlib import Path

from codigo.etapa_01_monte_carlo.monte_carlo_sequencial import monte_carlo_sequencial
from codigo.etapa_02_paralelismo.arguments import parse_arguments
from codigo.etapa_04_asyncio.monitoring import run_parallel_with_monitoring


def main() -> None:
    arguments = parse_arguments()
    n_tasks = arguments.n_tasks
    chunk_size = arguments.chunk_size

    # O total serial deve ser igual ao total processado pelos workers.
    total = n_tasks * chunk_size
    logs_path = Path(__file__).parent / "codigo" / "logs"
    log_file_path = str(logs_path / "monte_carlo.log")
    monitor_file_path = str(logs_path / "process_monitor.log")

    # Versao serial: um unico processo executa todas as amostras.
    start = time.perf_counter()
    serial_hits = monte_carlo_sequencial(total)
    serial_time = time.perf_counter() - start
    serial_pi = 4 * serial_hits / total

    # Versao paralela com 20 tarefas de monitoramento.
    parallel_hits, parallel_time = asyncio.run(
        run_parallel_with_monitoring(
            chunk_size,
            n_tasks,
            log_file_path,
            monitor_file_path
        )
    )
    parallel_pi = 4 * parallel_hits / total

    print("Versao serial:")
    print(f"Valor estimado de PI: {serial_pi}")
    print(f"Tempo: {serial_time:.4f} segundos")

    print("\nVersao paralela:")
    print(f"Valor estimado de PI: {parallel_pi}")
    print(f"Tempo: {parallel_time:.4f} segundos")


if __name__ == "__main__":
    main()
