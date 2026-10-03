"""Procedurally paints the mod's 16x16 textures. Re-run to regenerate: python3 tools/gen_textures.py"""
import math
import random
from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "src/main/resources/assets/mcflora/textures/block"
OUT.mkdir(parents=True, exist_ok=True)
N = 16


def new():
    return Image.new("RGBA", (N, N), (0, 0, 0, 0))


def clamp(v):
    return max(0, min(255, int(v)))


def shade(c, f):
    return tuple(clamp(ch * f) for ch in c[:3]) + (255,)


def mix(a, b, t):
    return tuple(clamp(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)


def put(im, x, y, c):
    x, y = int(round(x)), int(round(y))
    if 0 <= x < N and 0 <= y < N:
        im.putpixel((x, y), c if len(c) == 4 else c + (255,))


def get(im, x, y):
    return im.getpixel((x, y))


def line(im, x0, y0, x1, y1, c):
    steps = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
    for i in range(steps + 1):
        t = i / steps
        put(im, x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, c)


def save(im, name):
    im.save(OUT / f"{name}.png")


# --------------------------------------------------------------------------- lichens

def lichen(name, base, light, dark, seed):
    r = random.Random(seed)
    im = new()
    # crusty rosettes scattered over the face, with gaps showing the block behind
    for _ in range(6):
        cx, cy, rad = r.uniform(1, 15), r.uniform(1, 15), r.uniform(1.6, 3.4)
        for y in range(N):
            for x in range(N):
                d = math.hypot(x - cx, y - cy) + r.uniform(-0.6, 0.6)
                if d < rad:
                    if d > rad - 1.1:
                        c = light
                    elif r.random() < 0.18:
                        c = dark
                    else:
                        c = mix(base, light, r.uniform(0, 0.35))
                    put(im, x, y, c)
    # little isolated specks
    for _ in range(14):
        put(im, r.randrange(N), r.randrange(N), r.choice([base, light]))
    save(im, name)


lichen("silver_lichen", (168, 176, 168), (208, 214, 204), (126, 134, 130), 1)
lichen("black_lichen", (46, 45, 50), (78, 76, 82), (24, 23, 27), 2)
lichen("brown_lichen", (116, 86, 54), (150, 116, 76), (82, 58, 36), 3)
lichen("rust_lichen", (184, 96, 40), (220, 138, 62), (138, 64, 26), 4)


# --------------------------------------------------------------------------- old man's beard

def old_mans_beard():
    r = random.Random(5)
    im = new()
    pale = (172, 190, 152)
    for sx in [1, 3, 4, 6, 8, 9, 11, 13, 14]:
        x = sx + r.uniform(-0.3, 0.3)
        length = r.randint(9, 16)
        for y in range(length):
            x += r.uniform(-0.45, 0.45)
            c = mix(pale, (120, 140, 108), r.uniform(0, 0.5)) if y > 2 else mix(pale, (210, 220, 196), 0.4)
            put(im, x, y, c)
            if r.random() < 0.12:
                line(im, x, y, x + r.choice([-2, 2]), y + 2, shade(pale, 0.9))
    save(im, "old_mans_beard")


old_mans_beard()


# --------------------------------------------------------------------------- reindeer lichen

def reindeer_lichen():
    r = random.Random(6)
    im = new()
    base = (206, 210, 190)

    def branch(x, y, ang, length, depth):
        for _ in range(length):
            x += math.cos(ang) * 0.9
            y -= math.sin(ang) * 0.9
            put(im, x, y, mix(base, (150, 158, 134), r.uniform(0, 0.45)))
        if depth > 0:
            for da in (-0.55, 0.55):
                branch(x, y, ang + da + r.uniform(-0.2, 0.2), max(1, length - 1), depth - 1)
        else:
            put(im, x, y - 1, (232, 234, 222))

    for bx in (3, 6, 8, 10, 13):
        branch(bx, 15, math.pi / 2 + r.uniform(-0.3, 0.3), r.randint(3, 4), 2)
    save(im, "reindeer_lichen")


reindeer_lichen()


# --------------------------------------------------------------------------- moss blocks

def moss_block(name, base, accents, seed):
    r = random.Random(seed)
    im = new()
    for y in range(N):
        for x in range(N):
            put(im, x, y, shade(base, r.uniform(0.82, 1.12)))
    for color, count in accents:
        for _ in range(count):
            x, y = r.randrange(N), r.randrange(N)
            put(im, x, y, color)
            if r.random() < 0.5:
                put(im, x + r.choice([-1, 1]), y, shade(color, 0.9))
    save(im, name)


moss_block("frost_moss_block", (104, 146, 128),
           [((214, 232, 236), 26), ((150, 188, 176), 22), ((74, 108, 96), 18)], 7)
moss_block("sphagnum_moss_block", (112, 132, 58),
           [((156, 74, 58), 22), ((178, 168, 82), 18), ((76, 92, 40), 20)], 8)


# --------------------------------------------------------------------------- blades & grasses

def blades(im, r, count, top, color, lean=1.2, x_range=(1, 15)):
    for _ in range(count):
        x = r.uniform(*x_range)
        h = r.uniform(top[0], top[1])
        dx = r.uniform(-lean, lean)
        for i in range(int(16 - h)):
            t = i / max(1, 16 - h)
            put(im, x + dx * t * t, 15 - i, mix(color, shade(color, 1.3), t))


def cotton_grass():
    r = random.Random(9)
    green = (104, 130, 62)
    im = new()
    blades(im, r, 8, (0, 5), green, lean=2.5)
    save(im, "cotton_grass_bottom")
    im = new()
    blades(im, r, 5, (8, 12), green, lean=2.5)
    for sx in (3, 7, 10, 13):
        top = r.randint(2, 5)
        line(im, sx, 15, sx + r.choice([-1, 0, 1]), top + 2, (124, 128, 74))
        cx = sx + r.choice([-1, 0, 1])
        for dy in range(-2, 2):
            for dx in range(-1, 2):
                if abs(dx) + abs(dy + 0.5) < 2.6:
                    put(im, cx + dx, top + dy, mix((246, 246, 240), (214, 214, 206), r.random() * 0.6))
    save(im, "cotton_grass_top")


cotton_grass()


def arctic_poppy():
    im = new()
    stem = (92, 122, 56)
    line(im, 8, 15, 8, 8, stem)
    for x, y in [(6, 14), (5, 13), (10, 14), (11, 13), (7, 12)]:
        put(im, x, y, shade(stem, 1.15))
    yellow, deep = (246, 214, 52), (214, 160, 30)
    for y in range(3, 8):
        for x in range(5, 12):
            if (x - 8) ** 2 / 9 + (y - 5.5) ** 2 / 6 < 1:
                put(im, x, y, yellow if y < 6 else deep)
    put(im, 8, 6, (196, 122, 26))
    put(im, 8, 5, (236, 176, 40))
    save(im, "arctic_poppy")


arctic_poppy()


def fern_frond(im, r, x0, y0, ang, length, color, leaflet=2):
    x, y = x0, y0
    for i in range(length):
        x += math.cos(ang)
        y -= math.sin(ang)
        ang -= 0.07  # arch over
        put(im, x, y, shade(color, 0.85))
        if i > 0 and i % 1 == 0:
            span = max(1, leaflet - i // 4)
            for s in (-1, 1):
                nx, ny = -math.sin(ang) * s, -math.cos(ang) * s
                for k in range(1, span + 1):
                    put(im, x + nx * k, y + ny * k + 0.5 * k, mix(color, (150, 170, 70), r.uniform(0, 0.3)))


def bracken():
    r = random.Random(10)
    green = (88, 130, 48)
    im = new()
    for sx in (4, 8, 12):
        line(im, sx, 15, sx + r.choice([-1, 1]), 4, (110, 92, 50))
    fern_frond(im, r, 6, 9, math.radians(150), 6, green)
    fern_frond(im, r, 10, 8, math.radians(30), 6, green)
    save(im, "bracken_bottom")
    im = new()
    line(im, 8, 15, 8, 6, (110, 92, 50))
    fern_frond(im, r, 8, 5, math.radians(165), 8, green, 3)
    fern_frond(im, r, 8, 5, math.radians(15), 8, green, 3)
    fern_frond(im, r, 8, 9, math.radians(150), 7, shade(green, 1.1), 3)
    fern_frond(im, r, 8, 9, math.radians(30), 7, shade(green, 1.1), 3)
    fern_frond(im, r, 8, 6, math.radians(100), 5, shade(green, 1.15), 2)
    # a touch of autumn bronze on the tips
    for _ in range(5):
        x, y = r.randrange(N), r.randrange(8)
        if get(im, x, y)[3]:
            put(im, x, y, (156, 120, 52))
    save(im, "bracken_top")


bracken()


def lance_leaf(im, x0, y0, ang, length, width, fill, edge, mid=None):
    """Draws a broad pointed leaf from (x0, y0) heading towards `ang`."""
    for i in range(length):
        t = i / max(1, length - 1)
        cx, cy = x0 + math.cos(ang) * i, y0 - math.sin(ang) * i
        w = width * math.sin(math.pi * min(0.98, t * 0.9 + 0.08))
        nx, ny = -math.sin(ang), -math.cos(ang)
        steps = int(w * 2) + 1
        for k in range(-steps, steps + 1):
            f = k / 2
            if abs(f) > w:
                continue
            c = edge if abs(f) > w - 0.6 else fill
            put(im, cx + nx * f, cy + ny * f, c)
        if mid:
            put(im, cx, cy, mid)


def sasa():
    r = random.Random(11)
    fill, edge, mid = (64, 128, 44), (214, 210, 160), (48, 98, 34)
    im = new()
    for sx in (5, 8, 11):
        line(im, sx, 15, sx, 0, (120, 140, 66))
    lance_leaf(im, 8, 9, math.radians(200), 8, 1.6, fill, edge, mid)
    lance_leaf(im, 8, 6, math.radians(-20), 8, 1.6, fill, edge, mid)
    save(im, "sasa_bamboo_grass_bottom")
    im = new()
    line(im, 8, 15, 8, 5, (120, 140, 66))
    lance_leaf(im, 8, 6, math.radians(150), 8, 1.8, fill, edge, mid)
    lance_leaf(im, 8, 7, math.radians(25), 8, 1.8, fill, edge, mid)
    lance_leaf(im, 8, 10, math.radians(200), 7, 1.5, fill, edge, mid)
    lance_leaf(im, 8, 12, math.radians(-15), 7, 1.5, fill, edge, mid)
    save(im, "sasa_bamboo_grass_top")


sasa()


def red_spider_lily():
    r = random.Random(12)
    im = new()
    line(im, 8, 15, 8, 8, (86, 132, 54))
    red, deep = (214, 34, 40), (150, 18, 28)
    cx, cy = 8, 6
    for k in range(7):
        a = math.pi / 2 + (k - 3) * 0.55
        for i in range(1, 5):
            put(im, cx + math.cos(a) * i, cy - math.sin(a) * i * 0.7 + (i * i) * 0.12, red if i < 4 else deep)
    # long upswept stamens
    for k in range(6):
        a = math.pi / 2 + (k - 2.5) * 0.45
        x, y = cx, cy
        for i in range(6):
            x += math.cos(a) * 1.1
            y -= math.sin(a) * 1.1 - 0.18 * i
            put(im, x, y, (236, 70, 64))
    put(im, cx, cy, deep)
    save(im, "red_spider_lily")


red_spider_lily()


def japanese_iris():
    r = random.Random(13)
    leaf = (64, 118, 56)
    im = new()
    for sx, dx in ((4, -1.5), (6, -0.5), (8, 0.2), (10, 0.8), (12, 1.6)):
        line(im, sx, 15, sx + dx, 0, mix(leaf, (90, 150, 70), r.random() * 0.4))
    save(im, "japanese_iris_bottom")
    im = new()
    for sx, dx in ((4, -1.2), (6, -0.4), (11, 0.6)):
        line(im, sx, 15, sx + dx, 7, leaf)
    line(im, 8, 15, 8, 7, (82, 130, 60))
    purple, light, deep = (122, 66, 176), (176, 132, 220), (78, 38, 124)
    # three broad falls
    for a in (math.radians(200), math.radians(-20), math.radians(270)):
        for i in range(1, 5):
            for w in (-1, 0, 1):
                put(im, 8 + math.cos(a) * i - math.sin(a) * w * 0.8, 6 - math.sin(a) * i * 0.7 + math.cos(a) * w * 0.8,
                    purple if abs(w) < 1 else deep)
    # upright standards
    for x in (7, 8, 9):
        for y in range(2, 6):
            put(im, x, y, light if x == 8 else purple)
    put(im, 6, 7, (236, 200, 60))
    put(im, 10, 7, (236, 200, 60))
    put(im, 8, 9, (236, 200, 60))
    save(im, "japanese_iris_top")


japanese_iris()


def hydrangea(name, cols, seed):
    r = random.Random(seed)
    im = new()
    leaf = (52, 104, 48)
    lance_leaf(im, 8, 14, math.radians(160), 7, 1.6, leaf, shade(leaf, 0.8))
    lance_leaf(im, 8, 14, math.radians(20), 7, 1.6, leaf, shade(leaf, 0.8))
    line(im, 8, 15, 8, 9, (70, 110, 52))
    for y in range(1, 11):
        for x in range(1, 15):
            if (x - 7.5) ** 2 / 46 + (y - 6) ** 2 / 24 < 1:
                put(im, x, y, r.choice(cols[:2]))
    # four-petal florets
    for _ in range(9):
        x, y = r.randint(2, 13), r.randint(2, 9)
        if (x - 7.5) ** 2 / 46 + (y - 6) ** 2 / 24 < 0.8:
            c = cols[2]
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                put(im, x + dx, y + dy, c)
            put(im, x, y, cols[3])
    save(im, name)


hydrangea("blue_hydrangea", [(70, 112, 196), (92, 136, 214), (150, 182, 238), (236, 238, 250)], 14)
hydrangea("pink_hydrangea", [(206, 98, 150), (226, 128, 172), (246, 178, 206), (252, 236, 242)], 15)


def lotus_pad():
    r = random.Random(16)
    im = new()
    base = (70, 138, 64)
    for y in range(N):
        for x in range(N):
            d = math.hypot(x - 7.5, y - 7.5)
            a = math.atan2(y - 7.5, x - 7.5)
            if d < 7.6 and not (-0.25 < a < 0.25 and d > 1):
                c = shade(base, r.uniform(0.9, 1.08))
                if d > 6.6:
                    c = shade(base, 0.78)
                put(im, x, y, c)
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        for i in range(1, 7):
            put(im, 7.5 + math.cos(a) * i, 7.5 + math.sin(a) * i, (120, 176, 96))
    put(im, 7, 7, (160, 196, 110))
    put(im, 8, 8, (160, 196, 110))
    save(im, "lotus_pad")


lotus_pad()


def lotus_flower():
    im = new()
    pink, light, deep = (234, 140, 176), (250, 210, 226), (198, 82, 128)
    # cup of petals sitting low so it rests on the pad
    for y in range(6, 16):
        for x in range(2, 14):
            dx = abs(x - 7.5)
            if y >= 6 + dx * 0.9 - 2 and y < 16 - max(0, dx - 4) * 2:
                t = (y - 6) / 10
                c = mix(light, pink, t) if (int(x) % 3) else mix(pink, deep, t)
                put(im, x, y, c)
    # pointed petal tips
    for x, y in [(3, 7), (7, 4), (8, 4), (12, 7), (5, 5), (10, 5)]:
        put(im, x, y, light)
    put(im, 7, 9, (240, 210, 70))
    put(im, 8, 9, (240, 210, 70))
    save(im, "lotus_flower")


lotus_flower()


def split_leaf(im, cx, cy, rx, ry, base, hole_seed):
    r = random.Random(hole_seed)
    for y in range(N):
        for x in range(N):
            if (x - cx) ** 2 / rx ** 2 + (y - cy) ** 2 / ry ** 2 < 1:
                put(im, x, y, shade(base, r.uniform(0.92, 1.06)))
    # fenestrations: slits from the leaf edge towards the midrib
    for k in (-2, -1, 1, 2):
        # slit running from the rim in towards the midrib
        ex = cx + k * rx / 2.6
        for i in range(5):
            t = i / 4
            put(im, ex + (cx - ex) * t * 0.55, cy - ry * 0.85 + i * 0.9 * (1 if abs(k) == 1 else 1.3), (0, 0, 0, 0))
        # oval hole near the midrib
        if abs(k) == 1:
            put(im, cx + k * 1.5, cy + 1.5, (0, 0, 0, 0))
    line(im, cx, cy + ry - 1, cx, cy - ry + 1, shade(base, 0.72))


def monstera():
    base = (40, 118, 52)
    im = new()
    line(im, 6, 15, 5, 4, (70, 110, 50))
    line(im, 10, 15, 11, 6, (70, 110, 50))
    split_leaf(im, 7.5, 6, 6.5, 4.5, base, 17)
    save(im, "monstera_bottom")
    im = new()
    line(im, 8, 15, 8, 9, (70, 110, 50))
    split_leaf(im, 7.5, 7, 7.4, 5.8, shade(base, 1.1), 18)
    save(im, "monstera_top")


monstera()


def birds_nest_fern():
    im = new()
    fill, edge, mid = (108, 182, 56), (80, 146, 42), (52, 70, 36)
    for a in (110, 135, 160, 70, 45, 20, 90):
        lance_leaf(im, 8, 15, math.radians(a), 13 if a == 90 else 11, 1.4, fill, edge, mid)
    save(im, "birds_nest_fern")


birds_nest_fern()


def nepenthes():
    im = new()
    vine = (88, 128, 54)
    line(im, 8, 0, 7, 4, vine)
    line(im, 7, 4, 9, 7, vine)
    lance_leaf(im, 8, 2, math.radians(200), 5, 1.2, (96, 146, 58), (70, 112, 44))
    # pitcher
    body, spot, rim = (176, 50, 46), (112, 30, 34), (226, 160, 70)
    for y in range(9, 16):
        for x in range(5, 12):
            w = 3 if y > 11 else 2
            if abs(x - 8) <= w:
                put(im, x, y, spot if (x + y) % 4 == 0 else body)
    for x in range(6, 11):
        put(im, x, 8, rim)
    for x in range(8, 12):
        put(im, x, 7, (130, 152, 64))  # lid
    save(im, "nepenthes")


nepenthes()


def rafflesia():
    r = random.Random(19)
    im = new()
    petal, wart, core = (180, 52, 34), (236, 214, 198), (70, 26, 20)
    for y in range(N):
        for x in range(N):
            d = math.hypot(x - 7.5, y - 7.5)
            a = math.atan2(y - 7.5, x - 7.5)
            lobe = 6.2 + 1.6 * math.cos(5 * a)
            if d < lobe:
                put(im, x, y, shade(petal, r.uniform(0.88, 1.08)))
    for _ in range(22):
        x, y = r.randrange(N), r.randrange(N)
        if get(im, x, y)[3] and math.hypot(x - 7.5, y - 7.5) > 3.2:
            put(im, x, y, wart)
    for y in range(N):
        for x in range(N):
            d = math.hypot(x - 7.5, y - 7.5)
            if d < 3.2:
                put(im, x, y, (150, 40, 30) if d > 2.2 else core)
    save(im, "rafflesia")


rafflesia()
print("textures written to", OUT)
