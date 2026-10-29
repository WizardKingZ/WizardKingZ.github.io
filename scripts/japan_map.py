"""Old-style map for the Japan post. Usage: python3 turkey_map.py land10.geojson out.png
land10.geojson: Natural Earth 1:10m land (npm world-atlas land-10m.json via topojson-client)."""
import warnings, sys, json, numpy as np, matplotlib
warnings.filterwarnings("ignore"); matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
from matplotlib.patches import Rectangle, Polygon as MPoly, Circle
from shapely.geometry import shape, box, LineString
from shapely import contains_xy
LAND, OUT = sys.argv[1], sys.argv[2]
W, E, S, N = 135.05, 140.05, 34.0, 35.95
INK, RED, PAPER, SEA = "#3d2b1a", "#9b2d1f", "#f0e3c2", "#cfd2b6"
plt.rcParams["font.family"] = "FreeSerif"
frame = box(W, S, E, N)
geo = json.load(open(LAND))
land = shape(geo["features"][0]["geometry"] if "features" in geo else geo["geometry"]).intersection(box(W-2, S-2, E+2, N+2)).buffer(0)
sea = frame.difference(land)
k = 1/np.cos(np.radians(35))
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
route = [(139.767,35.681),(139.617,35.507),(139.155,35.256),(138.911,35.126),(138.389,34.972),(137.734,34.704),(137.382,34.763),(136.881,35.171),(136.29,35.314),(135.758,34.985),(135.50,34.733)]
ax.plot(*zip(*route), color=RED, lw=1.1, ls=(0, (4, 3)), alpha=0.8, zorder=7)
label(138.3, 35.85, "Mare Iaponicum", 10.5, "italic"); label(135.75, 35.82, "Sea of Japan", 8, "italic")
label(138.9, 34.2, "MARE PACIFICUM", 10.5, "italic"); label(138.9, 34.08, "Pacific Ocean", 8, "italic")
label(139.4, 35.92, "MUSASHI", 9, sp=1, color="#6b5536"); label(139.3, 35.42, "SAGAMI", 9, sp=1, color="#6b5536")
label(138.45, 35.2, "SURUGA", 9, sp=1, color="#6b5536"); label(136.9, 35.45, "OWARI", 9, sp=1, color="#6b5536")
label(135.6, 35.3, "YAMASHIRO", 9, sp=1, color="#6b5536"); label(135.95, 34.45, "YAMATO", 9, sp=1, color="#6b5536")
label(137.1, 34.92, "Tōkaidō", 9, "italic", color=RED, rot=-14)
fx, fy = 138.727, 35.361
ax.add_patch(MPoly([(fx-0.13, fy-0.07), (fx, fy+0.08), (fx+0.13, fy-0.07)], closed=True, facecolor=PAPER, edgecolor=INK, lw=1.2, zorder=10))
ax.add_patch(MPoly([(fx-0.045, fy+0.028), (fx, fy+0.08), (fx+0.045, fy+0.028)], closed=True, facecolor="white", edgecolor=INK, lw=0.8, zorder=11))
label(fx, fy - 0.15, "Mt Fuji", 10.5, color=RED, weight="bold", z=12)
places = [(139.767, 35.681, "Tokyo", "Edo", "r", 0),
          (139.02, 35.233, "Hakone", "", "l", 0.02),
          (135.768, 35.011, "Kyoto", "Heian-kyō", "r", 0.05),
          (135.672, 35.02, "Arashiyama", "", "l", 0.06),
          (135.84, 34.685, "Nara", "Heijō-kyō", "r", -0.04),
          (135.502, 34.694, "Osaka", "Naniwa", "l", -0.04)]
for x, y, n, old, side, dy in places:
    ax.add_patch(Circle((x, y), 0.045, facecolor=PAPER, edgecolor=RED, lw=1.4, zorder=10, transform=ax.transData))
    ax.add_patch(Circle((x, y), 0.017, facecolor=RED, edgecolor="none", zorder=11))
    dx = 0.09 if side == "r" else -0.09; ha = "left" if side == "r" else "right"
    label(x + dx, y + dy + (0.035 if old else 0), n, 10.5, color=RED, ha=ha, weight="bold", z=12)
    if old: label(x + dx, y + dy - 0.065, old, 8.3, "italic", ha=ha, z=12)
for lon in range(136, 140):
    for yy, va, d in [(S, "top", -0.03), (N, "bottom", 0.03)]:
        ax.plot([lon, lon], [yy, yy + (0.07 if yy == S else -0.07)], color=INK, lw=0.8, zorder=12, clip_on=False)
        ax.text(lon, yy + d, f"{lon}°E", ha="center", va=va, fontsize=7.5, color=INK, clip_on=False)
