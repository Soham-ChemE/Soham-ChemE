#!/usr/bin/env python3
"""Build the landing page's assets.

  python docs/build_assets.py             # everything below
  python docs/build_assets.py --data      # docs/assets/data.js from the sibling repositories' docs/assets/data.js files
  python docs/build_assets.py --hero      # docs/assets/hero.svg: the animated README hero generated from the page's own particle shapes
  python docs/build_assets.py --hero-png  # docs/assets/hero.png, the static hero fallback, from the hero canvas
  python docs/build_assets.py --snap      # static PNG fallbacks for the six card thumbnails (both themes)
  python docs/build_assets.py --qa        # both-theme screenshots and console check into docs/qa/
  python docs/build_assets.py --lighthouse
  python docs/build_assets.py --preview   # docs/assets/social-preview.png

The README hero is built from the live page: docs/tools/page-qa.mjs opens the page headlessly, asks the hero scene for 300
particles of each of the six shapes projected through the scene's camera (window.__hero.project), and this script writes
them as circles whose CSS keyframes carry each particle through the six shapes. GitHub renders CSS animation inside an SVG
loaded through <img>; no SMIL, no scripts. Needs: pip install -r requirements.txt, a global playwright + Chromium, and the
lighthouse CLI for the Lighthouse step."""
from __future__ import annotations
import json, os, random, subprocess, sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent; ROOT = DOCS.parent; OUT = DOCS / "assets"; PARENT = ROOT.parent
TOOL = [str(DOCS / "tools" / "page-qa.mjs"), "--docs", str(DOCS), "--pages", "index.html"]


def run(cmd, cwd=ROOT):
    print("$", " ".join(cmd)); subprocess.run(cmd, cwd=cwd, check=True)


# ---------------- scene data from the sibling repositories ----------------
def sibling_data(repo):
    p = PARENT / repo / "docs" / "assets" / "data.js"
    if not p.exists(): return None
    s = p.read_text(encoding="utf-8"); s = s[s.index("=") + 1:].strip().rstrip(";"); return json.loads(s)


