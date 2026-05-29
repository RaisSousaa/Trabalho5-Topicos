import arcade

from config import CONFIG
from scenarios import obter_cenario
from visualization.arcade_visualizer import ArcadeVisualizer


drones = obter_cenario(
    CONFIG["cenario"],
    config=CONFIG,
    seed=CONFIG["experimentos"]["seed_base"]
)

janela = ArcadeVisualizer(drones, CONFIG)
arcade.run()