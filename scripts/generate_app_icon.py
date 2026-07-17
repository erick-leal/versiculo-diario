"""Genera los assets de icono de la app (icon, splash, adaptive icon de
Android) coherentes con la paleta del sistema de diseno. Glifo: libro
abierto estilizado, que tambien se lee como una "V" (Versiculo).
Uso unico - no se re-corre automaticamente.
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw

OUT_DIR = Path(__file__).resolve().parent.parent / "apps/mobile/assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CREAM = (251, 250, 247)
GOLD_DEEP = (58, 47, 29)
GOLD_LIGHT = (212, 175, 55)
NEAR_BLACK = (20, 18, 15)

random.seed(7)


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return a + (b - a) * t


def dither(v):
    noisy = v + random.uniform(-1.2, 1.2)
    return max(0, min(255, round(noisy)))


def radial_gradient(size, center_color, edge_color):
    img = Image.new("RGB", (size, size))
    px = img.load()
    cx, cy = size / 2, size / 2
    max_dist = (2 * (size / 2) ** 2) ** 0.5
    for y in range(size):
        for x in range(size):
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            t = min(1.0, dist / max_dist)
            px[x, y] = tuple(dither(lerp(center_color[i], edge_color[i], t)) for i in range(3))
    return img


def draw_book_glyph(draw, cx, cy, half_width, height, color):
    """Dos paginas anchas abajo, que se juntan arriba en el lomo -
    silueta clasica de libro abierto visto de frente/arriba."""
    spine_x = cx
    spine_y = cy - height / 2
    base_y = cy + height / 2
    spine_gap = half_width * 0.06

    # Pagina izquierda
    draw.polygon(
        [
            (spine_x - spine_gap, spine_y),
            (spine_x - half_width, base_y - height * 0.08),
            (spine_x - half_width * 0.82, base_y),
            (spine_x - spine_gap * 2, base_y - height * 0.04),
        ],
        fill=color,
    )
    # Pagina derecha (espejo)
    draw.polygon(
        [
            (spine_x + spine_gap, spine_y),
            (spine_x + half_width, base_y - height * 0.08),
            (spine_x + half_width * 0.82, base_y),
            (spine_x + spine_gap * 2, base_y - height * 0.04),
        ],
        fill=color,
    )


SIZE = 1024

# --- icon.png: fondo degradado dorado + glifo crema, ocupa todo el cuadrado ---
icon = radial_gradient(SIZE, hex_to_rgb("#4A3B22"), hex_to_rgb("#1E1710"))
draw = ImageDraw.Draw(icon)
draw_book_glyph(draw, SIZE / 2, SIZE / 2 + SIZE * 0.02, SIZE * 0.28, SIZE * 0.42, CREAM)
icon.save(OUT_DIR / "icon.png")

# --- android-icon-background.png: solo el fondo degradado ---
bg = radial_gradient(SIZE, hex_to_rgb("#4A3B22"), hex_to_rgb("#1E1710"))
bg.save(OUT_DIR / "android-icon-background.png")

# --- android-icon-foreground.png: solo el glifo, transparente, dentro de la
# zona segura (Android recorta ~33% de los bordes en algunos launchers) ---
fg = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw_fg = ImageDraw.Draw(fg)
draw_book_glyph(draw_fg, SIZE / 2, SIZE / 2 + SIZE * 0.02, SIZE * 0.18, SIZE * 0.27, CREAM + (255,))
fg.save(OUT_DIR / "android-icon-foreground.png")

# --- android-icon-monochrome.png: mismo glifo, blanco solido (Android 13+ themed icons) ---
mono = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw_mono = ImageDraw.Draw(mono)
draw_book_glyph(
    draw_mono, SIZE / 2, SIZE / 2 + SIZE * 0.02, SIZE * 0.18, SIZE * 0.27, (255, 255, 255, 255)
)
mono.save(OUT_DIR / "android-icon-monochrome.png")

# --- splash-icon.png: glifo solo, transparente, mas chico (se centra sobre
# un fondo solido definido en app.json) ---
splash = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw_splash = ImageDraw.Draw(splash)
draw_book_glyph(
    draw_splash, SIZE / 2, SIZE / 2, SIZE * 0.16, SIZE * 0.24, hex_to_rgb("#B8860B") + (255,)
)
splash.save(OUT_DIR / "splash-icon.png")

# --- favicon.png: version chica para web ---
favicon_size = 196
favicon = radial_gradient(favicon_size, hex_to_rgb("#4A3B22"), hex_to_rgb("#1E1710"))
draw_fav = ImageDraw.Draw(favicon)
draw_book_glyph(
    draw_fav,
    favicon_size / 2,
    favicon_size / 2 + favicon_size * 0.02,
    favicon_size * 0.28,
    favicon_size * 0.42,
    CREAM,
)
favicon.save(OUT_DIR / "favicon.png")

print("Assets generados en", OUT_DIR)