def build_data():
    snap_path = OUT / "data.js"; snap = {}; old = None
    if snap_path.exists():
        t = snap_path.read_text(encoding="utf-8"); old = json.loads(t[t.index("=") + 1:].strip().rstrip(";"))
    rng = random.Random(0)
    ca = sibling_data("CathodeAI-Battery-Materials-Screener")
    if ca:
        idx = sorted(rng.sample(range(len(ca["materials"])), 320))
        snap["cathodeai"] = {"points": [[ca["materials"][i][1], round(ca["materials"][i][2] * 1000, 1), ca["materials"][i][3], ca["materials"][i][4]] for i in idx],
                             "validation": [[v["name"], v["dv"], round(v["eh"] * 1000, 1), v["bg"], v["cat"]] for v in ca["validation"] if "dv" in v], "n": len(ca["materials"]), "rho": ca["stats"]["rho"], "source": "CathodeAI docs/assets/data.js: 320 of 787 materials (seeded sample) and the 11 validation cathodes"}
    lmo = sibling_data("LMO-Cathode-Rate-Model-PyBaMM")
    if lmo:
        snap["lmo"] = {"curves": [{"rate": c["rate"], "measured": c["measured"][::3], "model": c["model"][::3]} for c in lmo["curves"]], "shares": lmo["stats"]["shares"], "train_rmse_mV": lmo["stats"]["train_rmse_mV"], "two_c_v_err_mV": lmo["stats"]["two_c_v_err_mV"], "source": "LMO docs/assets/data.js: the four measured and modelled discharge curves, every third point"}
    cvd = sibling_data("CVD-Reactor-Uniformity-COMSOL")
    if cvd:
        snap["cvd"] = {"before": cvd["profiles"]["before"]["rc"][::2], "after": cvd["profiles"]["after"]["rc"][::2], "optimum": cvd["profiles"]["optimum"]["rc"][::2], "sigma": [cvd["stats"]["sigma_before"], cvd["stats"]["sigma_after"], cvd["stats"]["sigma_opt"]], "source": "CVD docs/assets/data.js: the three wafer-plane profiles, every second point"}
    md = sibling_data("MD-IL-CNT-Interfacial-Interactions")
    if md:
        A = md["atoms"]; keep = [i for i in range(len(A["t"])) if abs(A["z"][i]) < 5 and A["t"][i] != 3]
        snap["md"] = {"atoms": [[A["x"][i], A["y"][i], A["z"][i], A["t"][i]] for i in keep], "n_total": md["stats"]["n_atoms"], "cnt_radius_A": md["stats"]["cnt_radius_A"], "source": "MD docs/assets/data.js: the non-hydrogen atoms within 5 Å of the tube mid-plane (%d of 19,260)" % len(keep)}
    sc_ = sibling_data("Perovskite-Solar-Cell-SCAPS1D-Optimization")
    if sc_:
        snap["scaps"] = {"stack": sc_["stack"], "ranking": [[r[0], r[5]] for r in sc_["ranking"]], "best_pce": sc_["stats"]["best_pce"], "source": "SCAPS docs/assets/data.js: the layer stack and the ten-ETL ranking"}
    tr = sibling_data("4680-Thermal-Runaway-Propagation-COMSOL")
    if tr:
        key = tr["lumped"]["trace_cascade"]; t = tr["lumped"]["traces"][key]
        snap["tr4680"] = {"runs": [[r["h_plate"], r["k_tl"], r["outcome"], r["status"]] for r in tr["matrix"]["runs"]], "ignition_min": t["ignition_min"], "t_min": t["t_min"][::6], "cell_max_C": t["cell_max_C"][::6], "source": "4680 docs/assets/data.js: the COMSOL run matrix and the reduced-order model's cascade trace (k_tl = 1.0, h = 2,000), every sixth sample"}
    if old:
        for k, v in old.items(): snap.setdefault(k, v)   # keep a committed excerpt when a sibling clone is absent
    with open(snap_path, "w", encoding="utf-8") as f:
        f.write("// Generated by docs/build_assets.py from the sibling repositories' docs/assets/data.js files (each built from that project's raw data). Do not edit by hand.\n")
        f.write("window.PROFILE = " + json.dumps(snap, separators=(",", ":")) + ";\n")
    print("data.js:", {k: len(json.dumps(v)) for k, v in snap.items()}, snap_path.stat().st_size, "bytes")


# ---------------- animated README hero from the page's own particle shapes ----------------
HEAD = [("2,774", "cathodes screened", "#22d3ee"), ("26 mV", "PyBaMM fit, own data", "#f97316"), ("180 → 3.3 %", "CVD non-uniformity", "#fb7185"), ("−8.75 kcal/mol", "IL binding at the CNT wall", "#a78bfa"), ("27.99 %", "simulated ZnSe/CdTe cell", "#f59e0b"), ("1.0 → 1.25 W/m·K", "4680 cascade threshold", "#f97316")]


def build_hero():
    shapes_path = OUT / "hero_shapes.json"
    run(["node", *TOOL, "--hero-json", str(shapes_path)])
    shapes = json.loads(shapes_path.read_text()); K = len(shapes); n = min(len(s["points"]) for s in shapes)
    # stage: right half of the banner; particle p of shape i is the p-th sampled particle of that shape (same particle id across shapes)
    X0, Y0, W, H = 860, 40, 700, 420; loop = K * 4.0; hold, travel = 2.6, 1.4
    css, circles = [], []
    for p in range(n):
        frames = []
        for i, s in enumerate(shapes):
            x, y, c = s["points"][p]; px, py = X0 + x * W, Y0 + y * H
            t0 = (i * (hold + travel)) / loop * 100; t1 = (i * (hold + travel) + hold) / loop * 100
            col = "#%02x%02x%02x" % tuple(int(max(0, min(1, v)) * 255) for v in c)
            frames.append(f"{t0:.2f}%{{transform:translate({px:.1f}px,{py:.1f}px);fill:{col}}}{t1:.2f}%{{transform:translate({px:.1f}px,{py:.1f}px);fill:{col}}}")
        x, y, c = shapes[0]["points"][p]; col0 = "#%02x%02x%02x" % tuple(int(max(0, min(1, v)) * 255) for v in c)
        frames.append(f"100%{{transform:translate({X0 + x * W:.1f}px,{Y0 + y * H:.1f}px);fill:{col0}}}")
        css.append(f"@keyframes p{p}{{{''.join(frames)}}}.p{p}{{animation-name:p{p}}}")
        circles.append(f'<circle class="pt p{p}" r="2.3" fill="{col0}" transform="translate({X0 + x * W:.1f},{Y0 + y * H:.1f})"/>')
    stats = "".join(f'<g class="st s{i}"><text x="80" y="300" class="big" fill="{c}">{a}</text><text x="80" y="332" class="small">{b}</text><text x="80" y="356" class="small">{shapes[i]["name"]}</text></g>' for i, (a, b, c) in enumerate(HEAD))
    st_css = "".join(f".s{i}{{animation-delay:{i * (hold + travel):.1f}s}}" for i in range(K))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 500" width="1600" height="500" role="img" aria-label="Soham Kavathekar: one cloud of particles morphing between six shapes built from six projects' own data, next to each project's headline number">
