import random
from dataclasses import dataclass

AREA_MINIMA = 1e-6  # descarta triangulos degenerados


@dataclass(frozen=True)
class Triangle:
    a: tuple
    b: tuple
    c: tuple

    def area2(self):
        return abs((self.b[0] - self.a[0]) * (self.c[1] - self.a[1])
                   - (self.c[0] - self.a[0]) * (self.b[1] - self.a[1]))


def new_seed():
    return random.SystemRandom().randrange(1, 2 ** 31)


def generate_random_triangles(n, bounds=(-50, 50, -50, 50), max_size=8, seed=None):
    if max_size <= 0:
        raise ValueError("--size deve ser maior que zero")
    rng = random.Random(seed)
    xmin, xmax, ymin, ymax = bounds
    triangles = []
    tentativas = 0
    while len(triangles) < n:
        tentativas += 1
        if tentativas > 100 * n:
            raise ValueError(
                "nao consegui gerar triangulos validos; aumente --size")
        cx, cy = rng.uniform(xmin, xmax), rng.uniform(ymin, ymax)
        verts = [(cx + rng.uniform(-max_size, max_size),
                  cy + rng.uniform(-max_size, max_size)) for _ in range(3)]
        tri = Triangle(*verts)
        if tri.area2() > AREA_MINIMA:
            triangles.append(tri)
    return triangles


def load_triangles_from_file(path):
    """Uma linha por triangulo: 'ax ay bx by cx cy'. Linhas com # sao comentario."""
    triangles = []
    with open(path, encoding="utf-8") as f:
        for num, line in enumerate(f, start=1):
            line = line.split("#")[0].strip()
            if not line:
                continue
            vals = [float(v) for v in line.replace(",", " ").split()]
            if len(vals) != 6:
                raise ValueError(
                    f"{path}, linha {num}: esperado 6 numeros, achei {len(vals)}")
            tri = Triangle((vals[0], vals[1]),
                           (vals[2], vals[3]), (vals[4], vals[5]))
            if tri.area2() > AREA_MINIMA:
                triangles.append(tri)
            else:
                print(f"aviso: {path}, linha {num}: triangulo degenerado ignorado")
    return triangles
