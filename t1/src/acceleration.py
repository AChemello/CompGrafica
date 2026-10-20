import math
from dataclasses import dataclass

EPS = 1e-9  # tolerancia numerica (borda/vertice contam como dentro)


@dataclass
class AABB:
    min_x: float
    max_x: float
    min_y: float
    max_y: float

    @staticmethod
    def from_triangle(tri):
        xs = (tri.a[0], tri.b[0], tri.c[0])
        ys = (tri.a[1], tri.b[1], tri.c[1])
        return AABB(min(xs), max(xs), min(ys), max(ys))

    def contains_point(self, p, eps=EPS):
        return (self.min_x - eps <= p[0] <= self.max_x + eps and
                self.min_y - eps <= p[1] <= self.max_y + eps)


class UniformGrid:
    """Subdivisao uniforme. Guarda so INDICES dos triangulos (nao copia geometria)."""

    def __init__(self, aabbs, cell_size):
        self.cell_size = cell_size
        self.cells = {}  # (cx, cy) -> [indices]; origem da grade em (0,0)
        for i, box in enumerate(aabbs):
            cx0, cy0 = self._cell_of(box.min_x - EPS, box.min_y - EPS)
            cx1, cy1 = self._cell_of(box.max_x + EPS, box.max_y + EPS)
            for cx in range(cx0, cx1 + 1):
                for cy in range(cy0, cy1 + 1):
                    self.cells.setdefault((cx, cy), []).append(i)

    def _cell_of(self, x, y):
        return (math.floor(x / self.cell_size), math.floor(y / self.cell_size))

    def candidate_indices(self, p):
        return self.cells.get(self._cell_of(p[0], p[1]), [])

    def stats(self):
        """(celulas ocupadas, media de indices por celula, maximo) - util pro relatorio."""
        tamanhos = [len(v) for v in self.cells.values()]
        if not tamanhos:
            return 0, 0.0, 0
        return len(tamanhos), sum(tamanhos) / len(tamanhos), max(tamanhos)