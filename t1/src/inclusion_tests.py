import time
from dataclasses import dataclass, field

from acceleration import EPS


def ponto_no_triangulo(p, a, b, c, eps=EPS):
    """Teste detalhado do enunciado (lateralidade, Aula 3/4), com tolerancia."""
    def orientacao(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    d1 = orientacao(p, a, b)
    d2 = orientacao(p, b, c)
    d3 = orientacao(p, c, a)
    tem_negativo = (d1 < -eps) or (d2 < -eps) or (d3 < -eps)
    tem_positivo = (d1 > eps) or (d2 > eps) or (d3 > eps)
    return not (tem_negativo and tem_positivo)


@dataclass
class QueryStats:
    total_triangulos: int = 0
    candidatos_subdivisao: int = 0
    candidatos_envelope: int = 0
    testes_detalhados: int = 0
    contidos: list = field(default_factory=list)
    cand_sub: list = field(default_factory=list)   # para visualização
    cand_env: list = field(default_factory=list)   # para visualização
    tempo_s: float = 0.0


def query(p, triangles, aabbs, grid=None, use_subdivision=True, use_envelope=True):
    """Pipeline: subdivisão -> envelope -> teste detalhado (cada etapa liga/desliga)."""
    t0 = time.perf_counter()
    stats = QueryStats(total_triangulos=len(triangles))

    if use_subdivision and grid is not None:
        indices = list(grid.candidate_indices(p))
    else:
        indices = list(range(len(triangles)))
    stats.candidatos_subdivisao = len(indices)
    stats.cand_sub = indices

    if use_envelope:
        indices = [i for i in indices if aabbs[i].contains_point(p)]
    stats.candidatos_envelope = len(indices)
    stats.cand_env = indices

    for i in indices:
        stats.testes_detalhados += 1
        tri = triangles[i]
        if ponto_no_triangulo(p, tri.a, tri.b, tri.c):
            stats.contidos.append(i)

    stats.tempo_s = time.perf_counter() - t0
    return stats