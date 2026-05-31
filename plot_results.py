import os
import pandas as pd
import matplotlib.pyplot as plt

#gera os graficos.


def carregar_resultados(caminho_csv):
    if not os.path.exists(caminho_csv):
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho_csv}. "
            "Execute primeiro: python experiment.py"
        )

    return pd.read_csv(caminho_csv)


def criar_pasta_graficos():
    caminho = "results/graficos"
    os.makedirs(caminho, exist_ok=True)
    return caminho


def formatar_nome_cenario(nome):
    nomes = {
        "sem_colisao": "Sem colisão",
        "colisao_central": "Colisão central",
        "alta_densidade": "Alta densidade fixa",
        "aleatorio_baixa_densidade": "Aleatório baixa",
        "aleatorio_media_densidade": "Aleatório média",
        "aleatorio_alta_densidade": "Aleatório alta",
    }

    return nomes.get(nome, nome)


def preparar_dataframe(df):
    df["cenario_formatado"] = df["cenario"].apply(formatar_nome_cenario)

    colunas_numericas = [
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

    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    return df


def grafico_barras_com_desvio(
    df,
    coluna_media,
    coluna_desvio,
    titulo,
    eixo_y,
    nome_arquivo
):
    pasta_graficos = criar_pasta_graficos()

    plt.figure(figsize=(12, 6))

    plt.bar(
        df["cenario_formatado"],
        df[coluna_media],
        yerr=df[coluna_desvio],
        capsize=5
    )

    plt.title(titulo)
    plt.xlabel("Cenário")
    plt.ylabel(eixo_y)
    plt.xticks(rotation=30, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    caminho_saida = os.path.join(pasta_graficos, nome_arquivo)
    plt.savefig(caminho_saida, dpi=300)
    plt.show()

    print(f"Gráfico salvo em: {caminho_saida}")


def gerar_graficos():
    caminho_csv = "results/resumo_experimentos.csv"

    df = carregar_resultados(caminho_csv)
    df = preparar_dataframe(df)

    grafico_barras_com_desvio(
        df=df,
        coluna_media="media_taxa_sucesso",
        coluna_desvio="desvio_taxa_sucesso",
        titulo="Taxa média de sucesso por cenário",
        eixo_y="Taxa de sucesso (%)",
        nome_arquivo="taxa_sucesso_por_cenario.png"
    )

    grafico_barras_com_desvio(
        df=df,
        coluna_media="media_taxa_colisao",
        coluna_desvio="desvio_taxa_colisao",
        titulo="Taxa média de colisão por cenário",
        eixo_y="Taxa de colisão (%)",
        nome_arquivo="taxa_colisao_por_cenario.png"
    )

    grafico_barras_com_desvio(
        df=df,
        coluna_media="media_chegaram",
        coluna_desvio="desvio_chegaram",
        titulo="Média de drones que chegaram ao destino por cenário",
        eixo_y="Quantidade média de drones",
        nome_arquivo="drones_chegaram_por_cenario.png"
    )

    grafico_barras_com_desvio(
        df=df,
        coluna_media="media_colidiram",
        coluna_desvio="desvio_colidiram",
        titulo="Média de drones que colidiram por cenário",
        eixo_y="Quantidade média de drones",
        nome_arquivo="drones_colidiram_por_cenario.png"
    )

    grafico_barras_com_desvio(
        df=df,
        coluna_media="media_nao_concluiram",
        coluna_desvio="desvio_nao_concluiram",
        titulo="Média de drones que não concluíram por cenário",
        eixo_y="Quantidade média de drones",
        nome_arquivo="drones_nao_concluiram_por_cenario.png"
    )

    grafico_barras_com_desvio(
        df=df,
        coluna_media="media_tempo_total",
        coluna_desvio="desvio_tempo_total",
        titulo="Tempo médio total da simulação por cenário",
        eixo_y="Passos",
        nome_arquivo="tempo_total_por_cenario.png"
    )

    grafico_barras_com_desvio(
        df=df,
        coluna_media="media_distancia_percorrida",
        coluna_desvio="desvio_distancia_percorrida",
        titulo="Distância média percorrida por cenário",
        eixo_y="Distância média",
        nome_arquivo="distancia_media_por_cenario.png"
    )

    print("\nTodos os gráficos foram gerados com sucesso.")


if __name__ == "__main__":
    gerar_graficos()