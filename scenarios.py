import random

from models.drone import Drone


def cenario_sem_colisao():
    return [
        Drone(id=1, posicao_inicial=(0, 0), destino=(10, 0), velocidade=1),
        Drone(id=2, posicao_inicial=(0, 3), destino=(10, 3), velocidade=1),
        Drone(id=3, posicao_inicial=(0, 6), destino=(10, 6), velocidade=1),
        Drone(id=4, posicao_inicial=(0, 9), destino=(10, 9), velocidade=1),
    ]


def cenario_colisao_central():
    return [
        Drone(id=1, posicao_inicial=(0, 0), destino=(10, 10), velocidade=1),
        Drone(id=2, posicao_inicial=(10, 10), destino=(0, 0), velocidade=1),
        Drone(id=3, posicao_inicial=(0, 10), destino=(10, 0), velocidade=1),
        Drone(id=4, posicao_inicial=(10, 0), destino=(0, 10), velocidade=1),
    ]


def cenario_alta_densidade():
    return [
        Drone(id=1, posicao_inicial=(0, 0), destino=(10, 10), velocidade=1),
        Drone(id=2, posicao_inicial=(10, 10), destino=(0, 0), velocidade=1),
        Drone(id=3, posicao_inicial=(0, 10), destino=(10, 0), velocidade=1),
        Drone(id=4, posicao_inicial=(10, 0), destino=(0, 10), velocidade=1),
        Drone(id=5, posicao_inicial=(5, 0), destino=(5, 10), velocidade=1),
        Drone(id=6, posicao_inicial=(5, 10), destino=(5, 0), velocidade=1),
        Drone(id=7, posicao_inicial=(0, 5), destino=(10, 5), velocidade=1),
        Drone(id=8, posicao_inicial=(10, 5), destino=(0, 5), velocidade=1),
    ]


def gerar_cenario_aleatorio(
    quantidade_drones,
    largura_ambiente,
    altura_ambiente,
    velocidade_minima,
    velocidade_maxima,
    seed=None
):
    if seed is not None:
        random.seed(seed)

    drones = []

    for i in range(1, quantidade_drones + 1):
        x_inicial = random.uniform(0, largura_ambiente)
        y_inicial = random.uniform(0, altura_ambiente)

        destino_x = random.uniform(0, largura_ambiente)
        destino_y = random.uniform(0, altura_ambiente)

        velocidade = random.uniform(velocidade_minima, velocidade_maxima)

        drone = Drone(
            id=i,
            posicao_inicial=(x_inicial, y_inicial),
            destino=(destino_x, destino_y),
            velocidade=velocidade
        )

        drones.append(drone)

    return drones


def cenario_aleatorio_baixa_densidade(config, seed=None):
    return gerar_cenario_aleatorio(
        quantidade_drones=10,
        largura_ambiente=config["largura_ambiente"],
        altura_ambiente=config["altura_ambiente"],
        velocidade_minima=0.8,
        velocidade_maxima=1.5,
        seed=seed
    )


def cenario_aleatorio_media_densidade(config, seed=None):
    return gerar_cenario_aleatorio(
        quantidade_drones=25,
        largura_ambiente=config["largura_ambiente"],
        altura_ambiente=config["altura_ambiente"],
        velocidade_minima=0.8,
        velocidade_maxima=1.5,
        seed=seed
    )


def cenario_aleatorio_alta_densidade(config, seed=None):
    return gerar_cenario_aleatorio(
        quantidade_drones=50,
        largura_ambiente=config["largura_ambiente"],
        altura_ambiente=config["altura_ambiente"],
        velocidade_minima=0.8,
        velocidade_maxima=1.5,
        seed=seed
    )


def obter_cenario(nome, config=None, seed=None):
    cenarios_fixos = {
        "sem_colisao": cenario_sem_colisao,
        "colisao_central": cenario_colisao_central,
        "alta_densidade": cenario_alta_densidade,
    }

    cenarios_aleatorios = {
        "aleatorio_baixa_densidade": cenario_aleatorio_baixa_densidade,
        "aleatorio_media_densidade": cenario_aleatorio_media_densidade,
        "aleatorio_alta_densidade": cenario_aleatorio_alta_densidade,
    }

    if nome in cenarios_fixos:
        return cenarios_fixos[nome]()

    if nome in cenarios_aleatorios:
        if config is None:
            raise ValueError("Cenários aleatórios precisam receber o config.")

        return cenarios_aleatorios[nome](config, seed)

    raise ValueError(f"Cenário '{nome}' não encontrado.")