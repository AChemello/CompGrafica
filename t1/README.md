# Experimentos de desempenho (`performance.py`)

Este documento explica como reproduzir os experimentos do relatório do Trabalho 1. O
script `t1/src/performance.py` compara as **4 configurações** do algoritmo de inclusão de
ponto em triângulos e imprime os resultados em CSV:

| Nome no CSV | Etapas executadas |
|---|---|
| `forca_bruta` | teste detalhado em todos os triângulos |
| `envelopes` | envelope (AABB) → teste detalhado |
| `subdivisao` | grade uniforme → teste detalhado |
| `subdivisao+envelopes` | grade uniforme → envelope → teste detalhado |

Para cada combinação de parâmetros, o cenário é gerado **uma vez** e as quatro
configurações rodam sobre **o mesmo cenário e os mesmos pontos de consulta**. A cada ponto,
o conjunto de triângulos devolvido por cada configuração é comparado com o da força bruta;
se houver qualquer divergência, o script para com um erro (`Resultado divergente: ...`).

> O script **não abre janela**: não precisa do desktop virtual nem da porta 6080. O ambiente
> do Codespace (ver `README.md`) já tem tudo o que ele usa.

---

## Como rodar

A partir da raiz do repositório:

```bash
cd t1/src
```

Os três comandos abaixo geram os três arquivos usados no relatório. Rode **um de cada vez**,
esperando o anterior terminar. O `tee` mostra as linhas na tela enquanto grava o arquivo, e o
`-u` evita que a saída fique retida em buffer.

```bash
# 1) quantidade de triângulos, semente, tamanho e célula (pontos uniformes)
python -u performance.py --n 100 1000 5000 --seed 1 2 3 --size 4 8 --cell 5 10 20 --queries 100 --reps 2 | tee ../resultados.csv

# 2) posição dos pontos consultados
python -u performance.py --n 1000 --seed 1 2 3 --size 8 --cell 10 --pontos uniforme centro borda --queries 200 --reps 3 | tee ../resultados_pontos.csv

# 3) células pequenas (procura o melhor lado de célula)
python -u performance.py --n 5000 --seed 1 2 3 --size 8 --cell 1 2 3 5 --queries 100 --reps 2 | tee ../resultados_celulas.csv
```

Os arquivos são gravados em `t1/` (o `../` sobe uma pasta, saindo de `src/`). Para
interromper uma rodada, use **Ctrl+C**; o arquivo fica com o que já foi impresso.

**Atenção ao tempo.** Cada opção aceita vários valores, e o script roda **todas as
combinações** (o produto). Os valores padrão incluem `n = 10000`, que demora muito; use os
comandos acima, ou reduza `--n`, `--seed` e `--queries` para um teste rápido:

```bash
python -u performance.py --n 100 --seed 1 --pontos uniforme centro borda --queries 20 --reps 1
```

---

## Opções

| Opção | Padrão | Descrição |
|---|---|---|
| `--n` | `100 1000 10000` | Quantidades de triângulos |
| `--seed` | `1 2 3` | Sementes dos cenários |
| `--size` | `4 8` | Tamanho máximo dos triângulos (deslocamento máximo dos vértices a partir do centro) |
| `--cell` | `5 10 20` | Lado da célula da grade de subdivisão |
| `--pontos` | `uniforme` | Região de onde os pontos consultados são sorteados (ver abaixo) |
| `--queries` | `200` | Quantidade de pontos consultados por cenário |
| `--reps` | `3` | Repetições de cada consulta (o tempo de um ponto é a média delas) |

**Regiões dos pontos (`--pontos`):**

- `uniforme`: a área inteira, de −50 a 50 em cada eixo;
- `centro`: o quadrado de lado 30 ao redor da origem;
- `borda`: uma faixa de 10 unidades junto a um dos quatro lados da área.

Os pontos são gerados a partir da semente do cenário, então são **os mesmos em todas as
configurações** e se repetem a cada execução.

---

## Colunas do CSV

| Coluna | Significado |
|---|---|
| `n`, `seed`, `tamanho`, `celula`, `pontos` | Parâmetros da combinação |
| `config` | Configuração (ver a primeira tabela) |
| `consultas` | Quantidade de pontos consultados |
| `tempo_medio_ms` | Tempo médio de **uma consulta**, em milissegundos (não inclui a montagem) |
| `cand_sub_medio` | Candidatos devolvidos pela subdivisão (ou `n`, quando a subdivisão está desligada) |
| `cand_env_medio` | Candidatos que passaram pelo envelope (ou `n`, quando está desligado) |
| `testes_medio` | Testes detalhados executados por consulta |
| `contidos_medio` | Triângulos que contêm o ponto, em média |
| `build_aabb_ms` | Tempo, uma única vez, para construir os envelopes |
| `build_grid_ms` | Tempo, uma única vez, para construir a grade |
| `celulas_ocupadas` | Células da grade que guardam ao menos um triângulo |
| `max_indices_por_celula` | Maior quantidade de índices em uma única célula |

As colunas `build_*`, `celulas_ocupadas` e `max_indices_por_celula` descrevem o cenário e a
grade, por isso se repetem nas quatro linhas de uma mesma combinação.

Para ver o arquivo em colunas no terminal:

```bash
column -s, -t < ../resultados.csv | less -S
```

---

## Como interpretar os resultados

- **As contagens são determinísticas.** Para uma mesma semente e os mesmos parâmetros,
  `cand_sub_medio`, `cand_env_medio`, `testes_medio` e `contidos_medio` saem **idênticos** em
  qualquer máquina. É nelas que as conclusões do relatório se apoiam.
- **Os tempos variam.** Dependem da máquina e do ruído do ambiente (no Codespace, que é
  compartilhado, a força bruta chegou a variar de 0,70 a 1,05 ms fazendo exatamente o mesmo
  trabalho). Use os tempos para comparar configurações entre si e para ordens de grandeza,
  e prefira médias entre sementes.
- **O ganho** de uma configuração é a razão entre o tempo da força bruta e o dela.
- **Quanto a montagem custa:** `build_aabb_ms` + `build_grid_ms` é pago uma vez; divida pela
  economia por consulta (força bruta menos subdivisão + envelopes) para saber em quantas
  consultas ela se paga.

---

## Conferir a reprodutibilidade

Este teste curto confirma que o código reproduz as contagens do relatório (os tempos vão
diferir um pouco):

```bash
cd t1/src
python -u performance.py --n 1000 --seed 1 --size 8 --cell 10 --queries 100 --reps 2
```

Resultado esperado nas colunas de contagem:

| Configuração | Candidatos da subdivisão | Candidatos do envelope | Testes detalhados | Contidos |
|---|---|---|---|---|
| `forca_bruta` | 1000,00 | 1000,00 | 1000,00 | 1,910 |
| `envelopes` | 1000,00 | 6,42 | 6,42 | 1,910 |
| `subdivisao` | 29,76 | 29,76 | 29,76 | 1,910 |
| `subdivisao+envelopes` | 29,76 | 6,42 | 6,42 | 1,910 |

Os resultados do relatório foram gerados com o código do commit `c264db4`.

---

## Observações

- Os arquivos `.csv` **não são versionados** (estão no `.gitignore`); guarde uma cópia fora
  do Git, ou regenere-os com os comandos acima.
- Python puro, sem `numpy`, no laço de consulta: as razões entre configurações são mais
  confiáveis que os tempos absolutos.
- O programa interativo (janela OpenGL) e as opções dele estão no `README.md` principal.