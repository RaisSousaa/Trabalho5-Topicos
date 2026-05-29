import arcade

from metrics.metrics import calcular_metricas
from simulation.collision import verificar_colisoes
from utils.exporter import salvar_metricas_csv, salvar_eventos_log


LARGURA_JANELA = 1200
ALTURA_JANELA = 800
LARGURA_PAINEL = 300

MARGEM = 50


def cor_por_status(status):
    if status == "em_movimento":
        return arcade.color.BLUE
    if status == "chegou":
        return arcade.color.GREEN
    if status == "colidiu":
        return arcade.color.RED
    return arcade.color.GRAY


class ArcadeVisualizer(arcade.Window):
    def __init__(self, drones, config):
        super().__init__(
            LARGURA_JANELA,
            ALTURA_JANELA,
            "Simulador de Drones 2D - Arcade"
        )

        self.drones = drones
        self.sim_config = config

        self.max_passos = config["max_passos"]
        self.raio_colisao = config["raio_colisao"]

        self.passo_atual = 0
        self.eventos = []
        self.metricas = None

        self.pausado = False
        self.finalizado = False

        self.largura_ambiente = config.get("largura_ambiente", 100)
        self.altura_ambiente = config.get("altura_ambiente", 100)

        self.area_simulacao_largura = LARGURA_JANELA - LARGURA_PAINEL - 2 * MARGEM
        self.area_simulacao_altura = ALTURA_JANELA - 2 * MARGEM

        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def converter_raio(self, raio):
        escala_x = self.area_simulacao_largura / self.largura_ambiente
        escala_y = self.area_simulacao_altura / self.altura_ambiente
        escala_media = (escala_x + escala_y) / 2
        return raio * escala_media

    def converter_x(self, x):
        return MARGEM + (x / self.largura_ambiente) * self.area_simulacao_largura

    def converter_y(self, y):
        return MARGEM + (y / self.altura_ambiente) * self.area_simulacao_altura

    def on_draw(self):
        self.clear()

        self.desenhar_area_simulacao()
        self.desenhar_drones()
        self.desenhar_painel()

    def on_update(self, delta_time):
        if self.pausado or self.finalizado:
            return

        if self.passo_atual >= self.max_passos:
            self.marcar_nao_concluidos()
            self.finalizar_simulacao()
            return

        self.passo_atual += 1

        for drone in self.drones:
            drone.mover()

            if drone.status == "chegou" and drone.tempo_chegada is None:
                drone.tempo_chegada = self.passo_atual

        verificar_colisoes(
            self.drones,
            self.raio_colisao,
            self.passo_atual,
            self.eventos
        )

        if self.todos_finalizaram():
            self.finalizar_simulacao()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.pausado = not self.pausado

        if key == arcade.key.ESCAPE:
            self.close()

    def desenhar_area_simulacao(self):
        esquerda = MARGEM
        direita = LARGURA_JANELA - LARGURA_PAINEL - MARGEM
        baixo = MARGEM
        topo = ALTURA_JANELA - MARGEM

        arcade.draw_lrbt_rectangle_outline(
            esquerda,
            direita,
            baixo,
            topo,
            arcade.color.WHITE,
            2
        )

        arcade.draw_text(
            "Ambiente 2D - Visão Superior",
            esquerda,
            topo + 10,
            arcade.color.WHITE,
            14
        )

    def desenhar_drones(self):
        for drone in self.drones:
            x = self.converter_x(drone.x)
            y = self.converter_y(drone.y)

            destino_x = self.converter_x(drone.destino_x)
            destino_y = self.converter_y(drone.destino_y)

            origem_x = self.converter_x(drone.x_inicial)
            origem_y = self.converter_y(drone.y_inicial)

            # Rota planejada
            arcade.draw_line(
                origem_x,
                origem_y,
                destino_x,
                destino_y,
                arcade.color.LIGHT_GRAY,
                1
            )

            # Trajetória percorrida
            if len(drone.trajetoria) > 1:
                for i in range(len(drone.trajetoria) - 1):
                    x1 = self.converter_x(drone.trajetoria[i][0])
                    y1 = self.converter_y(drone.trajetoria[i][1])
                    x2 = self.converter_x(drone.trajetoria[i + 1][0])
                    y2 = self.converter_y(drone.trajetoria[i + 1][1])

                    arcade.draw_line(
                        x1,
                        y1,
                        x2,
                        y2,
                        arcade.color.YELLOW,
                        1
                    )

            # Origem
            arcade.draw_circle_filled(
                origem_x,
                origem_y,
                4,
                arcade.color.WHITE
            )

            # Destino
            arcade.draw_line(
                destino_x - 6,
                destino_y - 6,
                destino_x + 6,
                destino_y + 6,
                arcade.color.BLACK,
                3
            )
            arcade.draw_line(
                destino_x - 6,
                destino_y + 6,
                destino_x + 6,
                destino_y - 6,
                arcade.color.BLACK,
                3
            )

            # Drone
            cor = cor_por_status(drone.status)

            arcade.draw_circle_filled(
                x,
                y,
                8,
                cor
            )

            arcade.draw_circle_outline(
                x,
                y,
                self.converter_raio(self.raio_colisao),
                arcade.color.WHITE,
                1
            )

            arcade.draw_text(
                f"D{drone.id}",
                x + 10,
                y + 8,
                arcade.color.WHITE,
                10
            )

            if drone.status == "colidiu":
                arcade.draw_circle_outline(
                    x,
                    y,
                    18,
                    arcade.color.RED,
                    3
                )

    def desenhar_painel(self):
        x_painel = LARGURA_JANELA - LARGURA_PAINEL + 20
        y = ALTURA_JANELA - 50

        metricas_atuais = calcular_metricas(self.drones, self.passo_atual)

        linhas = [
            "PAINEL DA SIMULAÇÃO",
            "",
            f"Cenário: {self.sim_config['cenario']}",
            f"Passo atual: {self.passo_atual}",
            f"Máximo de passos: {self.max_passos}",
            "",
            f"Total de drones: {metricas_atuais['total_drones']}",
            f"Chegaram: {metricas_atuais['chegaram']}",
            f"Colidiram: {metricas_atuais['colidiram']}",
            f"Não concluíram: {metricas_atuais['nao_concluiram']}",
            "",
            f"Taxa sucesso: {metricas_atuais['taxa_sucesso']:.2f}%",
            f"Taxa colisão: {metricas_atuais['taxa_colisao']:.2f}%",
            "",
            "LEGENDA",
            "Azul: em movimento",
            "Verde: chegou",
            "Vermelho: colidiu",
            "Cinza: não concluiu",
            "Linha cinza: rota planejada",
            "Linha amarela: trajetória",
            "",
            "CONTROLES",
            "Espaço: pausar/continuar",
            "ESC: sair",
        ]

        for linha in linhas:
            arcade.draw_text(
                linha,
                x_painel,
                y,
                arcade.color.WHITE,
                12
            )
            y -= 24

        if self.pausado:
            arcade.draw_text(
                "PAUSADO",
                x_painel,
                80,
                arcade.color.YELLOW,
                18,
                bold=True
            )

        if self.finalizado:
            arcade.draw_text(
                "SIMULAÇÃO FINALIZADA",
                x_painel,
                80,
                arcade.color.GREEN,
                16,
                bold=True
            )

    def todos_finalizaram(self):
        for drone in self.drones:
            if drone.status == "em_movimento":
                return False
        return True

    def marcar_nao_concluidos(self):
        for drone in self.drones:
            if drone.status == "em_movimento":
                drone.status = "nao_concluiu"

    def finalizar_simulacao(self):
        self.marcar_nao_concluidos()
        self.metricas = calcular_metricas(self.drones, self.passo_atual)
        self.finalizado = True

        salvar_metricas_csv(self.metricas, self.sim_config)
        salvar_eventos_log(self.eventos, self.sim_config)

        print("\n========== SIMULAÇÃO ARCADE FINALIZADA ==========")
        print(f"Total de drones: {self.metricas['total_drones']}")
        print(f"Chegaram: {self.metricas['chegaram']}")
        print(f"Colidiram: {self.metricas['colidiram']}")
        print(f"Não concluíram: {self.metricas['nao_concluiram']}")
        print(f"Taxa de sucesso: {self.metricas['taxa_sucesso']:.2f}%")
        print(f"Taxa de colisão: {self.metricas['taxa_colisao']:.2f}%")

        if self.eventos:
            print("\nEventos:")
            for evento in self.eventos:
                print(evento)