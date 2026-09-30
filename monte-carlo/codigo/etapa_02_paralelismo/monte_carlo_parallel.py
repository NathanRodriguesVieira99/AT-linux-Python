import time
from multiprocessing import Pool
from codigo.etapa_01_monte_carlo.monte_carlo_serial import monte_carlo_serial
from codigo.etapa_03_logging.logger import write_log_file


def monte_carlo_parallel(
    chunk_size: int,
    n_tasks: int,
    log_file_path: str
):
    # valores iniciais
    start = time.perf_counter()
    partial_hits = []

    # arquivo de logs
    write_log_file(log_file_path, 0, n_tasks)

    # Cada worker recebe um bloco com chunk_size
    with Pool(processes=n_tasks) as pool:
        results = pool.imap_unordered(
            monte_carlo_serial,
            [chunk_size] * n_tasks
        )

        # adiciona valores ao log
        for completed_tasks, hits in enumerate(results, start=1):
            partial_hits.append(hits)
            write_log_file(
                log_file_path,
                completed_tasks,
                n_tasks
            )

    # valores finais após a execucao
    elapsed_time = time.perf_counter() - start
    total_hits = sum(partial_hits)
    return total_hits, elapsed_time
