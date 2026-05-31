def calcular_metricas(drones, total_passos):
    total = len(drones)

    chegaram = sum(1 for drone in drones if drone.status == "chegou")
    colidiram = sum(1 for drone in drones if drone.status == "colidiu")
    nao_concluiram = sum(1 for drone in drones if drone.status == "nao_concluiu")

    taxa_sucesso = (chegaram / total) * 100 if total > 0 else 0
    taxa_colisao = (colidiram / total) * 100 if total > 0 else 0

    tempos_chegada = [
        drone.tempo_chegada
        for drone in drones
        if drone.tempo_chegada is not None
    ]

    tempo_medio_chegada = (
        sum(tempos_chegada) / len(tempos_chegada)
        if tempos_chegada
        else 0
    )

    distancia_media = (
        sum(drone.distancia_percorrida for drone in drones) / total
        if total > 0
        else 0
    )

    return {
        "total_drones": total,
        "chegaram": chegaram,
        "colidiram": colidiram,
        "nao_concluiram": nao_concluiram,
        "taxa_sucesso": taxa_sucesso,
        "taxa_colisao": taxa_colisao,
        "tempo_total_simulacao": total_passos,
        "tempo_medio_chegada": tempo_medio_chegada,
        "distancia_media_percorrida": distancia_media
    }


def mostrar_metricas(metricas):
    print("\n========== METRICAS FINAIS ==========")
    print(f"Total de drones: {metricas['total_drones']}")
    print(f"Drones que chegaram ao destino: {metricas['chegaram']}")
    print(f"Drones que colidiram: {metricas['colidiram']}")
    print(f"Drones que não concluíram a missão: {metricas['nao_concluiram']}")
    print(f"Taxa de sucesso: {metricas['taxa_sucesso']:.2f}%")
    print(f"Taxa de colisão: {metricas['taxa_colisao']:.2f}%")
    print(f"Tempo total da simulação: {metricas['tempo_total_simulacao']} passos")
    print(f"Tempo médio de chegada: {metricas['tempo_medio_chegada']:.2f} passos")
    print(f"Distância média percorrida: {metricas['distancia_media_percorrida']:.2f}")