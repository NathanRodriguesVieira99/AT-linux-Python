import random


def monte_carlo_sequencial(samples: int) -> int:
    hits = 0

    # Cada iteracao representa um ponto no quadrado [-1, 1] x [-1, 1].
    for _ in range(samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        # O ponto esta dentro do circulo de raio 1 quando x^2 + y^2 <= 1.
        if x**2 + y**2 <= 1:
            hits += 1

    return hits
