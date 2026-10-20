import signal

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from geometry import generate_random_triangles
from acceleration import AABB, UniformGrid
from inclusion_tests import query
import visualization as vis

BOUNDS = (-50, 50, -50, 50)
SEED = 42
N_TRIANGLES = 200
CELL_SIZE = 10

triangles = generate_random_triangles(N_TRIANGLES, BOUNDS, seed=SEED)
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


# ---------- encerramento limpo ----------
def pedir_saida(*_):
    state["sair"] = True


def tick(_):
    if state["sair"]:
        glutLeaveMainLoop()
        return
    glutTimerFunc(100, tick, 0)


# ---------- desenho ----------
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
        f"Ponto: ({p[0]:.2f}, {p[1]:.2f})   Config: {modo}",
        f"Total: {stats.total_triangulos}  Cand.subdiv: {stats.candidatos_subdivisao}  "
        f"Cand.envelope: {stats.candidatos_envelope}",
        f"Testes detalhados: {stats.testes_detalhados}  Contidos: {len(stats.contidos)}  "
        f"Tempo: {stats.tempo_s * 1000:.3f} ms",
        f"Verificacao vs forca bruta: {'OK' if ok else 'DIVERGE!'}",
    ]
    y = BOUNDS[3] - 3
    for linha in linhas:
        vis.draw_text(BOUNDS[0] + 1, y, linha)
        y -= 3

    glutSwapBuffers()


# ---------- entrada ----------
def motion(x, y):
    w, h = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
    wx = BOUNDS[0] + (x / w) * (BOUNDS[1] - BOUNDS[0])
    wy = BOUNDS[3] - (y / h) * (BOUNDS[3] - BOUNDS[2])  # Y da janela é invertido
    state["point"] = (wx, wy)
    glutPostRedisplay()


def keyboard(key, x, y):
    if key == b'\x1b':  # ESC
        glutLeaveMainLoop()
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
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(*BOUNDS)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    signal.signal(signal.SIGINT, pedir_saida)

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 800)
    glutCreateWindow(b"T1 - Inclusao de Ponto em Poligonos")
    glClearColor(0.08, 0.08, 0.10, 1.0)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutPassiveMotionFunc(motion)   # mouse solto
    glutMotionFunc(motion)          # mouse com botão apertado
    glutKeyboardFunc(keyboard)
    glutTimerFunc(100, tick, 0)

    glutMainLoop()


if __name__ == "__main__":
    main()