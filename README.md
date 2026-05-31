# Simulador de Drones 2D — Dear PyGui

Este projeto implementa um simulador de drones em ambiente 2D com interface gráfica em **Dear PyGui**. A simulação permite visualizar drones em movimento, detectar colisões, registrar eventos e acompanhar métricas em tempo real.

## Funcionalidades

- Escolha de cenário pela interface;
- Visualização dos drones em ambiente 2D;
- Exibição de rotas, trajetórias e raio de colisão;
- Controles para iniciar, pausar, executar passo a passo e resetar;
- Detecção de colisões;
- Métricas em tempo real;
- Log de eventos;
- Exportação de métricas e eventos ao final da simulação.

## Tecnologias

- Python 3;
- Dear PyGui.

## Estrutura do Projeto

```text
simulador-drones/
├── dearpygui_main.py
├── config.py
├── scenarios.py
├── requirements.txt
├── README.md
├── models/
│   └── drone.py
├── simulation/
│   └── collision.py
├── metrics/
│   └── metrics.py
├── utils/
│   └── exporter.py
├── visualization/
│   └── dearpygui_visualizer.py
└── results/
```

## Instalação

Crie o ambiente virtual:

```bash
python3 -m venv venv
```

Ative o ambiente virtual:

```bash
source venv/bin/activate
```

No Windows, use:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
python3 -m pip install -r requirements.txt
```

Caso não utilize `requirements.txt`, instale manualmente:

```bash
python3 -m pip install dearpygui
```

## Arquivo requirements.txt

O arquivo `requirements.txt` deve conter:

```txt
dearpygui
pandas
matplotlib
```

## Como Executar

Execute o simulador com:

```bash
python3 dearpygui_main.py
```

Após executar o comando, será aberta a interface gráfica do simulador.

## Como Usar

Na interface Dear PyGui:

1. Escolha o cenário no painel esquerdo;
2. Clique em **Iniciar**;
3. Observe os drones se movimentando no ambiente 2D;
4. Acompanhe as métricas no painel direito;
5. Use **Pausar / Continuar** para controlar a execução;
6. Use **Executar 1 passo** para analisar a simulação passo a passo;
7. Use **Reset visualização** para reiniciar o cenário atual.

## Cenários Disponíveis

A interface permite executar os seguintes cenários:

```text
Sem colisão
Colisão central
Alta densidade fixa
Aleatório - baixa densidade
Aleatório - média densidade
Aleatório - alta densidade
```

No código, esses cenários são definidos no arquivo `scenarios.py`.

## Configuração

Os principais parâmetros da simulação ficam no arquivo `config.py`.

Exemplos de parâmetros configuráveis:

```text
cenário inicial
número máximo de passos
raio de colisão
largura do ambiente
altura do ambiente
intervalo da animação
```

O cenário definido em `config.py` funciona como cenário inicial. Depois que a interface é aberta, o usuário pode escolher outro cenário diretamente pela tela.

## Estados dos Drones

Cada drone pode assumir um dos seguintes estados:

```text
em_movimento
chegou
colidiu
nao_concluiu
```

## Funcionamento do Movimento

Cada drone possui uma posição inicial, um destino e uma velocidade.

A cada passo da simulação, o drone calcula a direção até o destino e se desloca nessa direção. Quando chega ao destino, seu estado muda para `chegou`.

## Critério de Colisão

A colisão ocorre quando a distância entre dois drones é menor ou igual ao raio de colisão definido na configuração.

Quando uma colisão é detectada:

```text
- os drones envolvidos mudam para o estado "colidiu";
- os drones envolvidos deixam de se mover;
- o evento é registrado no log;
- as métricas são atualizadas.
```

## Métricas Calculadas

O simulador calcula:

```text
Total de drones
Drones em movimento
Drones que chegaram ao destino
Drones que colidiram
Drones que não concluíram a missão
Taxa de sucesso
Taxa de colisão
Tempo médio de chegada
Distância média percorrida
Passo atual
```

## Arquivos Gerados

Ao final da simulação, os resultados são salvos na pasta `results/`.

Exemplos:

```text
results/metricas_<cenario>.csv
results/eventos_<cenario>.log
```

O arquivo `.csv` contém as métricas da simulação.

O arquivo `.log` contém os eventos registrados, como colisões.

## Funcionamento Geral

A simulação ocorre em passos discretos.

A cada passo:

1. Os drones em movimento avançam em direção aos seus destinos;
2. O sistema verifica se algum drone chegou ao destino;
3. O sistema verifica colisões entre drones;
4. Os eventos são registrados;
5. As métricas são atualizadas;
6. A interface gráfica é redesenhada.

## Organização do Código

O projeto foi organizado de forma modular:

```text
config.py
→ define os parâmetros gerais da simulação

scenarios.py
→ cria os cenários com posições iniciais e destinos dos drones

models/drone.py
→ define o comportamento individual de cada drone

simulation/collision.py
→ verifica colisões entre drones

metrics/metrics.py
→ calcula as métricas da simulação

utils/exporter.py
→ salva métricas e eventos na pasta results/

visualization/dearpygui_visualizer.py
→ constrói a interface gráfica e atualiza a visualização

dearpygui_main.py
→ inicia a execução principal do simulador
```

## Decisões de Projeto

O projeto foi organizado separando a lógica da simulação da interface gráfica.

Essa separação permite modificar a visualização sem alterar diretamente o comportamento dos drones, a detecção de colisões ou o cálculo das métricas.

A interface Dear PyGui foi escolhida por permitir uma visualização interativa, com controles para iniciar, pausar, executar passo a passo, resetar e trocar cenários.

## Limitações

Algumas simplificações foram adotadas:

```text
- ambiente bidimensional;
- todos os drones na mesma altitude;
- movimento por passos discretos;
- ausência de obstáculos externos;
- ausência de controle físico realista de aceleração;
- ausência de planejamento automático de rotas.
```

Essas simplificações foram adotadas para manter o foco na movimentação dos drones, na detecção de colisões e na análise das métricas geradas pela simulação.

## Comando Principal

```bash
python3 dearpygui_main.py
```
