# Computação Gráfica – Trabalho 1: Inclusão de Ponto em Triângulos

Programa em Python + OpenGL (PyOpenGL/GLUT) que, dado um ponto controlado pelo mouse,
descobre em quais triângulos de um cenário ele está contido. Permite comparar quatro
configurações do algoritmo (teste detalhado, envelopes, subdivisão espacial e combinações)
e acompanhar visualmente cada etapa.

---

## Início rápido (GitHub Codespaces)

O ambiente está totalmente configurado em `.devcontainer/`. **Não é preciso instalar nada
manualmente.**

1. No GitHub: **Code → Codespaces → Create codespace on main** (a primeira criação leva
   alguns minutos).
2. Na aba **PORTAS**, clique no **ícone de globo** da porta **6080** e, na página que abrir,
   em **Connect** (se pedir senha: `vscode`).
3. No terminal do Codespace, na raiz do repositório:
   ```bash
   ./run.sh
   ```
4. Volte à aba do navegador com o desktop: a janela do OpenGL está lá. **Mova o mouse sobre
   ela.**

Detalhes de cada passo abaixo.

---

## Se os arquivos forem arrastados para um Codespace (é preciso dar rebuild)
 
O ambiente só é montado a partir da pasta `.devcontainer/` **quando o Codespace é criado ou
reconstruído**. Por isso, se o Codespace foi aberto vazio (ou a partir de outro repositório)
e os arquivos deste projeto foram **arrastados para dentro dele depois**, ele **não foi
inicializado do jeito correto**: não aparecem as portas, não existe o desktop virtual e as
bibliotecas não estão instaladas (`ModuleNotFoundError: No module named 'OpenGL'`).
 
Para corrigir:
 
1. **Confira a estrutura.** A pasta `.devcontainer/` (oculta), o `run.sh` e a pasta `t1/`
   precisam estar **na raiz** do workspace, lado a lado. **Tudo o que está dentro de `t1/`
   permanece como está** (`src/`, `data/`, `requirements.txt`).
```
   <raiz do workspace>
   ├── .devcontainer/        ← na raiz (pasta oculta)
   ├── run.sh                ← na raiz
   └── t1/                   ← o conteúdo interno não muda
       ├── requirements.txt
       ├── data/
       └── src/
```
 
   Se tudo ficou dentro de uma pasta extra (por exemplo `CompGrafica-main/`, criada ao
   baixar o `.zip`), mova o conteúdo dela para a raiz:
 
```bash
   cd /workspaces/<nome-do-workspace>
   shopt -s dotglob
   mv -f CompGrafica-main/* .
   rmdir CompGrafica-main
   ls -a
```
 
   (`dotglob` faz o `*` incluir a pasta oculta `.devcontainer`.)
 
2. **Reconstrua o ambiente:** **Ctrl+Shift+P → "Codespaces: Full Rebuild Container"**.
   Leva alguns minutos e a página recarrega sozinha. Use o *Full* Rebuild.
3. **Confira.** Depois de recarregar, a porta **6080** deve aparecer na aba **PORTAS** e
   este comando deve imprimir `OpenGL OK`:
```bash
   python -c "from OpenGL.GL import *; from OpenGL.GLUT import *; print('OpenGL OK')"
```
 
A forma mais simples de evitar isso é criar o Codespace **diretamente de um repositório**
que já contenha os arquivos (**Code → Codespaces → Create codespace on main**): assim o
`.devcontainer/` é aplicado já na criação e nenhum rebuild é necessário.

---

## Como executar (passo a passo)

### 1. Criar o Codespace

1. Na página do repositório no GitHub, clique em **Code**.
2. Abra a aba **Codespaces**.
3. Clique em **Create codespace on main**.

Na primeira vez, o container é montado, o desktop virtual e as bibliotecas
OpenGL/freeglut são instalados e as dependências Python são instaladas (`PyOpenGL`,
`numpy`). Aguarde o terminal ficar disponível e o `postCreateCommand` terminar.

### 2. Abrir o desktop virtual (onde a janela do OpenGL aparece)

O Codespace não tem monitor, então a janela gráfica é exibida em um desktop virtual
acessado pelo navegador:

1. No painel inferior do VS Code, abra a aba **PORTAS** (*PORTS*).
2. Na linha da porta **6080** ("Desktop (janela OpenGL)"), clique no **ícone de globo**
   (*Abrir no Navegador*).
3. Na página do noVNC, clique em **Connect**.
   - Se pedir senha, use: `vscode`.
   - Se aparecer uma listagem de arquivos ou "Not Found", acrescente `/vnc.html` ao final
     do endereço.

Deixe essa aba aberta ao lado do VS Code.

> A porta **5901** é o servidor VNC "cru" e não precisa ser aberta. Use apenas a **6080**.

### 3. Rodar o programa

No terminal do Codespace, **na raiz do repositório** (`/workspaces/CompGrafica`):

```bash
./run.sh
```

Se aparecer `Permission denied`, use:

```bash
bash run.sh
```

O comando equivale a `cd t1 && python src/main.py`. Ao iniciar, o terminal imprime a
quantidade de triângulos, a **semente** usada e o tamanho da célula, por exemplo:

```
Triangulos: 200  seed: 323197073  celula: 10
```

O terminal fica ocupado enquanto o programa roda; isso é normal. A janela
**"T1 - Inclusao de Ponto em Poligonos"** aparece no desktop virtual (aba da porta 6080).

> Se uma janela pequena chamada "VNC config" aparecer, pode ignorá-la ou fechá-la; ela é do
> próprio servidor VNC e não afeta o programa.

### 4. Encerrar

