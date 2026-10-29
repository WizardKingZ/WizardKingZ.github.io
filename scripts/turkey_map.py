"""Old-style map for the Türkiye post. Usage: python3 turkey_map.py land10.geojson out.png
land10.geojson: Natural Earth 1:10m land (npm world-atlas land-10m.json via topojson-client)."""
import warnings, sys, json, numpy as np, matplotlib
warnings.filterwarnings("ignore"); matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
from matplotlib.patches import Rectangle, Polygon as MPoly, Circle
from shapely.geometry import shape, box, LineString
from shapely import contains_xy
LAND, OUT = sys.argv[1], sys.argv[2]
W, E, S, N = 25.55, 30.45, 37.35, 41.55
INK, RED, PAPER, SEA = "#3d2b1a", "#9b2d1f", "#f0e3c2", "#cfd2b6"
plt.rcParams["font.family"] = "FreeSerif"
frame = box(W, S, E, N)
geo = json.load(open(LAND))
land = shape(geo["features"][0]["geometry"] if "features" in geo else geo["geometry"]).intersection(box(W-2, S-2, E+2, N+2)).buffer(0)
sea = frame.difference(land)
k = 1/np.cos(np.radians(39.4))
fig = plt.figure(figsize=(8, 8.9), dpi=200, facecolor=PAPER)
ax = fig.add_axes([0.06, 0.045, 0.88, 0.91]); ax.set_xlim(W, E); ax.set_ylim(S, N); ax.set_aspect(k)
ax.set_facecolor(SEA); ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_color(INK); s.set_linewidth(2.2)
def polys(g): return [g] if g.geom_type == "Polygon" else [p for p in getattr(g, "geoms", []) if p.geom_type == "Polygon"]
from matplotlib.path import Path
from matplotlib.patches import PathPatch
def fill(g, **kw):
    for p in polys(g):
        verts, codes = [], []
        for ring in [p.exterior, *p.interiors]:
            c = np.array(ring.coords); verts += c.tolist(); codes += [Path.MOVETO] + [Path.LINETO]*(len(c)-2) + [Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts, codes), **kw))
def line(g, **kw):
    gs = [g] if g.geom_type in ("LineString", "LinearRing") else list(getattr(g, "geoms", []))
    for l in gs:
        if l.geom_type in ("LineString", "LinearRing") and not l.is_empty:
            x, y = l.xy; ax.plot(x, y, solid_capstyle="round", **kw)
big = land.buffer(0.004).simplify(0.004)
for i, d in enumerate([0.035, 0.08, 0.14, 0.22]):
    line(big.buffer(d).boundary.intersection(sea), color=INK, lw=0.5 - i*0.08, alpha=0.5 - i*0.1, zorder=2)
fill(land.intersection(frame.buffer(0.3)), facecolor=PAPER, edgecolor="none", zorder=3)
rng = np.random.default_rng(3); pts = np.column_stack([rng.uniform(W, E, 7000), rng.uniform(S, N, 7000)])
m = contains_xy(land, pts[:, 0], pts[:, 1]); ax.scatter(pts[m, 0], pts[m, 1], s=0.45, color=INK, alpha=0.2, lw=0, zorder=3.5)
line(land.boundary.intersection(frame), color=INK, lw=1.0, zorder=6)
halo = [pe.withStroke(linewidth=2.6, foreground=PAPER)]
def label(x, y, t, size=10, style="normal", color=INK, ha="center", sp=0, rot=0, weight="normal", z=9):
    if sp: t = (" " * sp).join(t)
    ax.text(x, y, t, fontsize=size, style=style, color=color, ha=ha, va="center", rotation=rot, weight=weight, path_effects=halo, zorder=z)
