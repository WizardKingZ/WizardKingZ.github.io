"""Old-style map of Tokyo for the Japan post. Usage: python3 turkey_map.py land10.geojson out.png
land10.geojson: Natural Earth 1:10m land (npm world-atlas land-10m.json via topojson-client)."""
import warnings, sys, json, numpy as np, matplotlib
warnings.filterwarnings("ignore"); matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
from matplotlib.patches import Rectangle, Polygon as MPoly, Circle, Ellipse
from shapely.geometry import shape, box, LineString
from shapely import contains_xy
LAND, OUT = sys.argv[1], sys.argv[2]
W, E, S, N = 139.665, 139.835, 35.612, 35.728
INK, RED, PAPER, SEA = "#3d2b1a", "#9b2d1f", "#f0e3c2", "#cfd2b6"
plt.rcParams["font.family"] = "FreeSerif"
frame = box(W, S, E, N)
geo = json.load(open(LAND))
land = shape(geo["features"][0]["geometry"] if "features" in geo else geo["geometry"]).intersection(box(W-2, S-2, E+2, N+2)).buffer(0)
# Natural Earth is too coarse at city scale, so the bay shore is drawn by hand (approximate).
from shapely.geometry import Polygon as SPoly
shore = [(139.665, 35.612), (139.745, 35.612), (139.748, 35.622), (139.754, 35.634), (139.760, 35.648), (139.766, 35.654),
         (139.772, 35.656), (139.777, 35.649), (139.786, 35.646), (139.795, 35.642), (139.806, 35.639), (139.816, 35.644),
         (139.835, 35.640), (139.835, 35.612)]
bay = SPoly([(139.745, 35.612), (139.748, 35.622), (139.754, 35.634), (139.760, 35.648), (139.766, 35.654), (139.772, 35.656),
             (139.777, 35.649), (139.786, 35.646), (139.795, 35.642), (139.806, 35.639), (139.816, 35.644), (139.835, 35.640),
             (139.835, 35.612)])
odaiba = SPoly([(139.766, 35.632), (139.772, 35.634), (139.786, 35.630), (139.790, 35.622), (139.780, 35.616), (139.768, 35.620)])
land = frame.difference(bay).union(odaiba)
sea = frame.difference(land)
k = 1/np.cos(np.radians(35.67))
fig = plt.figure(figsize=(8.0, round(8.0*0.88*k*(N-S)/(E-W)/0.91, 2)), dpi=200, facecolor=PAPER)
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
big = land.buffer(0.0002).simplify(0.0002)
for i, d in enumerate([0.0015, 0.0034, 0.006, 0.0095]):
    line(big.buffer(d).boundary.intersection(sea), color=INK, lw=0.5 - i*0.08, alpha=0.5 - i*0.1, zorder=2)
fill(land.intersection(frame.buffer(0.02)), facecolor=PAPER, edgecolor="none", zorder=3)
rng = np.random.default_rng(3); pts = np.column_stack([rng.uniform(W, E, 7000), rng.uniform(S, N, 7000)])
m = contains_xy(land, pts[:, 0], pts[:, 1]); ax.scatter(pts[m, 0], pts[m, 1], s=0.45, color=INK, alpha=0.2, lw=0, zorder=3.5)
line(land.boundary.intersection(frame), color=INK, lw=1.0, zorder=6)
halo = [pe.withStroke(linewidth=2.6, foreground=PAPER)]
sumida = [(139.800, 35.728), (139.799, 35.718), (139.797, 35.708), (139.794, 35.697), (139.789, 35.684), (139.785, 35.672), (139.779, 35.660)]
ax.plot(*zip(*sumida), color="#2f4a5c", lw=2.2, zorder=7, solid_capstyle="round")
ax.text(139.8035, 35.703, "Sumida River", fontsize=8.5, style="italic", color="#2f4a5c", rotation=-75, ha="center", va="center", zorder=9, path_effects=[pe.withStroke(linewidth=2.6, foreground=PAPER)])
def label(x, y, t, size=10, style="normal", color=INK, ha="center", sp=0, rot=0, weight="normal", z=9):
    if sp: t = (" " * sp).join(t)
    ax.text(x, y, t, fontsize=size, style=style, color=color, ha=ha, va="center", rotation=rot, weight=weight, path_effects=halo, zorder=z)
label(139.812, 35.628, "Edo Bay", 11, "italic"); label(139.812, 35.6235, "Tokyo Bay", 8, "italic")
label(139.73, 35.71, "YAMANOTE", 9, sp=1, color="#6b5536"); label(139.805, 35.695, "SHITAMACHI", 9, sp=1, color="#6b5536")
places = [(139.7528, 35.6852, "Imperial Palace", "Edo Castle", "l", 0.002),
          (139.7671, 35.6812, "Tokyo Station", "", "l", -0.0045),
          (139.7725, 35.6803, "Nihonbashi · Kyōbashi", "", "r", 0.0),
          (139.7718, 35.6927, "Kanda", "", "r", -0.002),
          (139.7731, 35.6984, "Akihabara", "", "r", 0.002),
          (139.7967, 35.7148, "Asakusa · Sensō-ji", "", "r", 0),
          (139.7010, 35.6938, "Shinjuku · Kabukichō", "", "r", 0),
          (139.6993, 35.6764, "Meiji Jingu", "", "r", 0),
          (139.7016, 35.6595, "Shibuya", "", "r", 0),
          (139.7480, 35.6573, "Zōjō-ji · Tokyo Tower", "", "l", 0),
          (139.7707, 35.6655, "Tsukiji", "", "r", 0),
          (139.7898, 35.6489, "Toyosu · teamLab", "", "r", 0),
          (139.7756, 35.6253, "Odaiba", "Daiba batteries", "r", 0)]
