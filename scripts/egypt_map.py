import warnings, numpy as np, matplotlib
warnings.filterwarnings("ignore")
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
from matplotlib.patches import Rectangle, Polygon as MPoly, Circle
import geopandas as gpd
from shapely.geometry import LineString, box, Point
from shapely.ops import unary_union
import sys

OUT = sys.argv[1]
W, E, S, N = 26.3, 35.6, 21.6, 31.95
INK, RED, PAPER, SEA = "#3d2b1a", "#9b2d1f", "#f0e3c2", "#e3d3a8"
F = "FreeSerif"
plt.rcParams["font.family"] = F

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
land = unary_union(world.geometry.values).intersection(box(W - 3, S - 3, E + 3, N + 3))
frame = box(W, S, E, N)
sea = frame.difference(land)

fig = plt.figure(figsize=(8, 9.8), dpi=200, facecolor=PAPER)
ax = fig.add_axes([0.055, 0.045, 0.89, 0.91])
ax.set_xlim(W, E); ax.set_ylim(S, N)
ax.set_aspect(1 / np.cos(np.radians(27)))
ax.set_facecolor(SEA)
for s in ax.spines.values():
    s.set_color(INK); s.set_linewidth(2.2)
ax.set_xticks([]); ax.set_yticks([])

def polys(g):
    return [g] if g.geom_type == "Polygon" else list(getattr(g, "geoms", []))

def fill(g, **kw):
    for p in polys(g):
        if p.geom_type != "Polygon" or p.is_empty:
            continue
        ax.add_patch(MPoly(np.array(p.exterior.coords), closed=True, **kw))

def line(g, **kw):
    gs = [g] if g.geom_type in ("LineString", "LinearRing") else list(getattr(g, "geoms", []))
    for l in gs:
        if l.geom_type in ("LineString", "LinearRing") and not l.is_empty:
            x, y = l.xy; ax.plot(x, y, solid_capstyle="round", **kw)

# Coastal ripple lines in the sea (old engraving style)
for i, d in enumerate([0.07, 0.15, 0.25, 0.37, 0.52]):
    ring = land.buffer(d).boundary.intersection(sea)
    line(ring, color=INK, lw=0.55 - i * 0.08, alpha=0.55 - i * 0.09, zorder=2)

fill(land.intersection(frame.buffer(0.5)), facecolor=PAPER, edgecolor="none", zorder=3)

# Desert stipple
rng = np.random.default_rng(7)
pts = np.column_stack([rng.uniform(W, E, 9000), rng.uniform(S, N, 9000)])
landp = land.intersection(frame)
from shapely import contains_xy
mask = contains_xy(landp, pts[:, 0], pts[:, 1])
ax.scatter(pts[mask, 0], pts[mask, 1], s=0.5, color=INK, alpha=0.18, lw=0, zorder=3.5)

line(land.boundary.intersection(frame), color=INK, lw=1.3, zorder=6)

# The Nile
main = [(31.20, 21.6), (31.33, 21.8), (31.65, 22.34), (32.0, 22.55), (32.25, 22.72), (32.45, 23.0), (32.86, 23.55), (32.88, 23.97), (32.90, 24.09),
        (32.94, 24.47), (32.88, 24.98), (32.70, 25.15), (32.56, 25.29), (32.52, 25.50), (32.64, 25.69), (32.75, 25.95), (32.72, 26.17),
        (32.45, 26.13), (32.25, 26.05), (31.95, 26.25), (31.70, 26.56), (31.42, 26.90), (31.18, 27.18), (30.90, 27.55), (30.76, 28.10),
        (30.80, 28.50), (31.10, 29.07), (31.22, 29.50), (31.26, 29.85), (31.23, 30.04), (31.13, 30.20)]
ros = [(31.13, 30.20), (30.95, 30.45), (30.75, 30.80), (30.55, 31.05), (30.42, 31.40), (30.37, 31.50)]
dam = [(31.13, 30.20), (31.18, 30.46), (31.26, 30.72), (31.38, 31.04), (31.62, 31.25), (31.81, 31.42), (31.84, 31.53)]
nile = [LineString(main), LineString(ros), LineString(dam)]
valley = unary_union([LineString(main).buffer(0.13), LineString(ros).buffer(0.0)])
delta = MPoly([(31.13, 30.20), (30.95, 30.45), (30.6, 30.95), (30.37, 31.50), (30.9, 31.55), (31.4, 31.52), (31.84, 31.53), (31.62, 31.25), (31.38, 31.04), (31.26, 30.72), (31.18, 30.46)], closed=True)
fill(valley.intersection(land), facecolor="#b9b98a", edgecolor="none", alpha=0.55, zorder=4)
from shapely.geometry import Polygon as SP
fill(SP(delta.get_xy()).intersection(land), facecolor="#b9b98a", edgecolor="none", alpha=0.55, zorder=4)
for l in nile:
    line(l.intersection(land), color="#2f4a5c", lw=1.9, zorder=7)

