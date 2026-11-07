"""Old-style maps for the New Zealand post.
Usage: python3 nz_map.py land10.geojson lakes10.geojson out_dir
land10.geojson: Natural Earth 1:10m land (npm world-atlas land-10m.json via topojson-client).
lakes10.geojson: Natural Earth 1:10m lakes (nvkelso/natural-earth-vector, geojson/ne_10m_lakes.geojson).
Writes nz-map.jpg. Coastlines and lakes are Natural Earth 1:10m, so small features are approximate."""
import warnings, sys, json, numpy as np, matplotlib
warnings.filterwarnings("ignore"); matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
from matplotlib.patches import Rectangle, Polygon as MPoly, Ellipse, PathPatch
from matplotlib.path import Path
from shapely.geometry import shape, box
from shapely.ops import unary_union
from shapely import contains_xy
from PIL import Image

LAND, LAKES, OUTDIR = sys.argv[1], sys.argv[2], sys.argv[3]
INK, RED, PAPER, SEA, GREEN = "#3d2b1a", "#9b2d1f", "#f0e3c2", "#cfd2b6", "#3f5a2a"
plt.rcParams["font.family"] = "FreeSerif"
geo = json.load(open(LAND))
LAND_ALL = shape(geo["features"][0]["geometry"] if "features" in geo else geo["geometry"])
LAKES_ALL = unary_union([shape(f["geometry"]) for f in json.load(open(LAKES))["features"]
                         if 166 < shape(f["geometry"]).centroid.x < 179 and -48 < shape(f["geometry"]).centroid.y < -34])


