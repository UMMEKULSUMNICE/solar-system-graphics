
import sys
import math
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *




zoom         = -65.0   
camera_angle = 28.0    

speed  = 1.0
paused = False

lighting_on = True
fog_on      = True

# Orbit angles 
angle_mercury = 0.0
angle_venus   = 0.0
angle_earth   = 0.0
angle_mars    = 0.0
angle_jupiter = 0.0
angle_saturn  = 0.0
angle_uranus  = 0.0
angle_neptune = 0.0

# Self-rotation angles
rot_mercury = 0.0
rot_venus   = 0.0
rot_earth   = 0.0
rot_mars    = 0.0
rot_jupiter = 0.0
rot_saturn  = 0.0
rot_uranus  = 0.0
rot_neptune = 0.0

stars = []  



PLANETS = {
    "mercury": dict(orbit_r=8,  size=0.35, orbit_spd=0.80, rot_spd=0.30, color=(0.72, 0.70, 0.68)),
    "venus"  : dict(orbit_r=11, size=0.85, orbit_spd=0.50, rot_spd=0.08, color=(0.90, 0.78, 0.50)),
    "earth"  : dict(orbit_r=15, size=0.90, orbit_spd=0.30, rot_spd=1.00, color=(0.22, 0.46, 0.82)),
    "mars"   : dict(orbit_r=19, size=0.55, orbit_spd=0.18, rot_spd=0.95, color=(0.76, 0.30, 0.10)),
    "jupiter": dict(orbit_r=28, size=2.20, orbit_spd=0.06, rot_spd=2.40, color=(0.76, 0.60, 0.42)),
    "saturn" : dict(orbit_r=37, size=1.80, orbit_spd=0.03, rot_spd=2.20, color=(0.88, 0.80, 0.52)),
    "uranus" : dict(orbit_r=45, size=1.20, orbit_spd=0.015,rot_spd=1.40, color=(0.48, 0.82, 0.88)),
    "neptune": dict(orbit_r=52, size=1.15, orbit_spd=0.008,rot_spd=1.30, color=(0.22, 0.38, 0.88)),
}



def init():
    global stars

    glClearColor(0.0, 0.0, 0.0, 1.0)   
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    setup_lighting()
    setup_fog()

    # 150 tiny realistic stars
    random.seed(77)
    for _ in range(150):
        theta = random.uniform(0.0, 2.0 * math.pi)
        phi   = random.uniform(0.0, math.pi)
        r     = random.uniform(90, 135)
        x = r * math.sin(phi) * math.cos(theta)
        y = r * math.sin(phi) * math.sin(theta)
        z = r * math.cos(phi)
        
        kind = random.random()
        if kind < 0.60:
            col = (1.0, 1.0, 1.0)              
        elif kind < 0.80:
            col = (0.82, 0.88, 1.0)           
        else:
            col = (1.0, 0.94, 0.82)            
        b = random.uniform(0.55, 1.0)          
        stars.append((x, y, z, col[0]*b, col[1]*b, col[2]*b))


def setup_lighting():
    """Positional light placed at the Sun (world origin)."""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.04, 0.04, 0.04, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [1.0,  0.92, 0.75, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0,  1.0,  1.0,  1.0])

    glMaterialfv(GL_FRONT, GL_SPECULAR,  [0.35, 0.35, 0.35, 1.0])
    glMaterialf (GL_FRONT, GL_SHININESS, 40.0)


def setup_fog():
    """Gentle linear fog to fade out distant orbits."""
    glEnable(GL_FOG)
    glFogi (GL_FOG_MODE,  GL_LINEAR)
    glFogfv(GL_FOG_COLOR, [0.0, 0.0, 0.0, 1.0])
    glFogf (GL_FOG_START, 60.0)
    glFogf (GL_FOG_END,   140.0)



def draw_stars():
    """
    Render 150 stars as single 1-pixel points.
    Lighting and fog are OFF so they always appear crisp and bright.
    """
    glDisable(GL_LIGHTING)
    glDisable(GL_FOG)
    glPointSize(1.0)          

    glBegin(GL_POINTS)
    for (x, y, z, r, g, b) in stars:
        glColor3f(r, g, b)
        glVertex3f(x, y, z)
    glEnd()

    if lighting_on:
        glEnable(GL_LIGHTING)
    if fog_on:
        glEnable(GL_FOG)


def draw_orbit_path(radius):
    """Faint dotted-style orbit guide on the XZ plane."""
    glDisable(GL_LIGHTING)
    glColor4f(0.30, 0.30, 0.40, 0.22)
    glLineWidth(1.0)
    glBegin(GL_LINE_LOOP)
    for i in range(128):
        a = 2.0 * math.pi * i / 128
        glVertex3f(radius * math.cos(a), 0.0, radius * math.sin(a))
    glEnd()
    if lighting_on:
        glEnable(GL_LIGHTING)


