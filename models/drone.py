import math


class Drone:
    def __init__(self, id, posicao_inicial, destino, velocidade):
        self.id = id

        self.x_inicial = posicao_inicial[0]
        self.y_inicial = posicao_inicial[1]

        self.x = posicao_inicial[0]
        self.y = posicao_inicial[1]

        self.destino_x = destino[0]
        self.destino_y = destino[1]

        self.velocidade = velocidade
        self.status = "em_movimento"

        self.distancia_percorrida = 0
        self.tempo_chegada = None

        self.trajetoria = [(self.x, self.y)]

    def distancia_ate_destino(self):
        return math.sqrt(
            (self.destino_x - self.x) ** 2 +
            (self.destino_y - self.y) ** 2
        )

    def mover(self):
        if self.status != "em_movimento":
            return

        distancia = self.distancia_ate_destino()

        if distancia <= self.velocidade:
            self.distancia_percorrida += distancia
            self.x = self.destino_x
            self.y = self.destino_y
            self.status = "chegou"
            self.trajetoria.append((self.x, self.y))
            return

        direcao_x = (self.destino_x - self.x) / distancia
        direcao_y = (self.destino_y - self.y) / distancia

        self.x += direcao_x * self.velocidade
        self.y += direcao_y * self.velocidade

        self.distancia_percorrida += self.velocidade
        self.trajetoria.append((self.x, self.y))