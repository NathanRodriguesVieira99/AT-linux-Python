import asyncio

from codigo.etapa_02_paralelismo.monte_carlo_parallel import monte_carlo_parallel
from codigo.etapa_05_monitoramento.system_monitor import monitor_processes

# simula uma task async de monitoramento
async def monitor_task(task_id: int) -> str:
    await asyncio.sleep(0.1)
    return f"Monitoramento {task_id} concluido"

# cria e executa 20 tarefas de monitoramento
async def run_monitoring_tasks() -> list[str]:
    # 20 tarefas assincronas.
    tasks = [
        asyncio.create_task(monitor_task(task_id))
        for task_id in range(1, 21)
    ]

    return await asyncio.gather(*tasks)

# executa o cálculo junto com as 20 tarefas e monitoramento dos processos
async def run_parallel_with_monitoring(
    chunk_size: int,
    n_tasks: int,
    log_file_path: str,
    monitor_file_path: str
):
    stop_event = asyncio.Event()

    calculation_task = asyncio.create_task(
        asyncio.to_thread(
            monte_carlo_parallel,
            chunk_size,
            n_tasks,
            log_file_path
        )
    )

    monitoring_task = asyncio.create_task(
        run_monitoring_tasks()
    )

    process_monitoring_task = asyncio.create_task(
        monitor_processes(
            monitor_file_path,
            stop_event
        )
    )

    try:
        parallel_result, monitoring_results = await asyncio.gather(
            calculation_task,
            monitoring_task
        )
    finally:
        stop_event.set()
        await process_monitoring_task

    print(
        f"{len(monitoring_results)} tarefas de monitoramento concluídas"
    )

    return parallel_result