def draw(W, E, S, N, width, cfg, out):
    frame = box(W, S, E, N)
    land = LAND_ALL.intersection(box(W - 2, S - 2, E + 2, N + 2)).buffer(0)
    lakes = LAKES_ALL.intersection(frame.buffer(0.5))
    water = frame.difference(land).union(lakes.intersection(frame))
    k = 1 / np.cos(np.radians((S + N) / 2))
    fig = plt.figure(figsize=(width, round(width * 0.88 * k * (N - S) / (E - W) / 0.91, 2)), dpi=200, facecolor=PAPER)
    ax = fig.add_axes([0.06, 0.045, 0.88, 0.91]); ax.set_xlim(W, E); ax.set_ylim(S, N); ax.set_aspect(k)
    ax.set_facecolor(SEA); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color(INK); s.set_linewidth(2.2)
    sc = (E - W) / 5.0  # scale factor relative to the Japan map

    def polys(g): return [g] if g.geom_type == "Polygon" else [p for p in getattr(g, "geoms", []) if p.geom_type == "Polygon"]

    def fill(g, **kw):
        for p in polys(g):
            verts, codes = [], []
            for ring in [p.exterior, *p.interiors]:
                c = np.array(ring.coords); verts += c.tolist(); codes += [Path.MOVETO] + [Path.LINETO] * (len(c) - 2) + [Path.CLOSEPOLY]
            ax.add_patch(PathPatch(Path(verts, codes), **kw))

    def line(g, **kw):
        gs = [g] if g.geom_type in ("LineString", "LinearRing") else list(getattr(g, "geoms", []))
        for l in gs:
            if l.geom_type in ("LineString", "LinearRing") and not l.is_empty:
                x, y = l.xy; ax.plot(x, y, solid_capstyle="round", **kw)

    big = land.buffer(0.004 * sc).simplify(0.004 * sc)
    sea = frame.difference(land)
    for i, d in enumerate([0.035, 0.08, 0.14, 0.22]):
        line(big.buffer(d * sc).boundary.intersection(sea), color=INK, lw=0.5 - i * 0.08, alpha=0.5 - i * 0.1, zorder=2)
    fill(land.intersection(frame.buffer(0.3 * sc)), facecolor=PAPER, edgecolor="none", zorder=3)
    rng = np.random.default_rng(3); n = 9000
    pts = np.column_stack([rng.uniform(W, E, n), rng.uniform(S, N, n)])
    m = contains_xy(land, pts[:, 0], pts[:, 1]) & ~contains_xy(lakes, pts[:, 0], pts[:, 1])
    ax.scatter(pts[m, 0], pts[m, 1], s=0.45, color=INK, alpha=0.2, lw=0, zorder=3.5)
    fill(lakes.intersection(frame), facecolor=SEA, edgecolor=INK, lw=0.7, zorder=4)
    line(land.boundary.intersection(frame), color=INK, lw=1.0, zorder=6)
    halo = [pe.withStroke(linewidth=2.6, foreground=PAPER)]

    def label(x, y, t, size=10, style="normal", color=INK, ha="center", sp=0, rot=0, weight="normal", z=9):
        if sp: t = (" " * sp).join(t)
        ax.text(x, y, t, fontsize=size, style=style, color=color, ha=ha, va="center", rotation=rot, weight=weight, path_effects=halo, zorder=z)

    for pts_, style in cfg.get("routes", []):
        ls = (0, (4, 3)) if style == "road" else (0, (1, 2.2))
        ax.plot(*zip(*pts_), color=RED, lw=1.1 if style == "road" else 1.0, ls=ls, alpha=0.85, zorder=7)
    for args in cfg.get("labels", []):
        label(*args[:3], **args[3])
    for mx, my, name, sub in cfg.get("mountains", []):
        h = 0.045 * sc
        ax.add_patch(MPoly([(mx - h * 1.3, my - h), (mx, my + h), (mx + h * 1.3, my - h)], closed=True, facecolor=PAPER, edgecolor=INK, lw=1.2, zorder=10))
        ax.add_patch(MPoly([(mx - h * 0.55, my + h * 0.35), (mx, my + h), (mx + h * 0.55, my + h * 0.35)], closed=True, facecolor="white", edgecolor=INK, lw=0.8, zorder=11))
        label(mx - h*1.6, my + 0.035 * sc, name, 10.5, color=RED, weight="bold", ha="right", z=12)
        if sub: label(mx - h*1.6, my - 0.035 * sc, sub, 8.3, "italic", ha="right", z=12)
    for p in cfg["places"]:
        x, y, nme, old, side, dx, dy = p[:7]
        lx, ly = (p[7] if len(p) > 7 else (None, None))
        r = 0.045 * sc
        ax.add_patch(Ellipse((x, y), 2 * r, 2 * r / k, facecolor=PAPER, edgecolor=RED, lw=1.4, zorder=10))
        ax.add_patch(Ellipse((x, y), 2 * 0.017 * sc, 2 * 0.017 * sc / k, facecolor=RED, edgecolor="none", zorder=11))
        ha = {"r": "left", "l": "right", "c": "center"}[side]
        tx, ty = x + dx * sc, y + dy * sc
        if lx is not None:
            ax.plot([x, lx], [y, ly], color=RED, lw=0.6, zorder=9)
        label(tx, ty + (0.035 * sc if old else 0), nme, 10.5, color=RED, ha=ha, weight="bold", z=12)
        if old: label(tx, ty - 0.065 * sc, old, 8.3, "italic", ha=ha, z=12)
    for x, y, t, ha in cfg.get("me", []):  # Middle-earth filming notes
        ax.add_patch(Ellipse((x, y), 2 * 0.022 * sc, 2 * 0.022 * sc / k, facecolor=GREEN, edgecolor="none", zorder=10))
        label(x + (0.05 * sc if ha == "left" else -0.05 * sc), y, t, 8.2, "italic", color=GREEN, ha=ha, z=12)
    # degree ticks
    for lon in cfg["lons"]:
        for yy, va, d in [(S, "top", -0.03 * sc), (N, "bottom", 0.03 * sc)]:
            ax.plot([lon, lon], [yy, yy + (0.07 * sc if yy == S else -0.07 * sc)], color=INK, lw=0.8, zorder=12, clip_on=False)
            ax.text(lon, yy + d, cfg["lonfmt"](lon), ha="center", va=va, fontsize=7.5, color=INK, clip_on=False)
    for lat in cfg["lats"]:
        for xx, ha, d in [(W, "right", -0.03 * sc), (E, "left", 0.03 * sc)]:
            ax.plot([xx, xx + (0.07 * sc if xx == W else -0.07 * sc)], [lat, lat], color=INK, lw=0.8, zorder=12, clip_on=False)
            ax.text(xx + d, lat, cfg["latfmt"](lat), ha=ha, va="center", fontsize=7.5, color=INK, rotation=90, clip_on=False)
    ax.add_patch(Rectangle((W + 0.04 * sc, S + 0.04 * sc), E - W - 0.08 * sc, N - S - 0.08 * sc, fill=False, edgecolor=INK, lw=0.6, zorder=12))
    # compass rose
    cx, cy = cfg["compass"]; r = 0.22 * sc
    for ang, rr, col in [(0, r, INK), (90, r, INK), (180, r, INK), (270, r, INK), (45, r * .55, "#6b5536"), (135, r * .55, "#6b5536"), (225, r * .55, "#6b5536"), (315, r * .55, "#6b5536")]:
        a, w = np.radians(ang), np.radians(90)
        tip = (cx + rr * np.sin(a) * k, cy + rr * np.cos(a)); l = (cx + rr * .18 * np.sin(a - w) * k, cy + rr * .18 * np.cos(a - w)); rt = (cx + rr * .18 * np.sin(a + w) * k, cy + rr * .18 * np.cos(a + w))
        ax.add_patch(MPoly([tip, l, (cx, cy)], closed=True, facecolor=col, edgecolor=INK, lw=0.6, zorder=12))
        ax.add_patch(MPoly([tip, rt, (cx, cy)], closed=True, facecolor=PAPER, edgecolor=INK, lw=0.6, zorder=12))
    label(cx, cy + r + 0.1 * sc, "N", 11, weight="bold", z=13)
    # scale bar
    sx, sy, km = cfg["scale"]
    kmd = 111.32 * np.cos(np.radians(sy)); L = km / kmd
    for i in range(4):
        ax.add_patch(Rectangle((sx + i * L / 4, sy), L / 4, 0.03 * sc, facecolor=INK if i % 2 == 0 else PAPER, edgecolor=INK, lw=0.6, zorder=12))
    for v, xx in [(0, sx), (km // 2, sx + L / 2), (km, sx + L)]:
        ax.text(xx, sy - 0.05 * sc, str(v), ha="center", va="top", fontsize=7.5, color=INK, zorder=12)
    ax.text(sx + L + 0.05 * sc, sy + 0.015 * sc, "km", ha="left", va="center", fontsize=7.5, color=INK, zorder=12)
    # title box
    tx, ty, tw, th = cfg["title_box"]
    ax.add_patch(Rectangle((tx, ty), tw, th, facecolor=PAPER, edgecolor=INK, lw=1.4, zorder=13))
    ax.add_patch(Rectangle((tx + .035 * sc, ty + .035 * sc), tw - .07 * sc, th - .07 * sc, fill=False, edgecolor=INK, lw=0.5, zorder=13))
    ax.text(tx + tw / 2, ty + th * 0.80, cfg["title"], ha="center", va="center", fontsize=14, color=INK, weight="bold", zorder=14)
    ax.text(tx + tw / 2, ty + th * 0.63, cfg["subtitle"], ha="center", va="center", fontsize=6.9, style="italic", color=INK, zorder=14)
    rows = cfg["legend"]
    for i, (kind, text) in enumerate(rows):
        yy = ty + th * (0.47 - i * 0.12)
        x0 = tx + 0.1 * sc
        if kind == "place":
            ax.add_patch(Ellipse((x0 + 0.05 * sc, yy), 2 * 0.035 * sc, 2 * 0.035 * sc / k, facecolor=PAPER, edgecolor=RED, lw=1.2, zorder=14)); col = RED
        elif kind == "me":
            ax.add_patch(Ellipse((x0 + 0.05 * sc, yy), 2 * 0.022 * sc, 2 * 0.022 * sc / k, facecolor=GREEN, edgecolor="none", zorder=14)); col = GREEN
        else:
            ax.plot([x0, x0 + 0.1 * sc], [yy, yy], color=RED, lw=1.1, ls=(0, (4, 3)) if kind == "road" else (0, (1, 2.2)), zorder=14); col = RED
        ax.text(x0 + 0.16 * sc, yy, text, ha="left", va="center", fontsize=7.6, color=col, zorder=14)
    yy, xx = np.mgrid[-1:1:400j, -1:1:400j]; v = np.clip((np.sqrt(xx ** 2 + yy ** 2) - .55) / .9, 0, 1)
    rgba = np.zeros((400, 400, 4)); rgba[..., 0], rgba[..., 1], rgba[..., 2], rgba[..., 3] = .36, .25, .12, v * .28
    ax.imshow(rgba, extent=(W, E, S, N), zorder=20, interpolation="bicubic", aspect=k); ax.set_xlim(W, E); ax.set_ylim(S, N)
    png = out.replace(".jpg", ".png")
    fig.savefig(png, facecolor=PAPER, dpi=200); plt.close(fig)
    im = Image.open(png).convert("RGB"); im.thumbnail((1600, 2400)); im.save(out, quality=86, progressive=True, optimize=True)
    print("ok", out, im.size)


deg = lambda h: (lambda v: f"{abs(v)}°{h}")

# ---------- Whole route ----------
road1 = [(172.636, -43.532), (171.2, -43.9), (170.477, -44.004), (170.15, -44.12), (170.10, -43.735),
         (170.15, -44.12), (170.10, -44.26), (170.97, -45.10), (170.828, -45.345), (170.504, -45.874),
         (169.40, -45.30), (169.0, -45.0), (168.833, -44.939), (168.663, -45.031), (168.388, -44.851)]
road2 = [(174.763, -36.848), (175.0, -37.6), (175.10, -38.26), (175.7, -38.15), (176.192, -38.086), (176.252, -38.137), (176.369, -38.359),
         (175.6, -37.8), (174.763, -36.848)]
def arc(a, c, b, n=60):
    t = np.linspace(0, 1, n)[:, None]; a, b, c = map(np.array, (a, b, c))
    return [tuple(p) for p in (1 - t) ** 2 * a + 2 * (1 - t) * t * c + t ** 2 * b]
fly1 = arc((174.70, -37.0), (176.2, -40.6), (172.60, -43.40))
fly2 = arc((168.60, -44.95), (167.6, -40.2), (174.60, -36.95))
main = dict(
    routes=[(road1, "road"), (road2, "road"), (fly1, "air"), (fly2, "air")],
    labels=[(168.2, -40.0, "Te Tai-o-Rēhua", dict(size=10.5, style="italic")),
            (168.2, -40.22, "Tasman Sea", dict(size=8, style="italic")),
            (177.0, -43.0, "TE MOANA-NUI-A-KIWA", dict(size=10.5, style="italic")),
            (177.0, -43.22, "Pacific Ocean", dict(size=8, style="italic")),
            (175.55, -39.35, "TE IKA-A-MĀUI", dict(size=9.5, sp=0, color="#6b5536", weight="bold")),
            (175.55, -39.57, "North Island", dict(size=8, style="italic", color="#6b5536")),
            (172.3, -42.1, "TE WAIPOUNAMU", dict(size=9.5, color="#6b5536", weight="bold", rot=36)),
            (172.5, -42.33, "South Island", dict(size=8, style="italic", color="#6b5536", rot=36)),
            (171.0, -43.1, "Southern Alps", dict(size=8.5, style="italic", color="#6b5536", rot=38))],
    mountains=[(170.142, -43.595, "Aoraki", "Mt Cook")],
    places=[(174.763, -36.848, "Auckland", "Tāmaki Makaurau", "l", -0.12, 0.0),
            (175.10, -38.26, "Waitomo", "", "l", -0.1, 0.0),
            (176.252, -38.137, "Rotorua", "", "r", 0.1, 0.06),
            (176.369, -38.359, "Wai-O-Tapu", "", "r", 0.1, -0.06),
            (172.636, -43.532, "Christchurch", "Ōtautahi", "r", 0.12, 0.0),
            (170.477, -44.004, "Tekapo", "Takapō", "r", 0.1, 0.03),
            (170.15, -44.19, "Lake Pukaki", "", "r", 0.1, -0.1),
            (170.971, -45.097, "Oamaru", "Ōamaru", "r", 0.1, 0.02),
            (170.828, -45.345, "Moeraki", "", "r", 0.12, -0.03),
            (170.504, -45.874, "Dunedin", "Ōtepoti", "r", 0.12, -0.04),
            (168.833, -44.939, "Arrowtown", "", "r", 0.07, 0.11),
            (168.663, -45.031, "Queenstown", "Tāhuna", "c", 0.0, -0.17),
            (168.388, -44.851, "Glenorchy", "", "l", -0.06, 0.11)],
    me=[(170.10, -44.30, "Pelennor Fields", "right")],
    lons=[168, 170, 172, 174, 176, 178], lats=[-36, -38, -40, -42, -44, -46],
    lonfmt=deg("E"), latfmt=deg("S"),
    compass=(177.4, -45.55), scale=(176.4, -47.1, 100),
    title_box=(172.9, -47.35, 2.95, 1.75), title="AOTEAROA",
    subtitle="New Zealand, in search of Middle-earth",
    legend=[("place", "Places in this post"), ("road", "My route, by road"), ("air", "My route, by air"), ("me", "A Middle-earth filming site")],
)
draw(166.3, 178.8, -47.5, -34.2, 10.0, main, f"{OUTDIR}/nz-map.jpg")

