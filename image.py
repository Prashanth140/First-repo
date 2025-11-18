# generate_tree_image.py
# Creates a simple stylized tree image and saves it to D:/Gitdemo/First-repo/image.jpg
# Requires: Pillow (pip install pillow)

from PIL import Image, ImageDraw
import os
import random
import math

OUT_PATH = r"D:/Gitdemo/First-repo/image.jpg"
W, H = 1200, 800

def ensure_dir(path):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def draw_sky_gradient(draw, w, h, top=(135, 206, 235), bottom=(255, 255, 255)):
    for y in range(h):
        t = y / (h - 1)
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def draw_trunk(draw, cx, ground_y, trunk_width, trunk_height):
    left = cx - trunk_width // 2
    right = cx + trunk_width // 2
    top = ground_y - trunk_height
    # trunk rectangle
    draw.rectangle([left, top, right, ground_y], fill=(101, 67, 33))
    # add some rings/texture
    for i in range(6):
        yy = top + int((i+1) * trunk_height / 7)
        draw.line([(left, yy), (right, yy)], fill=(120, 85, 51), width=1)

def draw_canopy(draw, cx, top_y, radius, leaf_colors):
    # draw layered clusters of leaves using circles
    n_clusters = 160
    for i in range(n_clusters):
        angle = random.uniform(0, 2*math.pi)
        r = random.gauss(radius*0.6, radius*0.3)
        rx = int(cx + math.cos(angle) * r * random.uniform(0.2, 1.0))
        ry = int(top_y + math.sin(angle) * r * random.uniform(0.2, 1.0))
        leaf_r = random.randint(int(radius*0.08), int(radius*0.2))
        color = random.choice(leaf_colors)
        bbox = [rx - leaf_r, ry - leaf_r, rx + leaf_r, ry + leaf_r]
        draw.ellipse(bbox, fill=color, outline=None)

def draw_ground(draw, w, h, ground_y):
    draw.rectangle([0, ground_y, w, h], fill=(98, 170, 85))
    # add simple grass blades
    for x in range(0, w, 6):
        blade_h = random.randint(6, 18)
        draw.line([(x, ground_y), (x + random.randint(-2, 2), ground_y - blade_h)], fill=(34, 139, 34))

def main():
    ensure_dir(OUT_PATH)
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # sky
    draw_sky_gradient(draw, W, H, top=(135, 206, 235), bottom=(255, 255, 255))

    # ground
    ground_y = int(H * 0.78)
    draw_ground(draw, W, H, ground_y)

    # tree position and size
    cx = W // 2
    trunk_height = int(H * 0.22)
    trunk_width = int(W * 0.06)
    draw_trunk(draw, cx, ground_y, trunk_width, trunk_height)

    # canopy
    canopy_top = ground_y - trunk_height - int(H * 0.05)
    canopy_radius = int(H * 0.25)
    leaf_colors = [
        (34, 139, 34), (46, 160, 44), (60, 179, 113), (50, 205, 50),
        (34, 139, 34), (24, 120, 20)
    ]
    # draw several layered canopies for depth
    for i, scale in enumerate([1.1, 0.95, 0.8]):
        draw_canopy(draw, cx + int(8 * i), canopy_top + int(10 * i), int(canopy_radius * scale), leaf_colors)

    # simple highlights (sunlit leaves)
    for _ in range(40):
        rx = random.randint(cx - canopy_radius//2, cx + canopy_radius//2)
        ry = random.randint(canopy_top - canopy_radius//6, canopy_top + canopy_radius//2)
        r = random.randint(6, 14)
        draw.ellipse([rx-r, ry-r, rx+r, ry+r], fill=(220, 255, 200, 128))

    # optionally resize slightly to add subtle anti-aliasing (kept original here)
    img.save(OUT_PATH, quality=90)
    print(f"Saved tree image to {OUT_PATH}")

if __name__ == "__main__":
    main()