# Route driven (approximate), dashed
route = [(28.98, 41.01), (28.2, 41.05), (27.5, 40.98), (26.95, 40.62), (26.68, 40.40), (26.41, 40.15), (26.24, 39.96), (26.16, 39.75),
         (26.45, 39.6), (26.9, 39.3), (27.05, 38.9), (27.14, 38.42), (27.25, 38.15), (27.34, 37.94), (26.78, 38.18), (27.37, 37.95),
         (28.0, 37.88), (28.6, 37.85), (29.12, 37.92)]
ax.plot(*zip(*route), color=RED, lw=1.1, ls=(0, (4, 3)), alpha=0.8, zorder=7)
label(31.0, 40.0, "")
label(29.6, 41.35, "PONTUS EUXINUS", 10.5, "italic"); label(29.6, 41.22, "Black Sea", 8, "italic")
label(28.15, 40.72, "PROPONTIS", 10.5, "italic"); label(28.15, 40.6, "Sea of Marmara", 8, "italic")
label(25.95, 38.85, "MARE AEGAEUM", 10.5, "italic", rot=90); label(26.17, 38.85, "Aegean Sea", 8, "italic", rot=90)
label(26.6, 40.3, "Hellespontus", 8.5, "italic", color="#2f4a5c", rot=38)
label(29.25, 41.12, "Bosporus", 8.5, "italic", color="#2f4a5c", rot=62)
label(27.75, 41.32, "THRACE", 11, sp=1, weight="bold"); label(26.85, 39.45, "TROAS", 9, sp=1, color="#6b5536")
label(27.85, 38.85, "IONIA", 9, sp=1, color="#6b5536"); label(29.75, 37.78, "PHRYGIA", 9, sp=1, color="#6b5536")
label(28.7, 39.55, "A S I A   M I N O R", 13, weight="bold"); label(29.3, 40.35, "BITHYNIA", 9, sp=1, color="#6b5536")
places = [(28.98, 41.01, "Istanbul", "Byzantion · Constantinople", "l", 0.12),
          (29.03, 40.99, "Kadıköy", "Chalcedon", "r", -0.12),
          (26.41, 40.15, "Çanakkale", "", "r", 0),
          (26.24, 39.96, "Troy", "Ilion", "l", 0),
          (26.16, 39.75, "Alexandria Troas", "", "l", -0.04),
          (27.14, 38.42, "İzmir", "Smyrna", "r", 0),
          (26.78, 38.18, "Teos", "", "l", 0),
          (27.34, 37.94, "Ephesus · Selçuk", "Ephesos", "r", -0.1),
          (29.12, 37.92, "Pamukkale", "Hierapolis · Laodicea", "l", 0.12)]
for x, y, n, old, side, dy in places:
    ax.add_patch(Circle((x, y), 0.045, facecolor=PAPER, edgecolor=RED, lw=1.4, zorder=10, transform=ax.transData))
    ax.add_patch(Circle((x, y), 0.017, facecolor=RED, edgecolor="none", zorder=11))
    dx = 0.09 if side == "r" else -0.09; ha = "left" if side == "r" else "right"
    label(x + dx, y + dy + (0.035 if old else 0), n, 10.5, color=RED, ha=ha, weight="bold", z=12)
    if old: label(x + dx, y + dy - 0.065, old, 8.3, "italic", ha=ha, z=12)
for lon in range(26, 31):
    for yy, va, d in [(S, "top", -0.03), (N, "bottom", 0.03)]:
        ax.plot([lon, lon], [yy, yy + (0.07 if yy == S else -0.07)], color=INK, lw=0.8, zorder=12, clip_on=False)
        ax.text(lon, yy + d, f"{lon}°E", ha="center", va=va, fontsize=7.5, color=INK, clip_on=False)
for lat in range(38, 42):
    for xx, ha, d in [(W, "right", -0.03), (E, "left", 0.03)]:
        ax.plot([xx, xx + (0.07 if xx == W else -0.07)], [lat, lat], color=INK, lw=0.8, zorder=12, clip_on=False)
        ax.text(xx + d, lat, f"{lat}°N", ha=ha, va="center", fontsize=7.5, color=INK, rotation=90, clip_on=False)
