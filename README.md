# Simulador de Drones 2D

## Descrição

Este projeto consiste em um simulador computacional de drones em um ambiente bidimensional. O simulador representa um conjunto de drones que se deslocam de posições iniciais até destinos definidos, considerando que todos voam na mesma altura.

Durante a execução, o sistema movimenta os drones passo a passo, verifica possíveis colisões entre eles, registra eventos importantes e apresenta métricas ao final da simulação.

A visualização permite observar os drones como pontos em movimento em uma visão superior do ambiente.

---

## Objetivo do Projeto

O objetivo do projeto é desenvolver um simulador capaz de:

- Representar drones em movimento;
- Simular o deslocamento dos drones até destinos definidos;
- Detectar colisões entre drones;
- Registrar eventos relevantes durante a execução;
- Gerar métricas finais da simulação;
- Apresentar visualmente a movimentação dos drones em um ambiente 2D.

---

## Tecnologias Utilizadas

O projeto foi desenvolvido em Python, utilizando a biblioteca Matplotlib para a visualização gráfica da simulação.

Principais tecnologias:

- Python 3
- Matplotlib

---

## Estrutura do Projeto

```text
simulador-drones/
│
├── main.py
├── config.py
│
├── models/
│   └── drone.py
│
├── simulation/
│   ├── simulator.py
│   └── collision.py
│
├── metrics/
│   └── metrics.py
│
└── visualization/
    └── visualizer.py
```

---

## Descrição dos Arquivos

### `main.py`

Arquivo principal do projeto.

Responsável por:

- Criar os drones;
- Definir as posições iniciais;
- Definir os destinos;
- Definir a velocidade de cada drone;
- Criar o simulador;
- Iniciar a execução da simulação.

---

### `config.py`

Arquivo que armazena os parâmetros gerais da simulação.

Exemplo:

```python
CONFIG = {
    "max_passos": 30,
    "raio_colisao": 1.0,
    "limite_x": (-1, 11),
    "limite_y": (-1, 11),
    "intervalo_animacao": 500
}
```

---

### `models/drone.py`

Arquivo que contém a classe `Drone`.

Cada objeto da classe `Drone` representa um drone da simulação.

Cada drone possui:

- Identificador;
- Posição atual;
- Posição inicial;
- Destino;
- Velocidade;
- Estado atual;
- Distância percorrida;
- Tempo de chegada.

Estados possíveis de um drone:

- `em_movimento`;
- `chegou`;
- `colidiu`;
- `nao_concluiu`.

---

### `simulation/simulator.py`

Arquivo responsável por controlar a execução da simulação.

Ele coordena:

- O avanço dos passos da simulação;
- A movimentação dos drones;
- A verificação de chegada ao destino;
- A verificação de colisões;
- O registro do histórico da simulação;
- A geração das métricas;
- A chamada da visualização.

---

### `simulation/collision.py`

Arquivo responsável pela lógica de colisão.

A colisão é verificada calculando a distância entre dois drones. Caso essa distância seja menor ou igual ao raio de colisão definido, os drones são marcados como colididos.

---

### `metrics/metrics.py`

Arquivo responsável por calcular e exibir as métricas finais da simulação.

As métricas incluem:

- Total de drones;
- Drones que chegaram ao destino;
- Drones que colidiram;
- Drones que não concluíram a missão;
- Taxa de sucesso;
- Taxa de colisão;
- Tempo total da simulação;
- Tempo médio de chegada;
- Distância média percorrida.

---

### `visualization/visualizer.py`

Arquivo responsável pela visualização gráfica da simulação.

A visualização mostra:

- Drones em movimento;
- Destinos dos drones;
- Estados dos drones por meio de cores;
- Evolução da simulação passo a passo.

---

## Instalação

Para executar o projeto, é necessário ter o Python instalado na máquina.

Após baixar ou clonar o repositório, acesse a pasta do projeto:

```bash
cd simulador-drones
```

Instale a biblioteca necessária:

```bash
pip install matplotlib
```

Caso esteja usando Linux ou tenha mais de uma versão do Python instalada, pode ser necessário usar:

```bash
pip3 install matplotlib
```

---

## Como Executar

Dentro da pasta do projeto, execute o arquivo principal:

```bash
python main.py
```

Ou, dependendo do ambiente:

```bash
python3 main.py
```

Ao executar o programa:

1. A simulação será iniciada;
2. Os drones serão movimentados em direção aos seus destinos;
3. As colisões serão verificadas;
4. As métricas finais serão exibidas no terminal;
5. Uma janela gráfica será aberta mostrando a movimentação dos drones.

---

## Parâmetros de Entrada

