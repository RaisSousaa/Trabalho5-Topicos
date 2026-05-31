import csv
import os
import statistics

from config import CONFIG
from scenarios import obter_cenario
from simulation.simulator import Simulador

#gera resultados para análise.

def calcular_media(valores):
    if not valores:
        return 0
    return statistics.mean(valores)


def calcular_desvio_padrao(valores):
    if len(valores) <= 1:
        return 0
    return statistics.stdev(valores)


def executar_experimentos():
    os.makedirs("results", exist_ok=True)

    cenarios = CONFIG["experimentos"]["cenarios"]
    repeticoes = CONFIG["experimentos"]["repeticoes"]
    seed_base = CONFIG["experimentos"]["seed_base"]

    resultados_resumidos = []

    print("========== INICIO DOS EXPERIMENTOS ==========")
    print(f"Cenários: {cenarios}")
    print(f"Repetições por cenário: {repeticoes}")
    print(f"Seed base: {seed_base}")

    for nome_cenario in cenarios:
        print(f"\nExecutando cenário: {nome_cenario}")

        metricas_repeticoes = []

        for repeticao in range(1, repeticoes + 1):
            seed_execucao = seed_base + repeticao

            config_execucao = CONFIG.copy()
            config_execucao["cenario"] = nome_cenario
            config_execucao["seed"] = seed_execucao

            drones = obter_cenario(
                nome_cenario,
                config=config_execucao,
                seed=seed_execucao
            )

            simulador = Simulador(drones=drones, config=config_execucao)

            metricas = simulador.executar(
                exibir_visualizacao=False,
                exportar_resultados=False,
                exibir_terminal=False
            )

            metricas["cenario"] = nome_cenario
            metricas["repeticao"] = repeticao
            metricas["seed"] = seed_execucao

            metricas_repeticoes.append(metricas)

            print(
                f"  Repetição {repeticao}/{repeticoes} concluída "
                f"(seed={seed_execucao})"
            )

        salvar_resultados_detalhados(nome_cenario, metricas_repeticoes)

        resumo = gerar_resumo_cenario(nome_cenario, metricas_repeticoes)
        resultados_resumidos.append(resumo)

    salvar_resumo_experimentos(resultados_resumidos)

    print("\n========== EXPERIMENTOS FINALIZADOS ==========")
    print("Resumo salvo em: results/resumo_experimentos.csv")
    print("Resultados detalhados salvos em: results/resultados_detalhados.csv")


def gerar_resumo_cenario(nome_cenario, metricas_repeticoes):
    taxas_sucesso = [m["taxa_sucesso"] for m in metricas_repeticoes]
    taxas_colisao = [m["taxa_colisao"] for m in metricas_repeticoes]
    tempos_totais = [m["tempo_total_simulacao"] for m in metricas_repeticoes]
    tempos_medios_chegada = [m["tempo_medio_chegada"] for m in metricas_repeticoes]
    distancias_medias = [m["distancia_media_percorrida"] for m in metricas_repeticoes]
    chegaram = [m["chegaram"] for m in metricas_repeticoes]
    colidiram = [m["colidiram"] for m in metricas_repeticoes]
    nao_concluiram = [m["nao_concluiram"] for m in metricas_repeticoes]

    total_drones = metricas_repeticoes[0]["total_drones"]

    resumo = {
        "cenario": nome_cenario,
        "repeticoes": len(metricas_repeticoes),
        "total_drones": total_drones,

        "media_chegaram": calcular_media(chegaram),
        "desvio_chegaram": calcular_desvio_padrao(chegaram),

        "media_colidiram": calcular_media(colidiram),
        "desvio_colidiram": calcular_desvio_padrao(colidiram),

        "media_nao_concluiram": calcular_media(nao_concluiram),
        "desvio_nao_concluiram": calcular_desvio_padrao(nao_concluiram),

        "media_taxa_sucesso": calcular_media(taxas_sucesso),
        "desvio_taxa_sucesso": calcular_desvio_padrao(taxas_sucesso),

        "media_taxa_colisao": calcular_media(taxas_colisao),
        "desvio_taxa_colisao": calcular_desvio_padrao(taxas_colisao),

        "media_tempo_total": calcular_media(tempos_totais),
        "desvio_tempo_total": calcular_desvio_padrao(tempos_totais),

        "media_tempo_chegada": calcular_media(tempos_medios_chegada),
        "desvio_tempo_chegada": calcular_desvio_padrao(tempos_medios_chegada),

        "media_distancia_percorrida": calcular_media(distancias_medias),
        "desvio_distancia_percorrida": calcular_desvio_padrao(distancias_medias),
    }

    return resumo


def salvar_resultados_detalhados(nome_cenario, metricas_repeticoes):
    caminho_arquivo = "results/resultados_detalhados.csv"

    arquivo_existe = os.path.exists(caminho_arquivo)

    campos = [
        "cenario",
        "repeticao",
        "seed",
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

    with open(caminho_arquivo, mode="a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)

        if not arquivo_existe:
            escritor.writeheader()

        for metricas in metricas_repeticoes:
            escritor.writerow({
                "cenario": nome_cenario,
                "repeticao": metricas["repeticao"],
                "seed": metricas["seed"],
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


def salvar_resumo_experimentos(resultados):
    caminho_arquivo = "results/resumo_experimentos.csv"

    campos = [
        "cenario",
        "repeticoes",
        "total_drones",

        "media_chegaram",
        "desvio_chegaram",

        "media_colidiram",
        "desvio_colidiram",

        "media_nao_concluiram",
        "desvio_nao_concluiram",

        "media_taxa_sucesso",
        "desvio_taxa_sucesso",

        "media_taxa_colisao",
        "desvio_taxa_colisao",

        "media_tempo_total",
        "desvio_tempo_total",

        "media_tempo_chegada",
        "desvio_tempo_chegada",

        "media_distancia_percorrida",
        "desvio_distancia_percorrida",
    ]

    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()

        for resultado in resultados:
            linha_formatada = {}

            for campo in campos:
                valor = resultado[campo]

                if isinstance(valor, float):
                    linha_formatada[campo] = f"{valor:.2f}"
                else:
                    linha_formatada[campo] = valor

            escritor.writerow(linha_formatada)


if __name__ == "__main__":
    executar_experimentos()