ax.add_patch(Rectangle((W + 0.04, S + 0.04), E - W - 0.08, N - S - 0.08, fill=False, edgecolor=INK, lw=0.6, zorder=12))
cx, cy, r = 29.9, 39.75, 0.28
for ang, rr, col in [(0, r, INK), (90, r, INK), (180, r, INK), (270, r, INK), (45, r*.55, "#6b5536"), (135, r*.55, "#6b5536"), (225, r*.55, "#6b5536"), (315, r*.55, "#6b5536")]:
    a, w = np.radians(ang), np.radians(90)
    tip = (cx + rr*np.sin(a)*k, cy + rr*np.cos(a)); l = (cx + rr*.18*np.sin(a-w)*k, cy + rr*.18*np.cos(a-w)); rt = (cx + rr*.18*np.sin(a+w)*k, cy + rr*.18*np.cos(a+w))
    ax.add_patch(MPoly([tip, l, (cx, cy)], closed=True, facecolor=col, edgecolor=INK, lw=0.6, zorder=12))
    ax.add_patch(MPoly([tip, rt, (cx, cy)], closed=True, facecolor=PAPER, edgecolor=INK, lw=0.6, zorder=12))
label(cx, cy + r + 0.1, "N", 11, weight="bold", z=13)
kmd = 111.32*np.cos(np.radians(37.6)); sx, sy, L = 28.95, 37.55, 100/kmd
for i in range(4):
    ax.add_patch(Rectangle((sx + i*L/4, sy), L/4, 0.03, facecolor=INK if i % 2 == 0 else PAPER, edgecolor=INK, lw=0.6, zorder=12))
for v, xx in [(0, sx), (50, sx + L/2), (100, sx + L)]:
    ax.text(xx, sy - 0.05, str(v), ha="center", va="top", fontsize=7.5, color=INK, zorder=12)
ax.text(sx + L + 0.05, sy + 0.015, "km", ha="left", va="center", fontsize=7.5, color=INK, zorder=12)
tx, ty, tw, th = 28.75, 38.3, 1.55, 0.78
ax.add_patch(Rectangle((tx, ty), tw, th, facecolor=PAPER, edgecolor=INK, lw=1.4, zorder=13))
ax.add_patch(Rectangle((tx + .035, ty + .035), tw - .07, th - .07, fill=False, edgecolor=INK, lw=0.5, zorder=13))
ax.text(tx + tw/2, ty + th - 0.17, "R O M A N I A", ha="center", va="center", fontsize=14, color=INK, weight="bold", zorder=14)
ax.text(tx + tw/2, ty + th - 0.34, "The Romans' own name for their eastern empire", ha="center", va="center", fontsize=6.9, style="italic", color=INK, zorder=14)
ax.add_patch(Circle((tx + .15, ty + .2), 0.035, facecolor=PAPER, edgecolor=RED, lw=1.2, zorder=14))
ax.plot([tx + .1, tx + .2], [ty + .1, ty + .1], color=RED, lw=1.1, ls=(0, (4, 3)), zorder=14)
ax.text(tx + .26, ty + .2, "Places in this post", ha="left", va="center", fontsize=7.8, color=RED, zorder=14)
ax.text(tx + .26, ty + .1, "My route, by road", ha="left", va="center", fontsize=7.4, color=RED, zorder=14)
yy, xx = np.mgrid[-1:1:400j, -1:1:400j]; v = np.clip((np.sqrt(xx**2 + yy**2) - .55)/.9, 0, 1)
rgba = np.zeros((400, 400, 4)); rgba[..., 0], rgba[..., 1], rgba[..., 2], rgba[..., 3] = .36, .25, .12, v*.28
ax.imshow(rgba, extent=(W, E, S, N), zorder=20, interpolation="bicubic", aspect="auto"); ax.set_xlim(W, E); ax.set_ylim(S, N)
fig.savefig(OUT, facecolor=PAPER, dpi=200); print("ok")