Os parâmetros gerais da simulação estão no arquivo `config.py`.

```python
CONFIG = {
    "max_passos": 30,
    "raio_colisao": 1.0,
    "limite_x": (-1, 11),
    "limite_y": (-1, 11),
    "intervalo_animacao": 500
}
```

### Descrição dos parâmetros

| Parâmetro | Descrição |
|---|---|
| `max_passos` | Quantidade máxima de passos da simulação |
| `raio_colisao` | Distância mínima para considerar colisão entre dois drones |
| `limite_x` | Limite horizontal do ambiente exibido na visualização |
| `limite_y` | Limite vertical do ambiente exibido na visualização |
| `intervalo_animacao` | Intervalo em milissegundos entre os quadros da animação |

---

## Definição dos Drones

Os drones são definidos no arquivo `main.py`.

Exemplo:

```python
drones = [
    Drone(id=1, posicao_inicial=(0, 0), destino=(10, 10), velocidade=1),
    Drone(id=2, posicao_inicial=(10, 10), destino=(0, 0), velocidade=1),
    Drone(id=3, posicao_inicial=(0, 10), destino=(10, 0), velocidade=1),
]
```

Cada drone possui os seguintes atributos de entrada:

| Atributo | Descrição |
|---|---|
| `id` | Identificador único do drone |
| `posicao_inicial` | Coordenada inicial do drone no ambiente 2D |
| `destino` | Coordenada final que o drone deve alcançar |
| `velocidade` | Quantidade de unidades percorridas por passo |

---

## Funcionamento da Simulação

A simulação ocorre em passos discretos. A cada passo, o simulador atualiza o estado dos drones.

O funcionamento geral é:

1. O simulador inicia com uma lista de drones;
2. Cada drone possui uma posição inicial e um destino;
3. A cada passo, os drones em movimento calculam a direção até o destino;
4. Cada drone se desloca de acordo com sua velocidade;
5. O sistema verifica se algum drone chegou ao destino;
6. O sistema verifica colisões entre os drones;
7. O estado atual dos drones é salvo no histórico;
8. O processo continua até que todos os drones finalizem ou o limite máximo de passos seja atingido;
9. Ao final, são exibidas as métricas e a visualização da simulação.

---

## Movimentação dos Drones

A movimentação é feita calculando a direção entre a posição atual do drone e o seu destino.

Para isso, o simulador calcula a distância até o destino e move o drone proporcionalmente na direção correta.

De forma simplificada:

```text
direção_x = (destino_x - x_atual) / distância
direção_y = (destino_y - y_atual) / distância

novo_x = x_atual + direção_x * velocidade
novo_y = y_atual + direção_y * velocidade
```

Quando a distância até o destino é menor ou igual à velocidade do drone, ele é colocado diretamente no destino e seu estado passa a ser `chegou`.

---

## Estados dos Drones

Durante a simulação, cada drone pode assumir um dos seguintes estados:

| Estado | Significado |
|---|---|
| `em_movimento` | O drone ainda está se deslocando até o destino |
| `chegou` | O drone alcançou o destino definido |
| `colidiu` | O drone colidiu com outro drone |
| `nao_concluiu` | O drone não chegou ao destino dentro do limite de passos |

---

## Tratamento de Colisões

Como todos os drones voam na mesma altura, a colisão é analisada apenas no plano bidimensional.

A verificação de colisão é feita comparando todos os pares de drones em movimento.

A distância entre dois drones é calculada pela distância euclidiana:

```text
distância = sqrt((x1 - x2)² + (y1 - y2)²)
```

Se a distância entre dois drones for menor ou igual ao `raio_colisao`, os dois drones são marcados com o estado `colidiu`.

Após uma colisão:

- Os drones envolvidos deixam de se movimentar;
- A missão desses drones é interrompida;
- O evento de colisão é registrado;
- Os drones colididos são contabilizados nas métricas finais.

Exemplo de evento registrado:

```text
Passo 7: Drone 1 colidiu com Drone 2
```

---

## Métricas Geradas

Ao final da simulação, o sistema apresenta as métricas finais no terminal.

As métricas geradas são:

| Métrica | Descrição |
|---|---|
| Total de drones | Quantidade total de drones simulados |
| Drones que chegaram ao destino | Quantidade de drones que concluíram a missão |
| Drones que colidiram | Quantidade de drones envolvidos em colisões |
| Drones que não concluíram a missão | Quantidade de drones que não chegaram ao destino dentro do limite de passos |
| Taxa de sucesso | Percentual de drones que chegaram ao destino |
| Taxa de colisão | Percentual de drones que colidiram |
| Tempo total da simulação | Número total de passos executados |
| Tempo médio de chegada | Média de passos necessários para os drones chegarem ao destino |
| Distância média percorrida | Média da distância percorrida pelos drones |

