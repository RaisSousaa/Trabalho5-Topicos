import time
import copy
import dearpygui.dearpygui as dpg

from metrics.metrics import calcular_metricas
from simulation.collision import verificar_colisoes
from utils.exporter import salvar_metricas_csv, salvar_eventos_log
from scenarios import obter_cenario


LARGURA_JANELA = 1250
ALTURA_JANELA = 820

LARGURA_CONTROLES = 260
LARGURA_METRICAS = 280

MARGEM = 35

COR_FUNDO = (11, 17, 32, 255)
COR_PAINEL = (17, 24, 39, 255)
COR_BORDA = (80, 90, 110, 255)
COR_TEXTO = (226, 232, 240, 255)
COR_MUTED = (120, 130, 150, 255)

COR_AZUL = (59, 130, 246, 255)
COR_VERDE = (34, 197, 94, 255)
COR_VERMELHO = (239, 68, 68, 255)
COR_AMARELO = (245, 158, 11, 255)
COR_CINZA = (148, 163, 184, 255)
COR_BRANCO = (255, 255, 255, 255)


def cor_por_status(status):
    if status == "em_movimento":
        return COR_AZUL
    if status == "chegou":
        return COR_VERDE
    if status == "colidiu":
        return COR_VERMELHO
    return COR_CINZA


def formatar_nome_cenario(nome):
    nomes = {
        "sem_colisao": "Sem colisão",
        "colisao_central": "Colisão central",
        "alta_densidade": "Alta densidade fixa",
        "aleatorio_baixa_densidade": "Aleatório - baixa densidade",
        "aleatorio_media_densidade": "Aleatório - média densidade",
        "aleatorio_alta_densidade": "Aleatório - alta densidade",
    }

    return nomes.get(nome, nome)


