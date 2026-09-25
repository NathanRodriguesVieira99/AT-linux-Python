import time

def list_data(n:int)->str:
  print(f"Iniciando tarefa {n}")
  time.sleep(2)   # simulando uma demora de 2s
  print(f"Finalizando tarefa {n}")
  return f"Resultado {n}"


def main()->None:
    start= time.perf_counter()
    numbers = [5,7,9,1,2]
    results =[]
    for number in numbers:
        results.append(list_data(number))
    total_time = time.perf_counter() - start
    print("\nResultados:")
    print(results)
    print(f"Tempo Total: {total_time:.2f} segundos")

if __name__ == "__main__":
   main()

