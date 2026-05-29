import matplotlib.pyplot as plt
import matplotlib.animation as animation


def obter_cor_por_status(status):
    if status == "em_movimento":
        return "blue"
    elif status == "chegou":
        return "green"
    elif status == "colidiu":
        return "red"
    else:
        return "gray"


def visualizar(historico, config, metricas):
    fig, ax = plt.subplots(figsize=(10, 7))

    limite_x = config["limite_x"]
    limite_y = config["limite_y"]

    def atualizar(frame):
        ax.clear()

        ax.set_xlim(limite_x[0], limite_x[1])
        ax.set_ylim(limite_y[0], limite_y[1])
        ax.set_title(f"Simulador de Drones 2D - Passo {frame + 1}")
        ax.set_xlabel("Eixo X")
        ax.set_ylabel("Eixo Y")
        ax.grid(True)

        estado = historico[frame]

        for drone in estado:
            cor = obter_cor_por_status(drone["status"])

            # Rota planejada: linha da origem até o destino
            ax.plot(
                [drone["x_inicial"], drone["destino_x"]],
                [drone["y_inicial"], drone["destino_y"]],
                linestyle="--",
                linewidth=1,
                alpha=0.4
            )

            # Trajetória percorrida
            trajetoria = drone["trajetoria"]
            if len(trajetoria) > 1:
                xs = [p[0] for p in trajetoria]
                ys = [p[1] for p in trajetoria]
                ax.plot(xs, ys, linewidth=2, alpha=0.8)

            # Posição atual do drone
            ax.scatter(drone["x"], drone["y"], color=cor, s=120)
            ax.text(
                drone["x"] + 0.2,
                drone["y"] + 0.2,
                f'D{drone["id"]}',
                fontsize=9
            )

            # Destino
            ax.scatter(
                drone["destino_x"],
                drone["destino_y"],
                color="black",
                marker="x",
                s=120
            )

            # Origem
            ax.scatter(
                drone["x_inicial"],
                drone["y_inicial"],
                color="black",
                marker="o",
                s=30,
                alpha=0.5
            )

        texto_metricas = (
            f"Cenário: {config['cenario']}\n"
            f"Total de drones: {metricas['total_drones']}\n"
            f"Chegaram: {metricas['chegaram']}\n"
            f"Colidiram: {metricas['colidiram']}\n"
            f"Não concluíram: {metricas['nao_concluiram']}\n"
            f"Taxa de sucesso: {metricas['taxa_sucesso']:.2f}%\n"
            f"Taxa de colisão: {metricas['taxa_colisao']:.2f}%"
        )

        ax.text(
            1.03,
            0.95,
            texto_metricas,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            bbox=dict(boxstyle="round", alpha=0.2)
        )

        legenda = (
            "Legenda:\n"
            "Azul: em movimento\n"
            "Verde: chegou\n"
            "Vermelho: colidiu\n"
            "Cinza: não concluiu\n"
            "X preto: destino\n"
            "Linha tracejada: rota planejada\n"
            "Linha contínua: trajetória"
        )

        ax.text(
            1.03,
            0.45,
            legenda,
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment="top",
            bbox=dict(boxstyle="round", alpha=0.2)
        )

    animacao = animation.FuncAnimation(
        fig,
        atualizar,
        frames=len(historico),
        interval=config["intervalo_animacao"],
        repeat=False
    )

    plt.tight_layout()
    plt.show()