<style>
.t{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
.h{{font-size:44px;font-weight:800;fill:#e6edf3;letter-spacing:-1.5px}}.sub{{font-size:19px;fill:#8b98a9}}.k{{font-size:14px;fill:#8b98a9;letter-spacing:2px}}.big{{font-size:34px;font-weight:800}}.small{{font-size:16px;fill:#8b98a9}}.foot{{font-size:14px;fill:#5b6676}}
.pt{{animation-duration:{loop:.0f}s;animation-timing-function:ease-in-out;animation-iteration-count:infinite;opacity:.9}}
{''.join(css)}
.st{{opacity:0;animation:cycle {loop:.0f}s infinite}}{st_css}
@keyframes cycle{{0%{{opacity:0}}4%{{opacity:1}}{hold / loop * 100:.1f}%{{opacity:1}}{(hold + travel * .6) / loop * 100:.1f}%{{opacity:0}}100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.pt,.st{{animation:none}}.s0{{opacity:1}}}}
</style>
<rect width="1600" height="500" fill="#0a0a0b"/>
<g class="t">
<text x="80" y="76" class="k">SOHAM KAVATHEKAR · MS CHEMICAL &amp; BIOMOLECULAR ENGINEERING · UNIVERSITY OF PENNSYLVANIA</text>
<text x="80" y="146" class="h">Energy materials and process engineering,</text><text x="80" y="200" class="h">with models that survive being re-run.</text>
<text x="80" y="244" class="sub">Six projects, each with a live 3D page and an audit trail from claim to script.</text>
{stats}
<text x="80" y="440" class="foot">The particles are the same six shapes the live page morphs between, built from each project's own data.</text>
<text x="80" y="464" class="foot">github.com/Soham-ChemE · soham-cheme.github.io/Soham-ChemE</text>
</g>
<g>{''.join(circles)}</g>
</svg>'''
    (OUT / "hero.svg").write_text(svg, encoding="utf-8"); print("wrote hero.svg", (OUT / "hero.svg").stat().st_size, "bytes,", n, "particles per shape")


# ---------------- social preview ----------------
def build_preview():
    from PIL import Image, ImageDraw, ImageFont
    COLS = ["#22d3ee", "#f97316", "#fb7185", "#a78bfa", "#f59e0b", "#f97316"]; BG = "#0a0a0b"
    im = Image.new("RGB", (1280, 640), BG); d = ImageDraw.Draw(im)
    for i, c in enumerate(COLS): d.rectangle([i * 214, 0, (i + 1) * 214, 18], fill=c)
    def font(sz, bold=True):
        for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]:
            try: return ImageFont.truetype(f, sz)
            except Exception: pass
        return ImageFont.load_default()
    d.text((70, 80), "SOHAM KAVATHEKAR", fill="#8b98a9", font=font(22))
    d.text((70, 130), "Energy materials and process engineering,", fill="#e6edf3", font=font(46)); d.text((70, 190), "with models that survive being re-run.", fill="#e6edf3", font=font(46))
    d.text((70, 275), "MS Chemical & Biomolecular Engineering, University of Pennsylvania  ·  batteries  ·  semiconductor processing", fill="#c9d4e2", font=font(20, False))
    labels = [("2,774", "cathodes screened"), ("26 mV", "PyBaMM fit, own data"), ("180 → 3.3 %", "CVD non-uniformity"), ("−8.75 kcal/mol", "IL binding at CNT wall"), ("27.99 %", "simulated ZnSe/CdTe"), ("1.0 → 1.25", "W/m·K, 4680 threshold")]
    for i, (big, small) in enumerate(labels):
        x = 70 + i * 196; d.rectangle([x, 380, x + 170, 384], fill=COLS[i]); d.text((x, 400), big, fill="#e6edf3", font=font(26)); d.text((x, 440), small, fill="#8b98a9", font=font(14, False))
    d.text((70, 560), "github.com/Soham-ChemE  ·  soham-cheme.github.io/Soham-ChemE", fill="#8b98a9", font=font(18, False))
    im.save(OUT / "social-preview.png", optimize=True); print("wrote social-preview.png")


def quantise(paths, colors=256, max_w=1400):
    from PIL import Image
    for p in paths:
        im = Image.open(p).convert("RGBA")
        if im.width > max_w: im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        q = im.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG); q.save(p, optimize=True); print("quantised", p.name, p.stat().st_size, "bytes")


def qa_readme(report):
    lines = ["# QA for the live page", "", "Served from docs/ by docs/tools/page-qa.mjs, loaded in headless Chromium (software WebGL, so frame timing is not representative). Screenshots in both themes: the hero, the first two body scenes, the 375 px hero.", ""]
    for page, pr in report.get("pages", {}).items():
        lines += [f"## {page}", ""]
        if "lighthouse" in pr:
            lh = pr["lighthouse"]; lines += [f"Lighthouse (desktop preset): performance {lh['performance']}, accessibility {lh['accessibility']}, best practices {lh['bestPractices']}, SEO {lh['seo']}", "", "| Metric | Value |", "|---|---|", f"| First Contentful Paint | {lh['fcp']} |", f"| Largest Contentful Paint | {lh['lcp']} |", f"| Speed Index | {lh['si']} |", f"| Total Blocking Time | {lh['tbt']} |", f"| Cumulative Layout Shift | {lh['cls']} |", f"| Total byte weight | {lh['bytes']} |", ""]
        lines += ["| Theme | Console errors | Failed requests | Images loaded | Transfer (bytes) | Body scenes captured |", "|---|---|---|---|---|---|"]
        for theme in ("dark", "light"):
            t = pr.get(theme)
            if t: lines.append(f"| {theme} | {len(t['errors']) + len(t.get('mobileErrors', []))} | {len(t['failed'])} | {t['imagesLoaded']} | {t['transferBytes']:,} | {', '.join(t['scenes'])} |")
        lines.append("")
    lines += ["Files: `light/` and `dark/` hold `index-hero.png`, `index-scene1-*.png`, `index-scene2-*.png` and `index-mobile-375-hero.png`; `lighthouse.report.html` and `.json` are the Lighthouse run; `qa.json` is the machine-readable summary."]
    (DOCS / "qa" / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv):
    only = [a for a in argv if a.startswith("--")]; do_all = not only
    if do_all or "--data" in only: build_data()
    if do_all or "--preview" in only: build_preview()
    if do_all or "--hero" in only: build_hero()
    if do_all or "--hero-png" in only:
        run(["node", *TOOL, "--hero-png"]); quantise([OUT / "hero.png"], max_w=1600)
    if do_all or "--snap" in only:
        run(["node", *TOOL, "--snap"]); quantise(sorted(OUT.glob("viz_*_*.png")))
    flags = [f for f in ("--qa", "--lighthouse") if do_all or f in only]
    if flags:
        run(["node", *TOOL, *flags]); qa_readme(json.loads((DOCS / "qa" / "qa.json").read_text()))


if __name__ == "__main__":
    main(sys.argv[1:])
