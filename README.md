

A fully animated 3D Solar System simulation created as a **Computer Graphics Sessional Project** for the CSE department. It features all 8 planets orbiting the Sun with realistic lighting, Saturn's rings, Jupiter's rings, fog effects, and a star field — all rendered using OpenGL.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| PyOpenGL | OpenGL bindings for Python |
| GLUT | Window management and input handling |
| gluPerspective | 3D camera projection |
| gluLookAt | Camera positioning |

---

## Installation

### Step 1 — Make sure Python is installed
Download from [python.org](https://www.python.org/downloads/) if not already installed.
```bash
python --version
```

### Step 2 — Install PyOpenGL
```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### Step 3 — Install GLUT (if needed)

**Windows:**
```bash
pip install PyOpenGL PyOpenGL_accelerate
```
> If you get a GLUT DLL error, download `freeglut` from [freeglut.sourceforge.net](https://freeglut.sourceforge.net) and place `freeglut.dll` in the same folder as the script.




## ⌨️ Keyboard Controls

| Key | Action |
|---|---|
| `+` | Zoom In |
| `-` | Zoom Out |
| `f` | Speed Up |
| `s` | Slow Down |
| `l` | Toggle Lighting ON/OFF |
| `g` | Toggle Fog ON/OFF |
| `p` | Pause / Resume |
| `r` | Reset Camera & Speed |
| `ESC` | Exit |



## 🔧 OpenGL Features Implemented

- `GL_DEPTH_TEST` — correct 3D depth ordering
- `GL_SMOOTH` — smooth shading across surfaces
- `GL_LIGHTING` + `GL_LIGHT0` — positional light at Sun
- `GL_FOG` — linear distance fog
- `GL_BLEND` — transparency for Saturn and Jupiter rings
- `GL_COLOR_MATERIAL` — per-vertex color with lighting
- `GL_EMISSION` — Sun glows its own color regardless of lighting
- `glPushMatrix / glPopMatrix` — correct transformation hierarchy
- `gluPerspective` — 3D perspective projection
- `gluLookAt` — camera control