for x, y, n, old, side, dy in places:
    ax.add_patch(Ellipse((x, y), 2*0.0016, 2*0.0016/k, facecolor=PAPER, edgecolor=RED, lw=1.4, zorder=10))
    ax.add_patch(Ellipse((x, y), 2*0.0006, 2*0.0006/k, facecolor=RED, edgecolor="none", zorder=11))
    dx = 0.0032 if side == "r" else -0.09; ha = "left" if side == "r" else "right"
    label(x + dx, y + dy + (0.0013 if old else 0), n, 10.5, color=RED, ha=ha, weight="bold", z=12)
    if old: label(x + dx, y + dy - 0.0024, old, 8.3, "italic", ha=ha, z=12)
for lon in []:
    for yy, va, d in [(S, "top", -0.03), (N, "bottom", 0.03)]:
        ax.plot([lon, lon], [yy, yy + (0.07 if yy == S else -0.07)], color=INK, lw=0.8, zorder=12, clip_on=False)
        ax.text(lon, yy + d, f"{lon}°E", ha="center", va=va, fontsize=7.5, color=INK, clip_on=False)
for lat in []:
    for xx, ha, d in [(W, "right", -0.03), (E, "left", 0.03)]:
        ax.plot([xx, xx + (0.07 if xx == W else -0.07)], [lat, lat], color=INK, lw=0.8, zorder=12, clip_on=False)
        ax.text(xx + d, lat, f"{lat}°N", ha=ha, va="center", fontsize=7.5, color=INK, rotation=90, clip_on=False)
ax.add_patch(Rectangle((W + 0.0015, S + 0.0015), E - W - 0.003, N - S - 0.003, fill=False, edgecolor=INK, lw=0.6, zorder=12))
cx, cy, r = 139.685, 35.626, 0.008
for ang, rr, col in [(0, r, INK), (90, r, INK), (180, r, INK), (270, r, INK), (45, r*.55, "#6b5536"), (135, r*.55, "#6b5536"), (225, r*.55, "#6b5536"), (315, r*.55, "#6b5536")]:
    a, w = np.radians(ang), np.radians(90)
    tip = (cx + rr*np.sin(a)*k, cy + rr*np.cos(a)); l = (cx + rr*.18*np.sin(a-w)*k, cy + rr*.18*np.cos(a-w)); rt = (cx + rr*.18*np.sin(a+w)*k, cy + rr*.18*np.cos(a+w))
    ax.add_patch(MPoly([tip, l, (cx, cy)], closed=True, facecolor=col, edgecolor=INK, lw=0.6, zorder=12))
    ax.add_patch(MPoly([tip, rt, (cx, cy)], closed=True, facecolor=PAPER, edgecolor=INK, lw=0.6, zorder=12))
label(cx, cy + r + 0.004, "N", 11, weight="bold", z=13)
kmd = 111.32*np.cos(np.radians(35.62)); sx, sy, L = 139.700, 35.617, 4/kmd
for i in range(4):
    ax.add_patch(Rectangle((sx + i*L/4, sy), L/4, 0.0011, facecolor=INK if i % 2 == 0 else PAPER, edgecolor=INK, lw=0.6, zorder=12))
for v, xx in [(0, sx), (2, sx + L/2), (4, sx + L)]:
    ax.text(xx, sy - 0.0018, str(v), ha="center", va="top", fontsize=7.5, color=INK, zorder=12)
ax.text(sx + L + 0.0018, sy + 0.0006, "km", ha="left", va="center", fontsize=7.5, color=INK, zorder=12)
tx, ty, tw, th = 139.762, 35.6155, 0.05, 0.0175
ax.add_patch(Rectangle((tx, ty), tw, th, facecolor=PAPER, edgecolor=INK, lw=1.4, zorder=13))
ax.add_patch(Rectangle((tx + .0012, ty + .0012), tw - .0024, th - .0024, fill=False, edgecolor=INK, lw=0.5, zorder=13))
ax.text(tx + tw/2, ty + th - 0.0045, "E D O · T O K Y O", ha="center", va="center", fontsize=14, color=INK, weight="bold", zorder=14)
ax.text(tx + tw/2, ty + th - 0.009, "The shogun's city and the emperor's capital", ha="center", va="center", fontsize=6.9, style="italic", color=INK, zorder=14)
ax.add_patch(Ellipse((tx + .005, ty + .0045), 2*0.0013, 2*0.0013/k, facecolor=PAPER, edgecolor=RED, lw=1.2, zorder=14))
ax.plot([], [], color=RED, lw=1.1, ls=(0, (4, 3)), zorder=14)
ax.text(tx + .009, ty + .0045, "Places in this post", ha="left", va="center", fontsize=7.8, color=RED, zorder=14)
ax.text(tx + .009, ty + .0045, "", ha="left", va="center", fontsize=7.4, color=RED, zorder=14)
yy, xx = np.mgrid[-1:1:400j, -1:1:400j]; v = np.clip((np.sqrt(xx**2 + yy**2) - .55)/.9, 0, 1)
rgba = np.zeros((400, 400, 4)); rgba[..., 0], rgba[..., 1], rgba[..., 2], rgba[..., 3] = .36, .25, .12, v*.28
ax.imshow(rgba, extent=(W, E, S, N), zorder=20, interpolation="bicubic", aspect=k); ax.set_xlim(W, E); ax.set_ylim(S, N)
fig.savefig(OUT, facecolor=PAPER, dpi=200); print("ok")
