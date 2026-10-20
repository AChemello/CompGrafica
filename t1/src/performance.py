import argparse
import itertools
import random
import time

from geometry import generate_random_triangles
from acceleration import AABB, UniformGrid
from inclusion_tests import query

BOUNDS = (-50, 50, -50, 50)  # mesmo cenario do main.py
CONFIGS = [
    ("forca_bruta", False, False),
    ("envelopes", False, True),
    ("subdivisao", True, False),
    ("subdivisao+envelopes", True, True),
]
CABECALHO = ("n,seed,tamanho,celula,config,consultas,tempo_medio_ms,cand_sub_medio,"
             "cand_env_medio,testes_medio,contidos_medio,build_aabb_ms,build_grid_ms,"
             "celulas_ocupadas,max_indices_por_celula")


def pontos_de_consulta(qtd, seed):
    rng = random.Random(seed * 1000 + 17)  # reprodutivel: mesmos pontos em todas as configs
    xmin, xmax, ymin, ymax = BOUNDS
    return [(rng.uniform(xmin, xmax), rng.uniform(ymin, ymax)) for _ in range(qtd)]


def rodar(n, seed, tamanho, celula, qtd, reps):
    triangulos = generate_random_triangles(n, BOUNDS, max_size=tamanho, seed=seed)
    t0 = time.perf_counter()
    aabbs = [AABB.from_triangle(t) for t in triangulos]
    t1 = time.perf_counter()
    grid = UniformGrid(aabbs, cell_size=celula)
    t2 = time.perf_counter()
    ocupadas, _, maximo = grid.stats()
    pontos = pontos_de_consulta(qtd, seed)
    referencia = [set(query(p, triangulos, aabbs, None, False, False).contidos) for p in pontos]

    linhas = []
    for nome, usa_sub, usa_env in CONFIGS:
        tempo = sub = env = testes = contidos = 0.0
        for p, ref in zip(pontos, referencia):
            for _ in range(reps):
                s = query(p, triangulos, aabbs, grid, usa_sub, usa_env)
                tempo += s.tempo_s
            if set(s.contidos) != ref:
                raise RuntimeError(f"Resultado divergente: {nome}, n={n}, seed={seed}, p={p}")
            sub += s.candidatos_subdivisao
            env += s.candidatos_envelope
            testes += s.testes_detalhados
            contidos += len(s.contidos)
        q = len(pontos)
        linhas.append(
            f"{n},{seed},{tamanho},{celula},{nome},{q},{tempo / (q * reps) * 1000:.5f},"
            f"{sub / q:.2f},{env / q:.2f},{testes / q:.2f},{contidos / q:.3f},"
            f"{(t1 - t0) * 1000:.3f},{(t2 - t1) * 1000:.3f},{ocupadas},{maximo}")
    return linhas


def principal(argv=None):
    ap = argparse.ArgumentParser(description="Benchmark das 4 configuracoes (gera CSV)")
    ap.add_argument("--n", type=int, nargs="+", default=[100, 1000, 10000])
    ap.add_argument("--seed", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--size", type=float, nargs="+", default=[4, 8])
    ap.add_argument("--cell", type=float, nargs="+", default=[5, 10, 20])
    ap.add_argument("--queries", type=int, default=200)
    ap.add_argument("--reps", type=int, default=3)
    args = ap.parse_args(argv)
    print(CABECALHO)
    for n, seed, tam, cel in itertools.product(args.n, args.seed, args.size, args.cell):
        for linha in rodar(n, seed, tam, cel, args.queries, args.reps):
            print(linha)


if __name__ == "__main__":
    principal()