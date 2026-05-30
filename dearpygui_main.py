from config import CONFIG
from scenarios import obter_cenario
from visualization.dearpygui_visualizer import DearPyGuiVisualizer


drones = obter_cenario(
    CONFIG["cenario"],
    config=CONFIG,
    seed=CONFIG["experimentos"]["seed_base"]
)

visualizador = DearPyGuiVisualizer(drones, CONFIG)
visualizador.executar()