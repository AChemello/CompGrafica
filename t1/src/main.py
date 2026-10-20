import signal
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *

sair = False


def pedir_saida(*_):
    global sair
    sair = True


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()


def keyboard(key, x, y):
    if key == b'\x1b':  # ESC
        glutLeaveMainLoop()


def tick(_):
    if sair:
        glutLeaveMainLoop()
        return
    glutTimerFunc(100, tick, 0)


def main():
    signal.signal(signal.SIGINT, pedir_saida)

    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b'T1 - Inclusao de ponto')

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(100, tick, 0)

    glutMainLoop()


if __name__ == '__main__':
    main()