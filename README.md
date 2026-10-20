# Computação Gráfica – Trabalho 1: Inclusão de Ponto em Triângulos

Programa em Python + OpenGL (PyOpenGL/GLUT) que, dado um ponto controlado pelo mouse,
descobre em quais triângulos de um cenário ele está contido. Permite comparar quatro
configurações do algoritmo (teste detalhado, envelopes, subdivisão espacial e combinações)
e acompanhar visualmente cada etapa.

---

## Como executar (GitHub Codespaces) — recomendado

O ambiente está totalmente configurado em `.devcontainer/`. **Não é preciso instalar nada
manualmente.** Basta seguir os passos abaixo.

### 1. Criar o Codespace

1. Na página do repositório no GitHub, clique em **Code**.
2. Abra a aba **Codespaces**.
3. Clique em **Create codespace on main**.

Na primeira vez, a criação leva alguns minutos: o container é montado, o desktop virtual
e as bibliotecas OpenGL/freeglut são instalados e as dependências Python são instaladas
(`PyOpenGL`, `numpy`). Aguarde até o terminal ficar disponível e o `postCreateCommand`
terminar.

### 2. Abrir o desktop virtual (onde a janela do OpenGL aparece)

O Codespace não tem monitor, então a janela gráfica é exibida em um desktop virtual
acessado pelo navegador:

1. No painel inferior do VS Code, abra a aba **PORTAS** (*PORTS*).
2. Na linha da porta **6080** ("Desktop (janela OpenGL)"), clique no **ícone de globo**
   (*Abrir no Navegador*).
3. Na página do noVNC que abrir, clique em **Connect**.
   - Se pedir senha, use: `vscode`.
   - Se aparecer uma listagem de arquivos ou "Not Found", acrescente `/vnc.html` ao final
     do endereço.

Deixe essa aba do navegador aberta ao lado do VS Code.

> A porta **5901** é o servidor VNC "cru" e não precisa ser aberta. Use apenas a **6080**.

### 3. Rodar o programa

No terminal do Codespace:

```bash
./run.sh
```

Equivale a:

```bash
cd t1 && python src/main.py
```

A janela **"T1 - Inclusao de Ponto em Poligonos"** aparece dentro do desktop virtual
(aba da porta 6080). Para ver o resultado, **mova o mouse sobre a janela do OpenGL**.

> Se uma janela pequena chamada "VNC config" aparecer, pode ignorá-la ou fechá-la; ela é do
> próprio servidor VNC e não afeta o programa.

### 4. Encerrar

- Tecla **ESC** com a janela do OpenGL em foco, ou
- **Ctrl+C** no terminal.
- Se o terminal travar: **Ctrl+\\**.

---

## Controles

| Entrada | Efeito |
|---|---|
| **Mouse** (movimento) | Move o ponto de consulta |
| `1` | Somente teste detalhado em todos os triângulos (força bruta / referência) |
| `2` | Envelopes (AABB) + teste detalhado |
| `3` | Subdivisão espacial (grade uniforme) + teste detalhado |
| `4` | Subdivisão espacial + envelopes + teste detalhado |
| `g` | Liga/desliga a exibição da grade e da célula que contém o ponto |
| `e` | Liga/desliga a exibição dos envelopes de todos os triângulos |
| `c` | Liga/desliga a coloração dos candidatos intermediários |
| `ESC` | Sai do programa |

Alterar a visualização (`g`, `e`, `c`) **não** modifica o resultado dos testes.

## Legenda de cores

| Cor | Significado |
|---|---|
| Azul acinzentado | Triângulo não considerado na consulta |
| Amarelo | Candidato produzido pela subdivisão espacial |
| Laranja | Candidato aprovado pelo teste de envelope |
| Vermelho | Triângulo que **efetivamente contém** o ponto |
| Moldura amarela na grade | Célula da subdivisão que contém o ponto |
| Linhas verdes | Envelopes (AABB), quando ativados com `e` |
| Ponto branco | Posição de consulta |

## Informações exibidas na tela (por consulta)