halo = [pe.withStroke(linewidth=2.6, foreground=PAPER)]

def label(x, y, t, size=10, style="normal", color=INK, ha="center", sp=0, rot=0, weight="normal", z=9):
    if sp:
        t = (" " * sp).join(t)
    ax.text(x, y, t, fontsize=size, style=style, color=color, ha=ha, va="center", rotation=rot, weight=weight,
            path_effects=halo, zorder=z)

# Regions and seas
label(28.6, 31.72, "MARE MEDITERRANEUM", 11.5, "italic", sp=0)
label(34.95, 26.6, "MARE RUBRUM", 11, "italic", rot=-58)
label(28.2, 28.6, "LIBYAN DESERT", 9.5, sp=1, color="#6b5536")
label(32.45, 27.7, "EASTERN DESERT", 9.5, sp=1, color="#6b5536", rot=-58)
label(33.9, 29.35, "SINAI", 9.5, sp=1, color="#6b5536")
label(29.3, 30.55, "LOWER EGYPT", 12, sp=1, weight="bold")
label(29.75, 26.0, "UPPER EGYPT", 12, sp=1, weight="bold")
label(30.4, 22.2, "NUBIA", 12, sp=1, weight="bold")
label(30.2, 27.55, "The Nile", 11, "italic", color="#2f4a5c", rot=-62)

# Places in the post: (lon, lat, name, old name, side, visited)
places = [
    (30.42, 31.40, "Rosetta", "Rashid", "r", True),
    (31.24, 30.05, "Cairo · Giza", "", "r", True),
    (31.24, 29.84, "Memphis · Saqqara · Dahshur", "", "l", True),
    (32.64, 25.70, "Luxor · Karnak", "Thebes", "r", True),
    (32.55, 25.29, "Esna", "Latopolis", "l", True),
    (32.87, 24.98, "Edfu", "Apollinopolis Magna", "r", True),
    (32.95, 24.47, "Kom Ombo", "Ombos", "r", True),
    (32.89, 24.08, "Aswan · Philae", "Syene", "r", True),
    (31.63, 22.34, "Abu Simbel", "", "l", True),
]
for x, y, n, old, side, v in places:
    if v:
        ax.add_patch(Circle((x, y), 0.075, facecolor=PAPER, edgecolor=RED, lw=1.4, zorder=10))
        ax.add_patch(Circle((x, y), 0.028, facecolor=RED, edgecolor="none", zorder=11))
    else:
        ax.add_patch(Circle((x, y), 0.045, facecolor=INK, edgecolor="none", zorder=10))
    dy0 = -0.2 if side == "lb" else 0
    side = side[0]
    dx = 0.16 if side == "r" else -0.16
    ha = "left" if side == "r" else "right"
    y = y + dy0
    label(x + dx, y + (0.05 if old else 0), n, 10.5, color=RED if v else INK, ha=ha, weight="bold" if v else "normal", z=12)
    if old:
        label(x + dx, y - 0.13, old, 8.5, "italic", ha=ha, z=12)

# Graticule ticks along the neat line
for lon in range(27, 36):
    for yy, va, dy in [(S, "top", -0.06), (N, "bottom", 0.06)]:
        ax.plot([lon, lon], [yy, yy + (0.12 if yy == S else -0.12)], color=INK, lw=0.8, zorder=12, clip_on=False)
        ax.text(lon, yy + dy, f"{lon}°E", ha="center", va=va, fontsize=7.5, color=INK, clip_on=False)
for lat in range(22, 32):
    for xx, ha, dx in [(W, "right", -0.06), (E, "left", 0.06)]:
        ax.plot([xx, xx + (0.12 if xx == W else -0.12)], [lat, lat], color=INK, lw=0.8, zorder=12, clip_on=False)
        ax.text(xx + dx, lat, f"{lat}°N", ha=ha, va="center", fontsize=7.5, color=INK, rotation=90, clip_on=False)