for lat in range(35, 36):
    for xx, ha, d in [(W, "right", -0.03), (E, "left", 0.03)]:
        ax.plot([xx, xx + (0.07 if xx == W else -0.07)], [lat, lat], color=INK, lw=0.8, zorder=12, clip_on=False)
        ax.text(xx + d, lat, f"{lat}°N", ha=ha, va="center", fontsize=7.5, color=INK, rotation=90, clip_on=False)
ax.add_patch(Rectangle((W + 0.04, S + 0.04), E - W - 0.08, N - S - 0.08, fill=False, edgecolor=INK, lw=0.6, zorder=12))
cx, cy, r = 139.65, 34.45, 0.22
for ang, rr, col in [(0, r, INK), (90, r, INK), (180, r, INK), (270, r, INK), (45, r*.55, "#6b5536"), (135, r*.55, "#6b5536"), (225, r*.55, "#6b5536"), (315, r*.55, "#6b5536")]:
    a, w = np.radians(ang), np.radians(90)
    tip = (cx + rr*np.sin(a)*k, cy + rr*np.cos(a)); l = (cx + rr*.18*np.sin(a-w)*k, cy + rr*.18*np.cos(a-w)); rt = (cx + rr*.18*np.sin(a+w)*k, cy + rr*.18*np.cos(a+w))
    ax.add_patch(MPoly([tip, l, (cx, cy)], closed=True, facecolor=col, edgecolor=INK, lw=0.6, zorder=12))
    ax.add_patch(MPoly([tip, rt, (cx, cy)], closed=True, facecolor=PAPER, edgecolor=INK, lw=0.6, zorder=12))
label(cx, cy + r + 0.1, "N", 11, weight="bold", z=13)
kmd = 111.32*np.cos(np.radians(34.2)); sx, sy, L = 135.25, 34.12, 100/kmd
for i in range(4):
    ax.add_patch(Rectangle((sx + i*L/4, sy), L/4, 0.03, facecolor=INK if i % 2 == 0 else PAPER, edgecolor=INK, lw=0.6, zorder=12))
for v, xx in [(0, sx), (50, sx + L/2), (100, sx + L)]:
    ax.text(xx, sy - 0.05, str(v), ha="center", va="top", fontsize=7.5, color=INK, zorder=12)
ax.text(sx + L + 0.05, sy + 0.015, "km", ha="left", va="center", fontsize=7.5, color=INK, zorder=12)
tx, ty, tw, th = 137.25, 34.05, 1.45, 0.66
ax.add_patch(Rectangle((tx, ty), tw, th, facecolor=PAPER, edgecolor=INK, lw=1.4, zorder=13))
ax.add_patch(Rectangle((tx + .035, ty + .035), tw - .07, th - .07, fill=False, edgecolor=INK, lw=0.5, zorder=13))
ax.text(tx + tw/2, ty + th - 0.17, "N I P P O N", ha="center", va="center", fontsize=14, color=INK, weight="bold", zorder=14)
ax.text(tx + tw/2, ty + th - 0.34, "Along the Tōkaidō, from Edo to Naniwa", ha="center", va="center", fontsize=6.9, style="italic", color=INK, zorder=14)
ax.add_patch(Circle((tx + .15, ty + .2), 0.035, facecolor=PAPER, edgecolor=RED, lw=1.2, zorder=14))
ax.plot([tx + .1, tx + .2], [ty + .1, ty + .1], color=RED, lw=1.1, ls=(0, (4, 3)), zorder=14)
ax.text(tx + .26, ty + .2, "Places in this post", ha="left", va="center", fontsize=7.8, color=RED, zorder=14)
ax.text(tx + .26, ty + .1, "My route, by train", ha="left", va="center", fontsize=7.4, color=RED, zorder=14)
yy, xx = np.mgrid[-1:1:400j, -1:1:400j]; v = np.clip((np.sqrt(xx**2 + yy**2) - .55)/.9, 0, 1)
rgba = np.zeros((400, 400, 4)); rgba[..., 0], rgba[..., 1], rgba[..., 2], rgba[..., 3] = .36, .25, .12, v*.28
ax.imshow(rgba, extent=(W, E, S, N), zorder=20, interpolation="bicubic", aspect="auto"); ax.set_xlim(W, E); ax.set_ylim(S, N)
fig.savefig(OUT, facecolor=PAPER, dpi=200); print("ok")
