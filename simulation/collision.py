import math


def calcular_distancia_entre_drones(drone_a, drone_b):
    return math.sqrt(
        (drone_a.x - drone_b.x) ** 2 +
        (drone_a.y - drone_b.y) ** 2
    )


def verificar_colisoes(drones, raio_colisao, passo_atual, eventos):
    for i in range(len(drones)):
        for j in range(i + 1, len(drones)):
            drone_a = drones[i]
            drone_b = drones[j]

            if drone_a.status != "em_movimento" or drone_b.status != "em_movimento":
                continue

            distancia = calcular_distancia_entre_drones(drone_a, drone_b)

            if distancia <= raio_colisao:
                drone_a.status = "colidiu"
                drone_b.status = "colidiu"

                evento = (
                    f"Passo {passo_atual}: "
                    f"Drone {drone_a.id} colidiu com Drone {drone_b.id}"
                )

                eventos.append(evento)
                print(f"[COLISÃO] {evento}")