- Tecla **ESC** com a janela do OpenGL em foco, ou
- **Ctrl+C** no terminal.

---

## Opções de linha de comando

O `run.sh` repassa seus argumentos ao programa:

| Opção | Padrão | Descrição |
|---|---|---|
| `--n N` | `200` | Quantidade de triângulos gerados |
| `--seed S` | sorteada | Semente da geração aleatória. Se omitida, é sorteada e impressa no terminal |
| `--size T` | `8` | Tamanho máximo dos triângulos (deslocamento máximo dos vértices a partir do centro) |
| `--cell C` | `10` | Lado da célula da grade de subdivisão espacial |
| `--arquivo ARQ` | – | Lê os triângulos de um arquivo, em vez de gerá-los |

Exemplos:

```bash
./run.sh                                   # cenário aleatório padrão
./run.sh --n 1000 --seed 7                 # 1000 triângulos, semente 7
./run.sh --n 500 --seed 7 --cell 5         # mesma semente, grade mais fina
./run.sh --size 15                         # triângulos maiores
./run.sh --arquivo data/triangulo_exemplo.txt   # a partir de arquivo
```

**Reprodutibilidade:** a mesma semente (com os mesmos `--n` e `--size`) gera sempre o mesmo
cenário. A semente aparece na tela e no terminal, então qualquer execução pode ser repetida.

**Caminho do arquivo:** o `run.sh` executa o programa de dentro da pasta `t1/`, portanto o
caminho de `--arquivo` é relativo a ela (`data/triangulo_exemplo.txt`, e não
`t1/data/...`).

### Formato do arquivo de triângulos

Uma linha por triângulo, com seis números: `ax ay bx by cx cy`. Linhas em branco são
ignoradas, `#` inicia um comentário e vírgulas também são aceitas como separador.
Triângulos degenerados (área praticamente nula) são ignorados.

```
# ax ay   bx by   cx cy
-10 -10   10 -10    0 10
 20  20   30  20   25 30
```

O cenário é exibido na região `(-50, 50) × (-50, 50)`; coordenadas fora dela ficam fora da
janela.

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

---

## O que aparece na tela

### Cores

Uma linha de legenda na parte inferior da janela mostra as cores principais. Completa:

| Cor | Significado |
|---|---|
| Vermelho | Triângulo que **efetivamente contém** o ponto |
| Laranja | Candidato aprovado pelo teste de envelope |
| Amarelo-oliva | Candidato produzido pela subdivisão espacial |
| Azul acinzentado | Triângulo não considerado na consulta |
| Moldura amarela na grade | Célula da subdivisão que contém o ponto |
| Linhas verdes | Envelopes (AABB), quando ativados com `e` |
| Ponto branco | Posição de consulta |

### Informações do cabeçalho

Os contadores são recalculados a cada nova posição do ponto e mostram:

- semente, tamanho da célula e quantidade de triângulos do cenário;
- resumo das teclas;
- posição do ponto e configuração ativa (subdivisão / envelope ligados ou não);
- total de triângulos, candidatos da subdivisão espacial e candidatos aprovados pelos
  envelopes;
- testes detalhados executados e triângulos que contêm o ponto;
- tempo da consulta (ms);
- **verificação contra a força bruta**: `OK` quando o resultado da configuração ativa é
  idêntico ao do teste detalhado aplicado a todos os triângulos (referência), ou
  `DIVERGE!` caso contrário.

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
        ├── main.py           # argumentos, janela GLUT, callbacks e laço principal
        ├── geometry.py       # dados geométricos: triângulos, geração e leitura
        ├── acceleration.py   # envelopes (AABB) e subdivisão espacial (grade uniforme)
        ├── inclusion_tests.py# teste detalhado e pipeline de consulta configurável
        ├── visualization.py  # funções de desenho (OpenGL)
        └── performance.py    # utilitários de medição de tempo
```

A separação segue o enunciado: dados geométricos, estruturas de aceleração, algoritmos
de teste e visualização ficam em módulos distintos. A consulta (`query`) executa as etapas
em sequência — subdivisão → envelope → teste detalhado — e cada etapa pode ser ligada ou
desligada de forma independente, o que dá as quatro configurações das teclas `1` a `4`.

---

## Solução de problemas

| Problema | O que fazer |
|---|---|
| `./run.sh: No such file or directory` | Você não está na raiz do repositório. Use `cd /workspaces/CompGrafica` (ou `../run.sh` se estiver em `t1/`). |
| `./run.sh: Permission denied` | Use `bash run.sh` ou `chmod +x run.sh`. |
| Porta 6080 não aparece na aba PORTAS | Clique em **Adicionar Porta** e digite `6080`. Se continuar sem desktop, **Ctrl+Shift+P → "Codespaces: Full Rebuild Container"**. |
| Página do noVNC em branco ou "Not Found" | Acrescente `/vnc.html` ao endereço da porta 6080. |
| Janela do OpenGL não aparece | Confirme que clicou em **Connect** no noVNC e que a aba do desktop está aberta. No terminal, rode `export DISPLAY=:1` e tente de novo. |
| Cabeçalho da janela cortado no topo | A janela é maior que o desktop virtual. Segure **Alt** e arraste a janela com o botão esquerdo, ou use o botão de maximizar dela. |
| `ModuleNotFoundError: No module named 'OpenGL'` | Rode `pip install -r t1/requirements.txt`. |
| `Ctrl+C` não encerra | Use ESC na janela do OpenGL, ou `Ctrl+\`. |
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

Em qualquer sistema, as opções da seção "Opções de linha de comando" valem com
`python src/main.py` (dentro de `t1/`). O uso do Codespace é preferível por dispensar esta
configuração.