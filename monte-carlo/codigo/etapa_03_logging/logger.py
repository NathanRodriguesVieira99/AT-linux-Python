import os
from datetime import datetime


def write_log_file(
    log_file_path: str,
    completed_tasks: int,
    total_tasks: int
) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds") # data 
    process_id = os.getpid() # PID
    progress = completed_tasks / total_tasks * 100 # etapa do progresso

    # cria de fato o arquivo de logs com os valores corretos
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(
            f"{timestamp} | "
            f"progresso={completed_tasks}/{total_tasks} "
            f"({progress:.1f}%) | "
            f"pid={process_id}\n"
        )
