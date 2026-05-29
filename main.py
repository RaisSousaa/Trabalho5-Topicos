from config import CONFIG
from scenarios import obter_cenario
from simulation.simulator import Simulador


drones = obter_cenario(
    CONFIG["cenario"],
    config=CONFIG,
    seed=CONFIG["experimentos"]["seed_base"]
)

simulador = Simulador(drones=drones, config=CONFIG)
simulador.executar(
    exibir_visualizacao=True,
    exportar_resultados=True,
    exibir_terminal=True
)