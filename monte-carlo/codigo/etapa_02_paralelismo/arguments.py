import argparse

# le os parametros da linha de comando e define quantos processos e samples cada chunk que será usado.
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimativa de PI usando Monte Carlo"
    )
    parser.add_argument(
        "--n-tasks",
        type=int,
        default=4,
        help="Numero de processos e blocos"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=250_000,
        help="Quantidade de amostras em cada bloco"
    )
    return parser.parse_args()
