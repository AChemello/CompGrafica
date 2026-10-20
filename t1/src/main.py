import signal
import os

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import argparse
from geometry import generate_random_triangles, load_triangles_from_file, new_seed
from acceleration import AABB, UniformGrid
from inclusion_tests import query
import visualization as vis

BOUNDS = (-50, 50, -50, 50)

ap = argparse.ArgumentParser(description="T1 - Inclusao de ponto em poligonos")
ap.add_argument("--n", type=int, default=200, help="quantidade de triangulos")
ap.add_argument("--seed", type=int, default=None,
                help="semente (se omitida, sorteia e imprime)")
ap.add_argument("--size", type=float, default=8,
                help="tamanho maximo dos triangulos")
ap.add_argument("--cell", type=float, default=10,
                help="lado da celula da grade")
ap.add_argument("--arquivo", default=None,
                help="le os triangulos de um arquivo")
args = ap.parse_args()

CELL_SIZE = args.cell
if args.arquivo:
    SEED = None
    triangles = load_triangles_from_file(args.arquivo)
else:
    SEED = args.seed if args.seed is not None else new_seed()
    triangles = generate_random_triangles(
        args.n, BOUNDS, max_size=args.size, seed=SEED)
print(f"Triangulos: {len(triangles)}  seed: {SEED}  celula: {CELL_SIZE}")

aabbs = [AABB.from_triangle(t) for t in triangles]
grid = UniformGrid(aabbs, cell_size=CELL_SIZE)

state = {
    "point": (0.0, 0.0),
    "use_subdivision": True,
    "use_envelope": True,
    "show_grid": True,
    "show_envelopes": False,
    "show_candidates": True,
    "sair": False,
}

# Cores por categoria
COR_BASE = (0.25, 0.25, 0.40)
COR_CAND_SUB = (0.55, 0.50, 0.10)   # candidatos da subdivisão
COR_CAND_ENV = (0.90, 0.55, 0.10)   # aprovados pelo envelope
COR_CONTIDO = (0.90, 0.20, 0.20)    # contêm o ponto


# encerramento limpo 
viewport = [0, 0, 1, 1]   # x, y, largura, altura em pixels
def pedir_saida(*_):
    state["sair"] = True


def tick(_):
    if state["sair"]:
        os._exit(0)
        return
    glutTimerFunc(100, tick, 0)


# desenho 
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    p = state["point"]

    stats = query(p, triangles, aabbs, grid,
                  state["use_subdivision"], state["use_envelope"])

    # Referência (força bruta) para verificar o resultado acelerado
    ref = query(p, triangles, aabbs, None, False, False)
    ok = set(ref.contidos) == set(stats.contidos)

    if state["show_grid"] and state["use_subdivision"]:
        vis.draw_grid(CELL_SIZE, BOUNDS)
        vis.draw_cell(grid._cell_of(*p), CELL_SIZE)

    contidos = set(stats.contidos)
    cand_env = set(stats.cand_env)
    cand_sub = set(stats.cand_sub)

    for i, tri in enumerate(triangles):
        if i in contidos:
            cor = COR_CONTIDO
        elif state["show_candidates"] and i in cand_env and state["use_envelope"]:
            cor = COR_CAND_ENV
        elif state["show_candidates"] and i in cand_sub and state["use_subdivision"]:
            cor = COR_CAND_SUB
        else:
            cor = COR_BASE
        vis.draw_triangle(tri, cor)

    if state["show_envelopes"]:
        for box in aabbs:
            vis.draw_aabb(box, (0.0, 0.7, 0.0))

    vis.draw_point(p)

    modo = (f"sub={'ON' if state['use_subdivision'] else 'off'} "
            f"env={'ON' if state['use_envelope'] else 'off'}")
    linhas = [
        f"Seed: {SEED}  Celula: {CELL_SIZE}  Triangulos: {len(triangles)}",
        "Teclas: 1 forca bruta | 2 envelopes | 3 subdivisao | 4 sub+env",
        "        g grade | e envelopes | c candidatos | ESC sai",
         "Cores: vermelho=contem | laranja=envelope | amarelo=subdivisao",
        "       azul=nao testado | moldura amarela=celula do ponto",
        f"Ponto: ({p[0]:.2f}, {p[1]:.2f})   Config: {modo}",
        f"Total: {stats.total_triangulos}  Cand.subdiv: {stats.candidatos_subdivisao}  "
        f"Cand.envelope: {stats.candidatos_envelope}",
        f"Testes detalhados: {stats.testes_detalhados}  Contidos: {len(stats.contidos)}  "
        f"Tempo: {stats.tempo_s * 1000:.3f} ms",
        f"Verificacao vs forca bruta: {'OK' if ok else 'DIVERGE!'}",
    ]
    h = glutGet(GLUT_WINDOW_HEIGHT)
    y = h - 16
    for linha in linhas:
        vis.draw_text_px(8, y, linha)
        y -= 16

    glutSwapBuffers()


# entrada
def motion(x, y):
    vx, vy, vw, vh = viewport
    h = glutGet(GLUT_WINDOW_HEIGHT)
    u = min(max((x - vx) / vw, 0.0), 1.0)          # 0..1, limitado ao quadrado
    v = min(max(((h - y) - vy) / vh, 0.0), 1.0)    # y do OpenGL cresce para cima
    state["point"] = (BOUNDS[0] + u * (BOUNDS[1] - BOUNDS[0]),
                      BOUNDS[2] + v * (BOUNDS[3] - BOUNDS[2]))
    glutPostRedisplay()


def keyboard(key, x, y):
    if key == b'\x1b':  # ESC
        os._exit(0)
        return
    if key == b'1':
        state["use_subdivision"], state["use_envelope"] = False, False
    elif key == b'2':
        state["use_subdivision"], state["use_envelope"] = False, True
    elif key == b'3':
        state["use_subdivision"], state["use_envelope"] = True, False
    elif key == b'4':
        state["use_subdivision"], state["use_envelope"] = True, True
    elif key == b'g':
        state["show_grid"] = not state["show_grid"]
    elif key == b'e':
        state["show_envelopes"] = not state["show_envelopes"]
    elif key == b'c':
        state["show_candidates"] = not state["show_candidates"]
    glutPostRedisplay()


def reshape(w, h):
    lado = min(w, h)
    vx, vy = (w - lado) // 2, (h - lado) // 2
    viewport[:] = [vx, vy, lado, lado]
    glViewport(vx, vy, lado, lado)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(*BOUNDS)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    signal.signal(signal.SIGINT, pedir_saida)

    glutInit()
    altura_tela = glutGet(GLUT_SCREEN_HEIGHT)
    lado = max(400, min(800, altura_tela - 120))   # margem para barras e título
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(lado, lado)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"T1 - Inclusao de Ponto em Poligonos")
    glClearColor(0.08, 0.08, 0.10, 1.0)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutPassiveMotionFunc(motion)   # mouse solto
    glutMotionFunc(motion)          # mouse com botão apertado
    glutKeyboardFunc(keyboard)
    glutTimerFunc(100, tick, 0)

    try:
        glutMainLoop()
    except SystemExit:
        os._exit(0)


if __name__ == "__main__":
    main()
