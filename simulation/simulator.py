from simulation.collision import verificar_colisoes
from metrics.metrics import calcular_metricas, mostrar_metricas
from visualization.visualizer import visualizar
from utils.exporter import salvar_metricas_csv, salvar_eventos_log


class Simulador:
    def __init__(self, drones, config):
        self.drones = drones
        self.config = config
        self.max_passos = config["max_passos"]
        self.raio_colisao = config["raio_colisao"]
        self.passo_atual = 0
        self.eventos = []
        self.historico = []
        self.metricas = None

    def executar(self, exibir_visualizacao=True, exportar_resultados=True, exibir_terminal=True):
        for passo in range(self.max_passos):
            self.passo_atual = passo + 1

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

            self.salvar_estado_atual()

            if self.todos_finalizaram():
                break

        self.marcar_nao_concluidos()

        self.metricas = calcular_metricas(self.drones, self.passo_atual)

        if exibir_terminal:
            mostrar_metricas(self.metricas)

            if self.eventos:
                print("\n========== EVENTOS ==========")
                for evento in self.eventos:
                    print(evento)

        if exportar_resultados:
            salvar_metricas_csv(self.metricas, self.config)
            salvar_eventos_log(self.eventos, self.config)

        if exibir_visualizacao:
            visualizar(self.historico, self.config, self.metricas)

        return self.metricas

    def salvar_estado_atual(self):
        estado_atual = []

        for drone in self.drones:
            estado_atual.append({
                "id": drone.id,

                "x_inicial": drone.x_inicial,
                "y_inicial": drone.y_inicial,

                "x": drone.x,
                "y": drone.y,

                "destino_x": drone.destino_x,
                "destino_y": drone.destino_y,

                "status": drone.status,
                "trajetoria": list(drone.trajetoria)
            })

        self.historico.append(estado_atual)

    def todos_finalizaram(self):
        for drone in self.drones:
            if drone.status == "em_movimento":
                return False
        return True

    def marcar_nao_concluidos(self):
        for drone in self.drones:
            if drone.status == "em_movimento":
                drone.status = "nao_concluiu"