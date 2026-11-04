"""Build the landing page's assets: card thumbnails from the five project pages' hero renders and a 1280x640 social preview.

Reads docs/assets/hero.png from each sibling project clone (../<repo>/docs/assets/hero.png, produced by each repo's own
page render) when present; otherwise skips that card image. Writes docs/assets/card_*.png and docs/assets/social-preview.png.
Run from the repository root:  python docs/build_assets.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, "docs", "assets"); os.makedirs(OUT, exist_ok=True)
PARENT = os.path.dirname(ROOT)
CARDS = {"cathodeai": "CathodeAI-Battery-Materials-Screener", "lmo": "LMO-Cathode-Rate-Model-PyBaMM", "cvd": "CVD-Reactor-Uniformity-COMSOL", "md": "MD-IL-CNT-Interfacial-Interactions", "scaps": "Perovskite-Solar-Cell-SCAPS1D-Optimization", "tr4680": "4680-Thermal-Runaway-Propagation-COMSOL"}
for key, repo in CARDS.items():
    src = os.path.join(PARENT, repo, "docs", "assets", "hero.png")
    if not os.path.exists(src):
        print("skip", key, "(no", src + ")"); continue
    im = Image.open(src).convert("RGB"); w, h = im.size; im = im.crop((0, int(h * .06), w, h)).resize((960, 480), Image.LANCZOS)
    im.quantize(colors=128, method=Image.Quantize.MEDIANCUT).save(os.path.join(OUT, f"card_{key}.png"), optimize=True); print("wrote card_%s.png" % key)

COLS = ["#22d3ee", "#ff7a1a", "#f43f5e", "#a78bfa", "#f59e0b"]; BG = "#0a0a0b"
im = Image.new("RGB", (1280, 640), BG); d = ImageDraw.Draw(im)
for i, c in enumerate(COLS): d.rectangle([i * 256, 0, (i + 1) * 256, 18], fill=c)
def font(sz, bold=True):
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]:
        try: return ImageFont.truetype(f, sz)
        except Exception: pass
    return ImageFont.load_default()
d.text((70, 80), "SOHAM KAVATHEKAR", fill="#8b98a9", font=font(22))
d.text((70, 130), "Energy materials and process engineering,", fill="#e6edf3", font=font(46)); d.text((70, 190), "with models that survive being re-run.", fill="#e6edf3", font=font(46))
d.text((70, 275), "MS Chemical & Biomolecular Engineering, University of Pennsylvania  ·  batteries  ·  semiconductor processing", fill="#c9d4e2", font=font(20, False))
labels = [("2,774", "cathodes screened"), ("26 mV", "PyBaMM fit, own data"), ("180 → 3.3 %", "CVD non-uniformity"), ("−8.75 kcal/mol", "IL binding at CNT wall"), ("27.99 %", "simulated ZnSe/CdTe cell")]
for i, (big, small) in enumerate(labels):
    x = 70 + i * 232; d.rectangle([x, 380, x + 200, 384], fill=COLS[i]); d.text((x, 400), big, fill="#e6edf3", font=font(30)); d.text((x, 445), small, fill="#8b98a9", font=font(16, False))
d.text((70, 560), "github.com/Soham-ChemE  ·  soham-cheme.github.io/Soham-ChemE", fill="#8b98a9", font=font(18, False))
im.save(os.path.join(OUT, "social-preview.png"), optimize=True); print("wrote social-preview.png")

# ---------------- scene snapshot for the landing page's hero (docs/assets/data.js) ----------------
# The hero threads the six project scenes together. Each vignette is drawn from a small excerpt of that project's own
# page data (docs/assets/data.js in the sibling clone, itself generated from the project's raw data), so the shapes on
# the landing page are the real ones, not illustrations. The excerpt is committed so the page builds without the siblings.
import json, re, random
def sibling_data(repo, varname):
    p = os.path.join(PARENT, repo, "docs", "assets", "data.js")
    if not os.path.exists(p): return None
    s = open(p, encoding="utf-8").read(); s = s[s.index("=") + 1:].strip().rstrip(";")
    return json.loads(s)
snap_path = os.path.join(OUT, "data.js"); snap = {}
old = None
if os.path.exists(snap_path):
    t = open(snap_path, encoding="utf-8").read(); old = json.loads(t[t.index("=") + 1:].strip().rstrip(";"))
rng = random.Random(0)
ca = sibling_data("CathodeAI-Battery-Materials-Screener", "CATHODEAI")
if ca:
    idx = sorted(rng.sample(range(len(ca["materials"])), 320))
    snap["cathodeai"] = {"points": [[ca["materials"][i][1], round(ca["materials"][i][2] * 1000, 1), ca["materials"][i][3], ca["materials"][i][4]] for i in idx],
                         "validation": [[v["name"], v["dv"], round(v["eh"] * 1000, 1), v["bg"], v["cat"]] for v in ca["validation"] if "dv" in v], "n": len(ca["materials"]), "rho": ca["stats"]["rho"], "source": "CathodeAI docs/assets/data.js: 320 of 787 materials (seeded sample) and the 11 validation cathodes"}
lmo = sibling_data("LMO-Cathode-Rate-Model-PyBaMM", "LMO")
if lmo:
    snap["lmo"] = {"curves": [{"rate": c["rate"], "measured": c["measured"][::3], "model": c["model"][::3]} for c in lmo["curves"]], "shares": lmo["stats"]["shares"], "train_rmse_mV": lmo["stats"]["train_rmse_mV"], "two_c_v_err_mV": lmo["stats"]["two_c_v_err_mV"], "source": "LMO docs/assets/data.js: the four measured and modelled discharge curves, every third point"}
cvd = sibling_data("CVD-Reactor-Uniformity-COMSOL", "CVD")
if cvd:
    snap["cvd"] = {"before": cvd["profiles"]["before"]["rc"][::2], "after": cvd["profiles"]["after"]["rc"][::2], "optimum": cvd["profiles"]["optimum"]["rc"][::2], "sigma": [cvd["stats"]["sigma_before"], cvd["stats"]["sigma_after"], cvd["stats"]["sigma_opt"]], "source": "CVD docs/assets/data.js: the three wafer-plane profiles, every second point"}
md = sibling_data("MD-IL-CNT-Interfacial-Interactions", "MD")
if md:
    A = md["atoms"]; keep = [i for i in range(len(A["t"])) if abs(A["z"][i]) < 5 and A["t"][i] != 3]
    snap["md"] = {"atoms": [[A["x"][i], A["y"][i], A["z"][i], A["t"][i]] for i in keep], "n_total": md["stats"]["n_atoms"], "cnt_radius_A": md["stats"]["cnt_radius_A"], "source": "MD docs/assets/data.js: the non-hydrogen atoms within 5 Å of the tube mid-plane (%d of 19,260)" % len(keep)}
sc_ = sibling_data("Perovskite-Solar-Cell-SCAPS1D-Optimization", "SCAPS")
if sc_:
    snap["scaps"] = {"stack": sc_["stack"], "ranking": [[r[0], r[5]] for r in sc_["ranking"]], "best_pce": sc_["stats"]["best_pce"], "source": "SCAPS docs/assets/data.js: the layer stack and the ten-ETL ranking"}
tr = sibling_data("4680-Thermal-Runaway-Propagation-COMSOL", "TR4680")
if tr:
    key = tr["lumped"]["trace_cascade"]; t = tr["lumped"]["traces"][key]
    snap["tr4680"] = {"runs": [[r["h_plate"], r["k_tl"], r["outcome"], r["status"]] for r in tr["matrix"]["runs"]], "ignition_min": t["ignition_min"], "t_min": t["t_min"][::6], "cell_max_C": t["cell_max_C"][::6], "source": "4680 docs/assets/data.js: the COMSOL run matrix and the surrogate's cascade trace (k_tl = 1.0, h = 2,000), every sixth sample"}
if old:
    for k, v in old.items(): snap.setdefault(k, v)   # keep a committed excerpt when a sibling clone is absent
with open(snap_path, "w", encoding="utf-8") as f:
    f.write("// Generated by docs/build_assets.py from the sibling repositories' docs/assets/data.js files (each built from that project's raw data). Do not edit by hand.\n")
    f.write("window.PROFILE = " + json.dumps(snap, separators=(",", ":")) + ";\n")
print("data.js:", {k: len(json.dumps(v)) for k, v in snap.items()}, os.path.getsize(snap_path), "bytes")

# ---------------- animated README hero (SVG with CSS keyframes; GitHub renders these through <img>) ----------------
# Six small marks, one per project, drawn from the same excerpt as the page: the CathodeAI points, the LMO curves, the CVD
# profile, the MD atoms, the SCAPS bars and the 4680 pack. Each lights up in turn. No SMIL, no scripts, no fonts.
def _vir(t):
    s = [(68, 1, 84), (59, 82, 139), (33, 145, 140), (94, 201, 98), (253, 231, 37)]; t = max(0, min(1, t)) * 4; i = int(t); f = t - i; a = s[i]; b = s[min(i + 1, 4)]
    return "#%02x%02x%02x" % tuple(int(a[k] + (b[k] - a[k]) * f) for k in range(3))
TILE_W, TILE_H, X0, Y0, GAPX = 220, 170, 180, 300, 16
tiles = []; titles = [("CathodeAI", "2,774 cathodes screened", "#22d3ee"), ("LMO rate model", "26 mV fit, own data", "#ff7a1a"), ("CVD reactor", "180 → 3.3 % non-uniformity", "#f43f5e"), ("IL / CNT MD", "−8.75 kcal/mol at the wall", "#a78bfa"), ("SCAPS-1D cell", "27.99 % simulated", "#f59e0b"), ("4680 pack", "1.0 → 1.25 W/m·K threshold", "#f97316")]
def tile(i, inner):
    x = X0 + i * (TILE_W + GAPX); t, sub_, col = titles[i]
    return f'<g class="tile t{i}"><rect x="{x}" y="{Y0}" width="{TILE_W}" height="{TILE_H}" rx="14" fill="#111115" stroke="{col}" stroke-opacity=".5"/><g transform="translate({x},{Y0})">{inner}</g><text class="t tt" x="{x + 12}" y="{Y0 + TILE_H + 24}" fill="{col}">{t}</text><text class="t ts" x="{x + 12}" y="{Y0 + TILE_H + 42}">{sub_}</text></g>'
inner = []
if "cathodeai" in snap:
    P = snap["cathodeai"]["points"]; inner.append("".join(f'<circle cx="{14 + min(p[0], 20) / 20 * 192:.1f}" cy="{{:.1f}}" r="2.4" fill="{_vir(p[3])}" opacity=".8"/>'.format(156 - min(p[1], 300) / 300 * 140) for p in P))
else: inner.append("")
if "lmo" in snap:
    RC = {"C/10": "#22d3ee", "C/5": "#34d399", "C/2": "#f59e0b", "2C": "#f87171"}; s_ = ""
    for c in snap["lmo"]["curves"]:
        s_ += '<path d="M ' + " L ".join(f"{14 + min(q, 1.5) / 1.5 * 192:.1f} {156 - (min(max(v, 3.5), 4.5) - 3.5) * 140:.1f}" for q, v in c["measured"]) + f'" fill="none" stroke="{RC[c["rate"]]}" stroke-width="2.5"/>'
    inner.append(s_)
else: inner.append("")
if "cvd" in snap:
    s_ = ""
    for k, col in (("before", "#f87171"), ("optimum", "#34d399")):
        s_ += '<path d="M ' + " L ".join(f"{14 + r / 138 * 192:.1f} {156 - min(c, 1.6) / 1.6 * 140:.1f}" for r, c in snap["cvd"][k]) + f'" fill="none" stroke="{col}" stroke-width="2.5"/>'
    inner.append(s_)
else: inner.append("")
if "md" in snap:
    A = snap["md"]["atoms"]; colm = {0: "#8b98a9", 1: "#a78bfa", 2: "#60a5fa", 4: "#34d399", 5: "#6ee7b7"}
    inner.append("".join(f'<circle cx="{110 + a[0] * 3.1:.1f}" cy="{85 - a[1] * 3.1:.1f}" r="1.8" fill="{colm.get(a[3], "#8b98a9")}"/>' for a in A if abs(a[0]) < 31 and abs(a[1]) < 26))
else: inner.append("")
if "scaps" in snap:
    rk = snap["scaps"]["ranking"]; bw = 192 / len(rk)
    inner.append("".join(f'<rect x="{14 + i * bw + 2:.1f}" y="{156 - max(2, r[1] / 28 * 140):.1f}" width="{bw - 4:.1f}" height="{max(2, r[1] / 28 * 140):.1f}" rx="2" fill="{"#f87171" if i == 0 else "#f59e0b" if r[1] > 20 else "#22d3ee" if r[1] > 5 else "#64748b"}"/>' for i, r in enumerate(rk)))
else: inner.append("")
if "tr4680" in snap:
    ign = snap["tr4680"]["ignition_min"]; s_ = ""
    for c in range(20):
        ix, iy = c % 5, c // 5; cx_, cy_ = 30 + ix * 40, 30 + iy * 37
        s_ += f'<circle cx="{cx_}" cy="{cy_}" r="15" fill="#334155"/>' + (f'<circle class="ig" style="animation-delay:{(ign[c] or 0) / 12:.2f}s" cx="{cx_}" cy="{cy_}" r="15" fill="#f97316"/>' if ign[c] is not None else "")
    inner.append(s_)
else: inner.append("")
tiles_svg = "".join(tile(i, inner[i]) for i in range(6))
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 500" width="1600" height="500" role="img" aria-label="Soham Kavathekar: six project marks drawn from each project's own data, lighting up in turn">
<style>
.t{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
.h{{font-size:46px;font-weight:800;fill:#e6edf3;letter-spacing:-1.5px}}.sub{{font-size:20px;fill:#8b98a9}}.k{{font-size:14px;fill:#8b98a9;letter-spacing:2px}}.tt{{font-size:15px;font-weight:800}}.ts{{font-size:12px;fill:#8b98a9}}
.tile{{opacity:.45;animation:lit 18s infinite}}{"".join(f".t{i}{{animation-delay:{i * 3}s}}" for i in range(6))}
@keyframes lit{{0%{{opacity:.45}}3%{{opacity:1}}16%{{opacity:1}}20%{{opacity:.45}}100%{{opacity:.45}}}}
.ig{{opacity:0;animation:ign 18s infinite}}@keyframes ign{{0%,83%{{opacity:0}}85%,98%{{opacity:1}}100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.tile,.ig{{animation:none;opacity:1}}}}
</style>
<rect width="1600" height="500" fill="#0a0a0b"/>
<g class="t">
<text x="180" y="70" class="k">SOHAM KAVATHEKAR · MS CHEMICAL &amp; BIOMOLECULAR ENGINEERING · UNIVERSITY OF PENNSYLVANIA</text>
<text x="180" y="140" class="h">Energy materials and process engineering,</text><text x="180" y="196" class="h">with models that survive being re-run.</text>
<text x="180" y="240" class="sub">Six projects, each with a live 3D page and an audit trail from claim to script. The marks below are drawn from their own data.</text>
</g>
{tiles_svg}
</svg>"""
with open(os.path.join(OUT, "hero.svg"), "w", encoding="utf-8") as f: f.write(svg)
print("wrote hero.svg", os.path.getsize(os.path.join(OUT, "hero.svg")), "bytes")