ax.add_patch(Rectangle((W + 0.07, S + 0.07), E - W - 0.14, N - S - 0.14, fill=False, edgecolor=INK, lw=0.6, zorder=12))

# Compass rose
cx, cy, r = 27.4, 23.2, 0.55
for ang, rr, col in [(0, r, INK), (90, r, INK), (180, r, INK), (270, r, INK), (45, r * 0.55, "#6b5536"), (135, r * 0.55, "#6b5536"), (225, r * 0.55, "#6b5536"), (315, r * 0.55, "#6b5536")]:
    a = np.radians(ang); w = np.radians(90)
    tip = (cx + rr * np.sin(a) * 1.12, cy + rr * np.cos(a))
    l = (cx + rr * 0.18 * np.sin(a - w) * 1.12, cy + rr * 0.18 * np.cos(a - w))
    rt = (cx + rr * 0.18 * np.sin(a + w) * 1.12, cy + rr * 0.18 * np.cos(a + w))
    ax.add_patch(MPoly([tip, l, (cx, cy)], closed=True, facecolor=col, edgecolor=INK, lw=0.6, zorder=12))
    ax.add_patch(MPoly([tip, rt, (cx, cy)], closed=True, facecolor=PAPER, edgecolor=INK, lw=0.6, zorder=12))
ax.add_patch(Circle((cx, cy), r * 0.78, fill=False, edgecolor=INK, lw=0.6, zorder=11))
label(cx, cy + r + 0.17, "N", 11, weight="bold", z=13)

# Scale bar (200 km)
km_per_deg = 111.32 * np.cos(np.radians(22.6))
sx, sy, L = 27.0, 22.05, 200 / km_per_deg
for i in range(4):
    ax.add_patch(Rectangle((sx + i * L / 4, sy), L / 4, 0.06, facecolor=INK if i % 2 == 0 else PAPER, edgecolor=INK, lw=0.6, zorder=12))
for v, xx in [(0, sx), (100, sx + L / 2), (200, sx + L)]:
    ax.text(xx, sy - 0.1, f"{v}", ha="center", va="top", fontsize=7.5, color=INK, zorder=12)
ax.text(sx + L + 0.08, sy + 0.03, "km", ha="left", va="center", fontsize=7.5, color=INK, zorder=12)

# Title cartouche
tx, ty, tw, th = 32.95, 21.95, 2.55, 1.45
ax.add_patch(Rectangle((tx, ty), tw, th, facecolor=PAPER, edgecolor=INK, lw=1.4, zorder=13))
ax.add_patch(Rectangle((tx + 0.06, ty + 0.06), tw - 0.12, th - 0.12, fill=False, edgecolor=INK, lw=0.5, zorder=13))
ax.text(tx + tw / 2, ty + th - 0.33, "A E G Y P T U S", ha="center", va="center", fontsize=15, color=INK, weight="bold", zorder=14)
ax.text(tx + tw / 2, ty + th - 0.68, "The Nile, from Abu Simbel to the Sea", ha="center", va="center", fontsize=8.2, style="italic", color=INK, zorder=14)
ax.add_patch(Circle((tx + 0.3, ty + 0.36), 0.065, facecolor=PAPER, edgecolor=RED, lw=1.2, zorder=14))
ax.add_patch(Circle((tx + 0.3, ty + 0.36), 0.025, facecolor=RED, edgecolor="none", zorder=15))
ax.text(tx + 0.45, ty + 0.36, "Places in this post", ha="left", va="center", fontsize=8.4, color=RED, zorder=14)
ax.text(tx + 0.45, ty + 0.17, "Ancient names in italics", ha="left", va="center", fontsize=7.6, style="italic", color=INK, zorder=14)

# Aged-paper vignette over everything
yy, xx = np.mgrid[-1:1:400j, -1:1:400j]
v = np.clip((np.sqrt(xx ** 2 + yy ** 2) - 0.55) / 0.9, 0, 1)
rgba = np.zeros((400, 400, 4)); rgba[..., 0] = 0.36; rgba[..., 1] = 0.25; rgba[..., 2] = 0.12; rgba[..., 3] = v * 0.28
ax.imshow(rgba, extent=(W, E, S, N), zorder=20, interpolation="bicubic", aspect="auto")
ax.set_xlim(W, E); ax.set_ylim(S, N)
fig.savefig(OUT, facecolor=PAPER, dpi=200)
print("ok")