Exemplo de saída:

```text
========== MÉTRICAS FINAIS ==========
Total de drones: 3
Drones que chegaram ao destino: 1
Drones que colidiram: 2
Drones que não concluíram a missão: 0
Taxa de sucesso: 33.33%
Taxa de colisão: 66.67%
Tempo total da simulação: 7 passos
Tempo médio de chegada: 0.00 passos
Distância média percorrida: 6.67
```

---

## Visualização

A visualização da simulação é feita com a biblioteca Matplotlib.

Os drones são representados por pontos em um ambiente 2D, e os destinos são representados por marcadores em formato de `X`.

### Legenda de cores

| Cor | Significado |
|---|---|
| Azul | Drone em movimento |
| Verde | Drone chegou ao destino |
| Vermelho | Drone colidiu |
| Cinza | Drone não concluiu a missão |
| X preto | Destino do drone |

A visualização permite observar a dinâmica da simulação durante a execução, mostrando os drones se deslocando, chegando ao destino ou colidindo.

---

## Exemplo de Cenário

O cenário utilizado no exemplo possui três drones:

```python
drones = [
    Drone(id=1, posicao_inicial=(0, 0), destino=(10, 10), velocidade=1),
    Drone(id=2, posicao_inicial=(10, 10), destino=(0, 0), velocidade=1),
    Drone(id=3, posicao_inicial=(0, 10), destino=(10, 0), velocidade=1),
]
```

Nesse cenário, os drones seguem trajetórias que podem se cruzar, permitindo testar a detecção de colisão.

---

## Decisões de Modelagem

Durante o desenvolvimento, foram adotadas algumas decisões para simplificar e organizar a simulação:

- O ambiente é bidimensional;
- A visualização é feita em visão superior;
- Todos os drones voam na mesma altura;
- A movimentação ocorre em passos discretos;
- A velocidade de cada drone é constante;
- A colisão é detectada por proximidade entre drones;
- O raio de colisão é configurável;
- Quando dois drones colidem, ambos param de se movimentar;
- Drones que chegaram ao destino não continuam participando da movimentação;
- Drones que não chegam ao destino até o limite de passos são marcados como `nao_concluiu`.

---

## Limitações do Simulador

A versão atual possui algumas simplificações:

- Não há variação de altitude;
- Não há desvio de rota;
- Não há obstáculos fixos;
- Os drones não tentam evitar colisões;
- Os drones colididos são removidos da missão;
- O ambiente não possui restrições físicas complexas, como vento ou aceleração.

Essas limitações foram adotadas para manter o simulador simples, funcional e compatível com os requisitos principais do trabalho.

---

## Possíveis Melhorias Futuras

Algumas melhorias podem ser adicionadas em versões futuras:

- Fazer drones colididos permanecerem no ambiente como obstáculos;
- Criar cenários automáticos com posições aleatórias;
- Permitir velocidades diferentes para cada drone;
- Permitir configuração dos drones por arquivo externo;
- Exportar métricas para arquivo CSV;
- Gerar gráficos finais das métricas;
- Adicionar obstáculos fixos no ambiente;
- Implementar desvio de rota para evitar colisões;
- Permitir escolha de parâmetros pelo usuário via terminal;
- Salvar a animação em vídeo ou GIF;
- Criar uma interface gráfica mais completa.

---

## Como Apresentar o Projeto

Durante a apresentação, recomenda-se explicar o projeto na seguinte ordem:

1. Objetivo do simulador;
2. Estrutura dos arquivos;
3. Como os drones são representados;
4. Como ocorre a movimentação;
5. Como a colisão é detectada;
6. Quais métricas são geradas;
7. Como a visualização funciona;
8. Quais decisões de modelagem foram adotadas;
9. Quais melhorias poderiam ser implementadas futuramente.

Resumo para apresentação:

```text
O simulador representa drones em um ambiente 2D. Cada drone possui uma posição inicial, um destino e uma velocidade. A cada passo da simulação, os drones se movem em direção aos seus destinos. O sistema verifica colisões calculando a distância entre os drones. Se a distância for menor ou igual ao raio de colisão, os drones envolvidos são marcados como colididos. Ao final, o simulador apresenta métricas como quantidade de drones que chegaram, colidiram ou não concluíram a missão. A visualização mostra os drones em movimento com cores diferentes para cada estado.
```

---

## Autores

Projeto desenvolvido por:

- Sthefany Moura Godinho
- Rais Eliete de Sousa

Disciplina: Tópicos em Computação — Modelagem Analítica  
Professor: Francisco Airton