class DearPyGuiVisualizer:
    def __init__(self, drones, config):
        self.drones_iniciais = copy.deepcopy(drones)
        self.drones = drones
        self.config = config

        self.cenarios_disponiveis = {
            "Sem colisão": "sem_colisao",
            "Colisão central": "colisao_central",
            "Alta densidade fixa": "alta_densidade",
            "Aleatório - baixa densidade": "aleatorio_baixa_densidade",
            "Aleatório - média densidade": "aleatorio_media_densidade",
            "Aleatório - alta densidade": "aleatorio_alta_densidade",
        }

        self.nome_cenario_atual = config["cenario"]

        self.passo_atual = 0
        self.max_passos = config["max_passos"]
        self.raio_colisao = config["raio_colisao"]

        self.eventos = []
        self.metricas = None

        self.rodando = False
        self.pausado = False
        self.finalizado = False

        self.ultimo_update = time.time()

        self.largura_ambiente = config.get("largura_ambiente", 100)
        self.altura_ambiente = config.get("altura_ambiente", 100)

        self.canvas_x = LARGURA_CONTROLES + 20
        self.canvas_y = 80
        self.canvas_largura = LARGURA_JANELA - LARGURA_CONTROLES - LARGURA_METRICAS - 60
        self.canvas_altura = ALTURA_JANELA - 150

    def converter_x(self, x):
        return self.canvas_x + MARGEM + (x / self.largura_ambiente) * (self.canvas_largura - 2 * MARGEM)

    def converter_y(self, y):
        return self.canvas_y + MARGEM + (y / self.altura_ambiente) * (self.canvas_altura - 2 * MARGEM)

    def converter_raio(self, raio):
        escala_x = (self.canvas_largura - 2 * MARGEM) / self.largura_ambiente
        escala_y = (self.canvas_altura - 2 * MARGEM) / self.altura_ambiente
        return raio * ((escala_x + escala_y) / 2)

    def executar(self):
        dpg.create_context()
        self.criar_tema()
        self.criar_interface()

        dpg.create_viewport(
            title="Simulador de Drones 2D - Dear PyGui",
            width=LARGURA_JANELA,
            height=ALTURA_JANELA,
            resizable=False
        )

        dpg.setup_dearpygui()
        dpg.show_viewport()

        while dpg.is_dearpygui_running():
            self.loop()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()

    def criar_tema(self):
        with dpg.theme() as tema_global:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, COR_FUNDO)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, COR_PAINEL)
                dpg.add_theme_color(dpg.mvThemeCol_Text, COR_TEXTO)
                dpg.add_theme_color(dpg.mvThemeCol_Button, (30, 41, 59, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (51, 65, 85, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (30, 41, 59, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (51, 65, 85, 255))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8)

        dpg.bind_theme(tema_global)

    def criar_interface(self):
        with dpg.window(
            label="Simulador",
            tag="janela_principal",
            width=LARGURA_JANELA,
            height=ALTURA_JANELA,
            no_resize=True,
            no_move=True,
            no_collapse=True,
            no_title_bar=True
        ):
            dpg.add_text("Simulador de Drones 2D", color=COR_TEXTO)
            dpg.add_text(
                "Ambiente bidimensional · Visão superior · Detecção de colisões · Métricas em tempo real",
                color=COR_MUTED
            )

            with dpg.group(horizontal=True):
                self.criar_painel_controles()
                self.criar_canvas()
                self.criar_painel_metricas()

        self.atualizar_metricas()
        self.desenhar()

    def criar_painel_controles(self):
        with dpg.child_window(width=LARGURA_CONTROLES, height=ALTURA_JANELA - 90, border=True):
            dpg.add_text("CONFIGURAÇÃO", color=COR_MUTED)
            dpg.add_spacer(height=5)

            dpg.add_text("Cenário:", color=COR_MUTED)

            cenario_padrao_formatado = formatar_nome_cenario(self.config["cenario"])

            dpg.add_combo(
                items=list(self.cenarios_disponiveis.keys()),
                default_value=cenario_padrao_formatado,
                tag="combo_cenario",
                width=-1,
                callback=self.trocar_cenario
            )

            dpg.add_text(
                f"Atual: {cenario_padrao_formatado}",
                tag="texto_cenario_atual",
                color=COR_TEXTO
            )

            dpg.add_spacer(height=12)

            dpg.add_slider_float(
                label="Velocidade visual",
                tag="velocidade_visual",
                default_value=1.0,
                min_value=0.2,
                max_value=5.0,
                format="%.1f"
            )

            dpg.add_checkbox(
                label="Mostrar rotas",
                tag="mostrar_rotas",
                default_value=True
            )

            dpg.add_checkbox(
                label="Mostrar trajetórias",
                tag="mostrar_trajetorias",
                default_value=True
            )

            dpg.add_checkbox(
                label="Mostrar raio de colisão",
                tag="mostrar_raio",
                default_value=True
            )

            dpg.add_checkbox(
                label="Mostrar rótulos",
                tag="mostrar_rotulos",
                default_value=True
            )

            dpg.add_spacer(height=20)
            dpg.add_text("CONTROLES", color=COR_MUTED)
            dpg.add_spacer(height=5)

            dpg.add_button(
                label="Iniciar",
                width=-1,
                callback=self.iniciar
            )

            dpg.add_button(
                label="Pausar / Continuar",
                width=-1,
                callback=self.pausar
            )

            dpg.add_button(
                label="Executar 1 passo",
                width=-1,
                callback=self.executar_um_passo
            )

            dpg.add_button(
                label="Reset visual",
                width=-1,
                callback=self.reset_visual
            )

            dpg.add_spacer(height=20)
            dpg.add_text("STATUS", color=COR_MUTED)

            dpg.add_text("Aguardando início", tag="status_simulacao", color=COR_AMARELO)

            dpg.add_spacer(height=20)
            dpg.add_text("LEGENDA", color=COR_MUTED)
            dpg.add_text("Azul: em movimento", color=COR_AZUL)
            dpg.add_text("Verde: chegou", color=COR_VERDE)
            dpg.add_text("Vermelho: colidiu", color=COR_VERMELHO)
            dpg.add_text("Cinza: não concluiu", color=COR_CINZA)

    def trocar_cenario(self, sender=None, app_data=None, user_data=None):
        nome_formatado = dpg.get_value("combo_cenario")
        nome_cenario = self.cenarios_disponiveis[nome_formatado]

        self.nome_cenario_atual = nome_cenario
        self.config["cenario"] = nome_cenario

        seed = self.config["experimentos"]["seed_base"]

        novos_drones = obter_cenario(
            nome_cenario,
            config=self.config,
            seed=seed
        )

        self.drones_iniciais = copy.deepcopy(novos_drones)
        self.drones = copy.deepcopy(novos_drones)

        self.passo_atual = 0
        self.eventos = []
        self.metricas = None

        self.rodando = False
        self.pausado = False
        self.finalizado = False
        self.ultimo_update = time.time()

        dpg.set_value(
            "texto_cenario_atual",
            f"Atual: {nome_formatado}"
        )

        dpg.set_value(
            "status_simulacao",
            "Cenário alterado. Clique em Iniciar."
        )

        dpg.set_value(
            "log_eventos",
            "Nenhum evento registrado."
        )

        self.atualizar_metricas()
        self.desenhar()


    def criar_canvas(self):
        with dpg.child_window(width=self.canvas_largura + 20, height=ALTURA_JANELA - 90, border=True):
            dpg.add_text("Ambiente 2D - Visão Superior", color=COR_TEXTO)
            dpg.add_text("Rotas, trajetórias e colisões são exibidas em tempo real.", color=COR_MUTED)

            with dpg.drawlist(
                width=self.canvas_largura,
                height=self.canvas_altura,
                tag="canvas_simulacao"
            ):
                pass

    def criar_painel_metricas(self):
        with dpg.child_window(width=LARGURA_METRICAS, height=ALTURA_JANELA - 90, border=True):
            dpg.add_text("MÉTRICAS", color=COR_MUTED)

            dpg.add_separator()

            dpg.add_text("Total de drones", color=COR_MUTED)
            dpg.add_text("0", tag="m_total", color=COR_TEXTO)

            dpg.add_spacer(height=8)
            dpg.add_text("Em movimento", color=COR_MUTED)
            dpg.add_text("0", tag="m_movimento", color=COR_AZUL)

            dpg.add_spacer(height=8)
            dpg.add_text("Chegaram", color=COR_MUTED)
            dpg.add_text("0", tag="m_chegaram", color=COR_VERDE)

            dpg.add_spacer(height=8)
            dpg.add_text("Colidiram", color=COR_MUTED)
            dpg.add_text("0", tag="m_colidiram", color=COR_VERMELHO)

            dpg.add_spacer(height=8)
            dpg.add_text("Não concluíram", color=COR_MUTED)
            dpg.add_text("0", tag="m_nao_concluiram", color=COR_AMARELO)

            dpg.add_separator()

            dpg.add_text("Taxa de sucesso", color=COR_MUTED)
            dpg.add_text("0.00%", tag="m_taxa_sucesso", color=COR_VERDE)

            dpg.add_spacer(height=8)
            dpg.add_text("Taxa de colisão", color=COR_MUTED)
            dpg.add_text("0.00%", tag="m_taxa_colisao", color=COR_VERMELHO)

            dpg.add_spacer(height=8)
            dpg.add_text("Tempo médio de chegada", color=COR_MUTED)
            dpg.add_text("0.00", tag="m_tempo_medio", color=COR_TEXTO)

            dpg.add_spacer(height=8)
            dpg.add_text("Distância média percorrida", color=COR_MUTED)
            dpg.add_text("0.00", tag="m_distancia_media", color=COR_TEXTO)

            dpg.add_spacer(height=8)
            dpg.add_text("Passo atual", color=COR_MUTED)
            dpg.add_text("0", tag="m_passo", color=COR_TEXTO)

            dpg.add_separator()
            dpg.add_text("LOG DE EVENTOS", color=COR_MUTED)

            with dpg.child_window(height=180, border=True):
                dpg.add_text("", tag="log_eventos", color=COR_TEXTO)

    def loop(self):
        if self.rodando and not self.pausado and not self.finalizado:
            velocidade_visual = dpg.get_value("velocidade_visual")
            intervalo = max(0.01, 0.15 / velocidade_visual)

            agora = time.time()
            if agora - self.ultimo_update >= intervalo:
                self.executar_passo()
                self.ultimo_update = agora

        self.desenhar()

    def iniciar(self, sender=None, app_data=None, user_data=None):
        if self.finalizado:
            self.resetar_simulacao()

        self.rodando = True
        self.pausado = False
        self.finalizado = False
        self.ultimo_update = time.time()

        dpg.set_value("status_simulacao", "Rodando")
        self.atualizar_metricas()
        self.atualizar_log()
        self.desenhar()


    def pausar(self, sender=None, app_data=None, user_data=None):
        if self.finalizado:
            dpg.set_value("status_simulacao", "Simulação finalizada")
            return

        if not self.rodando:
            dpg.set_value("status_simulacao", "Inicie a simulação antes de pausar")
            return

        self.pausado = not self.pausado

        if self.pausado:
            dpg.set_value("status_simulacao", "Pausado")
        else:
            dpg.set_value("status_simulacao", "Rodando")

        self.desenhar()


    def executar_um_passo(self, sender=None, app_data=None, user_data=None):
        if self.finalizado:
            dpg.set_value("status_simulacao", "Simulação finalizada")
            return

        # O passo manual funciona como modo passo a passo.
        # Então a simulação fica pausada depois do passo.
        self.rodando = True
        self.pausado = True

        self.executar_passo()
        self.atualizar_metricas()
        self.atualizar_log()
        self.desenhar()

        if not self.finalizado:
            dpg.set_value("status_simulacao", "Passo executado manualmente")


    def reset_visual(self, sender=None, app_data=None, user_data=None):
        self.resetar_simulacao()

    def resetar_simulacao(self):
        self.drones = copy.deepcopy(self.drones_iniciais)

        self.passo_atual = 0
        self.eventos = []
        self.metricas = None

        self.rodando = False
        self.pausado = False
        self.finalizado = False
        self.ultimo_update = time.time()

        dpg.set_value("status_simulacao", "Simulação reiniciada")
        dpg.set_value("log_eventos", "Nenhum evento registrado.")

        self.atualizar_metricas()
        self.desenhar()

    def executar_passo(self):
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

        self.atualizar_metricas()
        self.atualizar_log()

    def desenhar(self):
        dpg.delete_item("canvas_simulacao", children_only=True)

        # fundo do canvas
        dpg.draw_rectangle(
            (0, 0),
            (self.canvas_largura, self.canvas_altura),
            color=COR_BORDA,
            fill=COR_FUNDO,
            parent="canvas_simulacao"
        )

        self.desenhar_grade()
        self.desenhar_drones()

    def desenhar_grade(self):
        espacamento = 50

        for x in range(0, int(self.canvas_largura), espacamento):
            dpg.draw_line(
                (x, 0),
                (x, self.canvas_altura),
                color=(255, 255, 255, 25),
                thickness=1,
                parent="canvas_simulacao"
            )

        for y in range(0, int(self.canvas_altura), espacamento):
            dpg.draw_line(
                (0, y),
                (self.canvas_largura, y),
                color=(255, 255, 255, 25),
                thickness=1,
                parent="canvas_simulacao"
            )

    def desenhar_drones(self):
        mostrar_rotas = dpg.get_value("mostrar_rotas")
        mostrar_trajetorias = dpg.get_value("mostrar_trajetorias")
        mostrar_raio = dpg.get_value("mostrar_raio")
        mostrar_rotulos = dpg.get_value("mostrar_rotulos")

        for drone in self.drones:
            x = self.converter_x(drone.x) - self.canvas_x
            y = self.converter_y(drone.y) - self.canvas_y

            origem_x = self.converter_x(drone.x_inicial) - self.canvas_x
            origem_y = self.converter_y(drone.y_inicial) - self.canvas_y

            destino_x = self.converter_x(drone.destino_x) - self.canvas_x
            destino_y = self.converter_y(drone.destino_y) - self.canvas_y

            if mostrar_rotas:
                dpg.draw_line(
                    (origem_x, origem_y),
                    (destino_x, destino_y),
                    color=(180, 180, 180, 90),
                    thickness=1,
                    parent="canvas_simulacao"
                )

            if mostrar_trajetorias and len(drone.trajetoria) > 1:
                for i in range(len(drone.trajetoria) - 1):
                    x1 = self.converter_x(drone.trajetoria[i][0]) - self.canvas_x
                    y1 = self.converter_y(drone.trajetoria[i][1]) - self.canvas_y
                    x2 = self.converter_x(drone.trajetoria[i + 1][0]) - self.canvas_x
                    y2 = self.converter_y(drone.trajetoria[i + 1][1]) - self.canvas_y

                    dpg.draw_line(
                        (x1, y1),
                        (x2, y2),
                        color=(245, 158, 11, 140),
                        thickness=1,
                        parent="canvas_simulacao"
                    )

            # origem
            dpg.draw_circle(
                (origem_x, origem_y),
                4,
                color=COR_BRANCO,
                fill=COR_BRANCO,
                parent="canvas_simulacao"
            )

            # destino em X
            dpg.draw_line(
                (destino_x - 7, destino_y - 7),
                (destino_x + 7, destino_y + 7),
                color=COR_CINZA,
                thickness=2,
                parent="canvas_simulacao"
            )
            dpg.draw_line(
                (destino_x - 7, destino_y + 7),
                (destino_x + 7, destino_y - 7),
                color=COR_CINZA,
                thickness=2,
                parent="canvas_simulacao"
            )

            if mostrar_raio and drone.status == "em_movimento":
                dpg.draw_circle(
                    (x, y),
                    self.converter_raio(self.raio_colisao),
                    color=(59, 130, 246, 80),
                    fill=(59, 130, 246, 25),
                    parent="canvas_simulacao"
                )

            cor = cor_por_status(drone.status)

            dpg.draw_circle(
                (x, y),
                8,
                color=COR_BRANCO,
                fill=cor,
                thickness=2,
                parent="canvas_simulacao"
            )

            if drone.status == "colidiu":
                dpg.draw_circle(
                    (x, y),
                    18,
                    color=COR_VERMELHO,
                    thickness=3,
                    parent="canvas_simulacao"
                )

            if mostrar_rotulos:
                dpg.draw_text(
                    (x + 10, y - 18),
                    f"D{drone.id}",
                    color=COR_TEXTO,
                    size=11,
                    parent="canvas_simulacao"
                )

    def atualizar_metricas(self):
        metricas = calcular_metricas(self.drones, self.passo_atual)

        em_movimento = len([d for d in self.drones if d.status == "em_movimento"])

        dpg.set_value("m_total", str(metricas["total_drones"]))
        dpg.set_value("m_movimento", str(em_movimento))
        dpg.set_value("m_chegaram", str(metricas["chegaram"]))
        dpg.set_value("m_colidiram", str(metricas["colidiram"]))
        dpg.set_value("m_nao_concluiram", str(metricas["nao_concluiram"]))
        dpg.set_value("m_taxa_sucesso", f"{metricas['taxa_sucesso']:.2f}%")
        dpg.set_value("m_taxa_colisao", f"{metricas['taxa_colisao']:.2f}%")
        dpg.set_value("m_tempo_medio", f"{metricas['tempo_medio_chegada']:.2f}")
        dpg.set_value("m_distancia_media", f"{metricas['distancia_media_percorrida']:.2f}")
        dpg.set_value("m_passo", str(self.passo_atual))

    def atualizar_log(self):
        ultimos_eventos = self.eventos[-8:]

        if not ultimos_eventos:
            dpg.set_value("log_eventos", "Nenhum evento registrado.")
            return

        texto = "\n".join(ultimos_eventos)
        dpg.set_value("log_eventos", texto)

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

        salvar_metricas_csv(self.metricas, self.config)
        salvar_eventos_log(self.eventos, self.config)

        self.rodando = False
        self.pausado = False
        self.finalizado = True

        dpg.set_value("status_simulacao", "Simulação finalizada")

        self.atualizar_metricas()
        self.atualizar_log()

        print("\n========== SIMULAÇÃO FINALIZADA ==========")
        print(f"Total de drones: {self.metricas['total_drones']}")
        print(f"Chegaram: {self.metricas['chegaram']}")
        print(f"Colidiram: {self.metricas['colidiram']}")
        print(f"Não concluíram: {self.metricas['nao_concluiram']}")
        print(f"Taxa de sucesso: {self.metricas['taxa_sucesso']:.2f}%")
        print(f"Taxa de colisão: {self.metricas['taxa_colisao']:.2f}%")