def draw_sun():
    
    glDisable(GL_LIGHTING)

    
    glColor4f(0.88, 0.35, 0.00, 0.18)
    glutSolidSphere(4.6, 40, 40)

    
    glColor4f(1.00, 0.42, 0.00, 0.85)
    glutSolidSphere(3.9, 40, 40)

    
    glColor3f(1.00, 0.55, 0.10)
    glutSolidSphere(3.3, 48, 48)

    
    glColor3f(1.00, 0.78, 0.28)
    glutSolidSphere(2.5, 48, 48)

    if lighting_on:
        glEnable(GL_LIGHTING)


def draw_planet(color, size):
    glColor3f(*color)
    glutSolidSphere(size, 36, 36)


def draw_saturn_ring(planet_size):
    """
    Saturn's ring: 3 concentric torus bands, tilted 27°.
    Wide, flat (thin tube radius), semi-transparent.
    """
    glPushMatrix()
    glRotatef(27.0, 1.0, 0.0, 0.2)
    glDisable(GL_CULL_FACE)

   
    glColor4f(0.78, 0.70, 0.48, 0.70)
    glutSolidTorus(0.13, planet_size + 1.1, 4, 90)

   
    glColor4f(0.86, 0.78, 0.54, 0.50)
    glutSolidTorus(0.20, planet_size + 1.9, 4, 90)

    
    glColor4f(0.78, 0.70, 0.48, 0.28)
    glutSolidTorus(0.16, planet_size + 2.6, 4, 90)

    glEnable(GL_CULL_FACE)
    glPopMatrix()


def draw_jupiter_ring(planet_size):
    """
    Jupiter's ring: extremely faint, flat, thin — nearly invisible.
    Two gossamer bands with very low alpha (~0.12-0.18).
    No significant tilt (equatorial, ~3° actual inclination).
    """
    glPushMatrix()
    glRotatef(3.0, 1.0, 0.0, 0.0)   
    glDisable(GL_CULL_FACE)

   
    glColor4f(0.60, 0.50, 0.35, 0.18)
    glutSolidTorus(0.07, planet_size + 0.9, 3, 90)

    
    glColor4f(0.55, 0.46, 0.32, 0.10)
    glutSolidTorus(0.10, planet_size + 1.5, 3, 90)

    glEnable(GL_CULL_FACE)
    glPopMatrix()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

   
    dist  = -zoom
    eye_y = dist * math.sin(math.radians(camera_angle))
    eye_z = dist * math.cos(math.radians(camera_angle))
    gluLookAt(0.0, eye_y, eye_z,
              0.0, 0.0,   0.0,
              0.0, 1.0,   0.0)

    
    if lighting_on:
        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 0.0, 1.0])

    draw_stars()

    glPushMatrix()
    draw_sun()
    glPopMatrix()

    for p in PLANETS.values():
        draw_orbit_path(p["orbit_r"])

    # All planets
    _render_planet("mercury", angle_mercury, rot_mercury)
    _render_planet("venus",   angle_venus,   rot_venus)
    _render_planet("earth",   angle_earth,   rot_earth)
    _render_planet("mars",    angle_mars,    rot_mars)
    _render_jupiter()
    _render_saturn()
    _render_planet("uranus",  angle_uranus,  rot_uranus)
    _render_planet("neptune", angle_neptune, rot_neptune)

    glutSwapBuffers()


def _render_planet(name, orbit_angle, self_rot):
    p = PLANETS[name]
    glPushMatrix()
    glRotatef(orbit_angle, 0.0, 1.0, 0.0)  
    glTranslatef(p["orbit_r"], 0.0, 0.0)    
    glRotatef(self_rot, 0.08, 1.0, 0.05)    
    draw_planet(p["color"], p["size"])
    glPopMatrix()


def _render_jupiter():
    p = PLANETS["jupiter"]
    glPushMatrix()
    glRotatef(angle_jupiter, 0.0, 1.0, 0.0)
    glTranslatef(p["orbit_r"], 0.0, 0.0)
    glRotatef(rot_jupiter, 0.05, 1.0, 0.05)
    draw_planet(p["color"], p["size"])
    draw_jupiter_ring(p["size"])
    glPopMatrix()


def _render_saturn():
    p = PLANETS["saturn"]
    glPushMatrix()
    glRotatef(angle_saturn, 0.0, 1.0, 0.0)
    glTranslatef(p["orbit_r"], 0.0, 0.0)
    glRotatef(rot_saturn, 0.08, 1.0, 0.05)
    draw_planet(p["color"], p["size"])
    draw_saturn_ring(p["size"])
    glPopMatrix()


