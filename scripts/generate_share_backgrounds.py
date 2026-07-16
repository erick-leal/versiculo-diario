"""Genera 3 fondos degradados para la funcion de compartir, coherentes con
la paleta del sistema de diseno (docs/design-system.md). Uso unico hasta que
el panel admin (Fase 9) permita subir fondos reales via QuoteImages.
"""

import random

from pathlib import Path

from PIL import Image

WIDTH, HEIGHT = 1080, 1920
OUT_DIR = Path(__file__).resolve().parent.parent / "apps/mobile/assets/share-backgrounds"
OUT_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)


def hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def dither(value: float) -> int:
    # Ruido +/-1.5 antes de truncar a entero: rompe el banding visible en
    # degradados suaves de 8 bits (el ojo es muy sensible a esto en tonos oscuros).
    noisy = value + random.uniform(-1.5, 1.5)
    return max(0, min(255, round(noisy)))


def vertical_gradient(top: str, bottom: str) -> Image.Image:
    top_rgb = hex_to_rgb(top)
    bottom_rgb = hex_to_rgb(bottom)
    img = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = img.load()
    for y in range(HEIGHT):
        t = y / HEIGHT
        row_float = tuple(lerp(top_rgb[i], bottom_rgb[i], t) for i in range(3))
        for x in range(WIDTH):
            pixels[x, y] = tuple(dither(c) for c in row_float)
    return img


def add_radial_glow(img: Image.Image, color: str, strength: float, center_y_ratio: float) -> Image.Image:
    glow_rgb = hex_to_rgb(color)
    cx, cy = WIDTH / 2, HEIGHT * center_y_ratio
    max_dist = (WIDTH**2 + HEIGHT**2) ** 0.5 / 2
    pixels = img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            t = max(0.0, 1 - dist / max_dist) * strength
            if t <= 0:
                continue
            r, g, b = pixels[x, y]
            pixels[x, y] = (
                dither(lerp(r, glow_rgb[0], t)),
                dither(lerp(g, glow_rgb[1], t)),
                dither(lerp(b, glow_rgb[2], t)),
            )
    return img


cream = vertical_gradient("#FBFAF7", "#EDE6D6")
cream.save(OUT_DIR / "cream.jpg", quality=88)

charcoal = vertical_gradient("#1E1B16", "#0D0B08")
charcoal = add_radial_glow(charcoal, "#B8860B", strength=0.12, center_y_ratio=0.38)
charcoal.save(OUT_DIR / "charcoal.jpg", quality=88)

gold = vertical_gradient("#3A2F1D", "#14120F")
gold = add_radial_glow(gold, "#D4AF37", strength=0.22, center_y_ratio=0.32)
gold.save(OUT_DIR / "gold.jpg", quality=88)

print(f"Generados en {OUT_DIR}")
