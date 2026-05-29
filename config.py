CONFIG = {
    #"cenario": "aleatorio_medio",
    #"cenario": "aleatorio_media_densidade",
    #"cenario": "aleatorio_media_densidade",
    "cenario": "sem_colisao",
    #"cenario": "aleatorio_baixa_densidade",
    


    "max_passos": 100,
    "raio_colisao": 1.0,

    "limite_x": (-1, 101),
    "limite_y": (-1, 101),

    "largura_ambiente": 100,
    "altura_ambiente": 100,

    "intervalo_animacao": 200,

    "experimentos": {
        "cenarios": [
            "sem_colisao",
            "colisao_central",
            "alta_densidade",
            "aleatorio_baixa_densidade",
            "aleatorio_media_densidade",
            "aleatorio_alta_densidade"
        ],
        "repeticoes": 30,
        "seed_base": 42
    }
}