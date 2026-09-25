import asyncio
import time

async def list_data(n:int)->str:
  print(f"Iniciando tarefa {n}")
  await asyncio.sleep(2)   # simulando uma demora de 2s
  print(f"Finalizando tarefa {n}")
  return f"Resultado {n}"


async def main()->None:
    task_start= time.perf_counter()
    tasks = [
       list_data(5),
       list_data(7),
       list_data(9),
       list_data(1),
       list_data(2),
    ]
    results = await asyncio.gather(*tasks)
    total_time = time.perf_counter() - task_start
    print("\nResultados:")
    print(results)
    print(f"Tempo Total: {total_time:.2f} segundos")

if __name__ == "__main__":
   asyncio.run(main())
