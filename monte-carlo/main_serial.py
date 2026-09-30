import time
from codigo.etapa_01_monte_carlo.monte_carlo_serial import monte_carlo_serial

# Versao serial: um unico processo executa todas as amostras.
def main_serial():
      total_amostras = 1_000_000
      start = time.perf_counter()
      serial_hits = monte_carlo_serial(total_amostras)
      serial_time = time.perf_counter() - start
      serial_pi = 4 * serial_hits / total_amostras # estimativa de PI
      print("Versao serial:")
      print("Processos utilizados: 1")
      print(f"Valor estimado de PI: {serial_pi}")
      print(f"Tempo: {serial_time}s")

if __name__ == "__main__":
    main_serial()
