import csv
import os


def salvar_metricas_csv(metricas, config):
    os.makedirs("results", exist_ok=True)

    nome_cenario = config["cenario"]
    caminho_arquivo = f"results/metricas_{nome_cenario}.csv"

    arquivo_existe = os.path.exists(caminho_arquivo)

    with open(caminho_arquivo, mode="a", newline="", encoding="utf-8") as arquivo:
        campos = [
            "cenario",
            "total_drones",
            "chegaram",
            "colidiram",
            "nao_concluiram",
            "taxa_sucesso",
            "taxa_colisao",
            "tempo_total_simulacao",
            "tempo_medio_chegada",
            "distancia_media_percorrida"
        ]

        escritor = csv.DictWriter(arquivo, fieldnames=campos)

        if not arquivo_existe:
            escritor.writeheader()

        escritor.writerow({
            "cenario": nome_cenario,
            "total_drones": metricas["total_drones"],
            "chegaram": metricas["chegaram"],
            "colidiram": metricas["colidiram"],
            "nao_concluiram": metricas["nao_concluiram"],
            "taxa_sucesso": f"{metricas['taxa_sucesso']:.2f}",
            "taxa_colisao": f"{metricas['taxa_colisao']:.2f}",
            "tempo_total_simulacao": metricas["tempo_total_simulacao"],
            "tempo_medio_chegada": f"{metricas['tempo_medio_chegada']:.2f}",
            "distancia_media_percorrida": f"{metricas['distancia_media_percorrida']:.2f}"
        })


def salvar_eventos_log(eventos, config):
    os.makedirs("results", exist_ok=True)

    nome_cenario = config["cenario"]
    caminho_arquivo = f"results/eventos_{nome_cenario}.log"

    with open(caminho_arquivo, mode="w", encoding="utf-8") as arquivo:
        arquivo.write(f"Eventos da simulação - Cenário: {nome_cenario}\n")
        arquivo.write("=" * 50 + "\n\n")

        if not eventos:
            arquivo.write("Nenhum evento de colisão registrado.\n")
        else:
            for evento in eventos:
                arquivo.write(evento + "\n")