Os contadores são zerados a cada nova posição do ponto e mostram:

- posição do ponto e configuração ativa (subdivisão / envelope ligados ou não);
- quantidade total de triângulos do cenário;
- candidatos produzidos pela subdivisão espacial;
- candidatos aprovados pelos envelopes;
- testes detalhados executados;
- triângulos que contêm o ponto;
- tempo da consulta (ms);
- **verificação contra a força bruta**: indica `OK` quando o resultado da configuração
  ativa é idêntico ao do teste detalhado aplicado a todos os triângulos (referência), ou
  `DIVERGE!` caso contrário.

---

## Parâmetros do cenário

Ficam no início de `t1/src/main.py`:

```python
BOUNDS = (-50, 50, -50, 50)   # limites do cenário
SEED = 42                     # semente da geração aleatória (reprodutível)
N_TRIANGLES = 200             # quantidade de triângulos
CELL_SIZE = 10                # tamanho da célula da grade uniforme
```

Para repetir um experimento, mantenha a mesma `SEED`. O tamanho máximo dos triângulos
é o parâmetro `max_size` de `generate_random_triangles` em `t1/src/geometry.py`.

Também é possível carregar triângulos de um arquivo com `load_triangles_from_file`
(formato: uma linha por triângulo, `ax ay bx by cx cy`; exemplo em `t1/data/`).

---

## Estrutura do projeto

```
.
├── .devcontainer/
│   └── devcontainer.json     # ambiente do Codespace (Python, OpenGL, desktop virtual)
├── run.sh                    # atalho para executar o programa
└── t1/
    ├── requirements.txt      # dependências Python
    ├── data/                 # arquivos de entrada de exemplo
    └── src/
        ├── main.py           # janela GLUT, callbacks, entrada e laço principal
        ├── geometry.py       # dados geométricos: triângulos, geração e leitura
        ├── acceleration.py   # envelopes (AABB) e subdivisão espacial (grade uniforme)
        ├── inclusion_tests.py# teste detalhado e pipeline de consulta configurável
        ├── visualization.py  # funções de desenho (OpenGL)
        └── performance.py    # utilitários de medição de tempo
```

A separação segue o enunciado: dados geométricos, estruturas de aceleração, algoritmos
de teste e visualização ficam em módulos distintos.

---

## Solução de problemas

| Problema | O que fazer |
|---|---|
| Porta 6080 não aparece na aba PORTAS | Clique em **Adicionar Porta**, digite `6080`. Se não houver desktop, use **Ctrl+Shift+P → "Codespaces: Rebuild Container"**. |
| Página do noVNC em branco ou "Not Found" | Acrescente `/vnc.html` ao endereço da porta 6080. |
| Janela do OpenGL não aparece | Confirme que clicou em **Connect** no noVNC e que a aba do desktop está aberta. No terminal, rode `export DISPLAY=:1` e tente de novo. |
| `ModuleNotFoundError: No module named 'OpenGL'` | Rode `pip install -r t1/requirements.txt`. |
| `Ctrl+C` não encerra | Use ESC na janela, ou `Ctrl+\`. |
| Ambiente criado de forma incompleta | **Ctrl+Shift+P → "Codespaces: Full Rebuild Container"**. |

Para conferir que o ambiente está correto:

```bash
python -c "from OpenGL.GL import *; from OpenGL.GLUT import *; print('OpenGL OK')"
```

---

## Execução local (alternativa, sem Codespaces)

Requer Python 3.10+ e uma biblioteca GLUT instalada no sistema.

**Linux (Debian/Ubuntu):**

```bash
sudo apt-get install -y freeglut3-dev libglu1-mesa-dev libgl1-mesa-dev
pip install -r t1/requirements.txt
cd t1 && python src/main.py
```

**macOS:** `pip install -r t1/requirements.txt` (o GLUT já vem com o sistema).

**Windows:** `pip install -r t1/requirements.txt` e disponibilizar a `freeglut.dll`
no PATH ou na pasta do projeto.

O uso do Codespace é preferível por dispensar essa configuração.