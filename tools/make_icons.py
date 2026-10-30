#!/usr/bin/env python3
"""Generate add-on icon/logo (shopping cart on green background)."""
from PIL import Image, ImageDraw

GREEN = (5, 150, 105)
WHITE = (255, 255, 255)


def draw_icon(size):
    S = 8  # supersampling
    n = size * S
    img = Image.new("RGB", (n, n), GREEN)
    d = ImageDraw.Draw(img)

    # cart body (basket)
    x0, y0 = n * 0.22, n * 0.36
    x1, y1 = n * 0.78, n * 0.64
    d.polygon([(x0, y0), (x1, y0), (x1 - n * 0.06, y1), (x0 + n * 0.06, y1)], fill=WHITE)

    # handle
    d.line([(n * 0.12, n * 0.24), (n * 0.22, n * 0.24), (x0 + n * 0.02, y0)],
           fill=WHITE, width=int(n * 0.045), joint="curve")

    # wheels
    r = n * 0.055
    for cx in (n * 0.36, n * 0.68):
        d.ellipse([cx - r, n * 0.75 - r, cx + r, n * 0.75 + r], fill=WHITE)

    # basket slats
    for f in (0.34, 0.5, 0.66):
        d.line([(n * f, y0 + n * 0.03), (n * f, y1 - n * 0.03)],
               fill=GREEN, width=int(n * 0.018))

    resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS", 1)
    return img.resize((size, size), resample)


draw_icon(128).save("addon/icon.png")
draw_icon(512).save("addon/logo.png")
print("addon/icon.png (128), addon/logo.png (512)")
