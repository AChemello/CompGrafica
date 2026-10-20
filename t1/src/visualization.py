import math

from OpenGL.GL import *
from OpenGL.GLUT import *


def draw_triangle(tri, color):
    glColor3f(*color)
    glBegin(GL_TRIANGLES)
    glVertex2f(*tri.a)
    glVertex2f(*tri.b)
    glVertex2f(*tri.c)
    glEnd()
    glColor3f(color[0] * 0.5, color[1] * 0.5, color[2] * 0.5)  # contorno mais escuro
    glBegin(GL_LINE_LOOP)
    glVertex2f(*tri.a)
    glVertex2f(*tri.b)
    glVertex2f(*tri.c)
    glEnd()


def draw_aabb(box, color=(0.0, 0.7, 0.0)):
    glColor3f(*color)
    glBegin(GL_LINE_LOOP)
    glVertex2f(box.min_x, box.min_y)
    glVertex2f(box.max_x, box.min_y)
    glVertex2f(box.max_x, box.max_y)
    glVertex2f(box.min_x, box.max_y)
    glEnd()


def draw_point(p, color=(1.0, 1.0, 1.0), size=8.0):
    glPointSize(size)
    glColor3f(*color)
    glBegin(GL_POINTS)
    glVertex2f(*p)
    glEnd()


def draw_grid(cell_size, bounds, color=(0.25, 0.25, 0.32)):
    xmin, xmax, ymin, ymax = bounds
    glColor3f(*color)
    glBegin(GL_LINES)
    x = math.floor(xmin / cell_size) * cell_size
    while x <= xmax:
        glVertex2f(x, ymin); glVertex2f(x, ymax)
        x += cell_size
    y = math.floor(ymin / cell_size) * cell_size
    while y <= ymax:
        glVertex2f(xmin, y); glVertex2f(xmax, y)
        y += cell_size
    glEnd()


def draw_cell(cell, cell_size, color=(1.0, 1.0, 0.0)):
    cx, cy = cell
    x0, y0 = cx * cell_size, cy * cell_size
    glColor3f(*color)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x0, y0); glVertex2f(x0 + cell_size, y0)
    glVertex2f(x0 + cell_size, y0 + cell_size); glVertex2f(x0, y0 + cell_size)
    glEnd()


def draw_text(x, y, text, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(ch)) # type: ignore

def draw_text_px(x, y, text, color=(1.0, 1.0, 1.0)):
    """Texto em pixels da janela (origem no canto inferior esquerdo)."""
    glColor3f(*color)
    glWindowPos2i(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(ch))  # type: ignore