def update(value):
    global angle_mercury, angle_venus,   angle_earth,   angle_mars
    global angle_jupiter, angle_saturn,  angle_uranus,  angle_neptune
    global rot_mercury,   rot_venus,     rot_earth,     rot_mars
    global rot_jupiter,   rot_saturn,    rot_uranus,    rot_neptune

    if not paused:
        dt = speed

        angle_mercury = (angle_mercury + PLANETS["mercury"]["orbit_spd"] * dt) % 360
        angle_venus   = (angle_venus   + PLANETS["venus"]  ["orbit_spd"] * dt) % 360
        angle_earth   = (angle_earth   + PLANETS["earth"]  ["orbit_spd"] * dt) % 360
        angle_mars    = (angle_mars    + PLANETS["mars"]   ["orbit_spd"] * dt) % 360
        angle_jupiter = (angle_jupiter + PLANETS["jupiter"]["orbit_spd"] * dt) % 360
        angle_saturn  = (angle_saturn  + PLANETS["saturn"] ["orbit_spd"] * dt) % 360
        angle_uranus  = (angle_uranus  + PLANETS["uranus"] ["orbit_spd"] * dt) % 360
        angle_neptune = (angle_neptune + PLANETS["neptune"]["orbit_spd"] * dt) % 360

        rot_mercury = (rot_mercury + PLANETS["mercury"]["rot_spd"] * dt) % 360
        rot_venus   = (rot_venus   + PLANETS["venus"]  ["rot_spd"] * dt) % 360
        rot_earth   = (rot_earth   + PLANETS["earth"]  ["rot_spd"] * dt) % 360
        rot_mars    = (rot_mars    + PLANETS["mars"]   ["rot_spd"] * dt) % 360
        rot_jupiter = (rot_jupiter + PLANETS["jupiter"]["rot_spd"] * dt) % 360
        rot_saturn  = (rot_saturn  + PLANETS["saturn"] ["rot_spd"] * dt) % 360
        rot_uranus  = (rot_uranus  + PLANETS["uranus"] ["rot_spd"] * dt) % 360
        rot_neptune = (rot_neptune + PLANETS["neptune"]["rot_spd"] * dt) % 360

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


#  RESHAPE

def reshape(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w / h, 0.5, 350.0)
    glMatrixMode(GL_MODELVIEW)


#  KEYBOARD

def keyboard(key, x, y):
    global zoom, speed, lighting_on, fog_on, paused

    if isinstance(key, bytes):
        key = key.decode("utf-8")

    if key in ('+', '='):
        zoom = min(zoom + 3.0, -15.0)
        print(f"[Zoom] {zoom:.1f}")
    elif key in ('-', '_'):
        zoom = max(zoom - 3.0, -160.0)
        print(f"[Zoom] {zoom:.1f}")
    elif key == 'f':
        speed = min(speed + 0.2, 10.0)
        print(f"[Speed] {speed:.2f}")
    elif key == 's':
        speed = max(speed - 0.2, 0.1)
        print(f"[Speed] {speed:.2f}")
    elif key == 'l':
        lighting_on = not lighting_on
        (glEnable if lighting_on else glDisable)(GL_LIGHTING)
        print(f"[Lighting] {'ON' if lighting_on else 'OFF'}")
    elif key == 'g':
        fog_on = not fog_on
        (glEnable if fog_on else glDisable)(GL_FOG)
        print(f"[Fog] {'ON' if fog_on else 'OFF'}")
    elif key == 'p':
        paused = not paused
        print(f"[Sim] {'PAUSED' if paused else 'RUNNING'}")
    elif key == 'r':
        zoom  = -65.0
        speed = 1.0
        print("[Reset] Default view restored")
    elif key == '\x1b':
        print("Goodbye! 🚀")
        sys.exit(0)

    glutPostRedisplay()



def main():
    print("╔══════════════════════════════════════════════╗")
    print("║  3D Solar System Simulation  v2 — Realistic  ║")
    print("╠══════════════════════════════════════════════╣")
    print("║  +/-  Zoom In/Out    f/s  Speed Up/Down     ║")
    print("║  l  Lighting toggle  g  Fog toggle           ║")
    print("║  p  Pause/Resume     r  Reset    ESC  Quit  ║")
    print("╚══════════════════════════════════════════════╝")

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1100, 720)
    glutInitWindowPosition(80, 40)
    glutCreateWindow(b"3D Solar System_Realistic v2")

    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, update, 0)

    glutMainLoop()


if __name__ == "__main__":
    main()
