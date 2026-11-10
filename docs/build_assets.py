#!/usr/bin/env python3
"""Build the landing page's assets.

  python docs/build_assets.py             # everything below
  python docs/build_assets.py --data      # docs/assets/data.js from the sibling repositories' docs/assets/data.js files
  python docs/build_assets.py --hero      # docs/assets/hero.svg: the animated README hero generated from the page's own particle shapes
  python docs/build_assets.py --hero-shapes  # same, but re-project the shapes from the live page first even if hero_shapes.json is fresh
  python docs/build_assets.py --hero-png  # docs/assets/hero.png, the static hero fallback, from the hero canvas
  python docs/build_assets.py --snap      # static PNG fallbacks for the seven card thumbnails (both themes)
  python docs/build_assets.py --qa        # both-theme screenshots and console check into docs/qa/
  python docs/build_assets.py --lighthouse
  python docs/build_assets.py --preview   # docs/assets/social-preview.png

The README hero is built from the live page: docs/tools/page-qa.mjs (node) or docs/tools/hero_shapes.py (Python Playwright)
opens the page headlessly, asks the hero scene for 300 particles of each of the seven shapes projected through the scene's
camera (window.__hero.project) and writes docs/assets/hero_shapes.json; this script writes them as circles whose CSS
keyframes carry each particle through the seven shapes. GitHub renders CSS animation inside an SVG loaded through <img>; no
SMIL, no scripts. --hero reuses hero_shapes.json when it is newer than scene.js and data.js, otherwise it regenerates it with
node + the global playwright, falling back to the Python tool. Needs: pip install -r requirements.txt, playwright + Chromium
(node or Python), and the lighthouse CLI for the Lighthouse step."""
from __future__ import annotations
import json, os, random, subprocess, sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent; ROOT = DOCS.parent; OUT = DOCS / "assets"; PARENT = ROOT.parent
TOOL = [str(DOCS / "tools" / "page-qa.mjs"), "--docs", str(DOCS), "--pages", "index.html"]
PYTOOL = [sys.executable, str(DOCS / "tools" / "hero_shapes.py"), "--docs", str(DOCS)]
# Sibling repositories normally sit next to this clone (PARENT/<repo>); a repository kept elsewhere is listed here by its data.js path.
SIBLING_PATHS = {"ald-conformality": [Path("/Users/thegreat/Documents/MATLAB/ald-conformality/docs/assets/data.js")]}


def run(cmd, cwd=ROOT):
    print("$", " ".join(cmd)); subprocess.run(cmd, cwd=cwd, check=True)


# ---------------- scene data from the sibling repositories ----------------
def sibling_data(repo):
    for p in [PARENT / repo / "docs" / "assets" / "data.js", *SIBLING_PATHS.get(repo, [])]:
        if p.exists():
            s = p.read_text(encoding="utf-8"); s = s[s.index("=") + 1:].strip().rstrip(";"); return json.loads(s)
    return None


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
    ald = sibling_data("ald-conformality")
    if ald:
        H = ald["hero"]; hole = H["hole"]; r3 = lambda v: round(v, 3); every = 10   # 221 chamber times -> 23
        ti = list(range(0, len(H["times"]), every))
        snap["ald"] = {"hole": {"depths": hole["depths"], "times": hole["times"], "theta": [[r3(v) for v in row] for row in hole["theta"]]},
                       "cov": {"times": [H["times"][i] for i in ti], "radii_mm": H["radii_mm"], "thetaFlat": [[r3(v) for v in H["cov"]["thetaFlat"][i]] for i in ti], "thetaBottom": [[r3(v) for v in H["cov"]["thetaBottom"][i]] for i in ti]},
                       "map": [[r["kind"], r["x"], r["AR"], r["t90_worst"], r3(r["t_supply"])] for r in ald["map"]["rows"]],
                       "blanket_t90": ald["stats"]["blanket_t90"], "patterned_t90": ald["stats"]["patterned_t90"], "wall_ratio": ald["stats"]["wall_ratio"], "underdose": ald["stats"]["underdose"], "rule_band": ald["stats"]["rule_band"], "blanket_band": ald["stats"]["blanket_band"],
                       "source": "ald-conformality docs/assets/data.js: the AR-100 hole's coverage-depth profile at 19 pulse times, the chamber run's flat and hole-bottom coverage against wafer radius at every tenth time step (23 of 221), the 16-row pulse-time map (kind, TMA fraction, AR, worst-point t90, supply limit) and the headline statistics"}
    if old:
        for k, v in old.items(): snap.setdefault(k, v)   # keep a committed excerpt when a sibling clone is absent
    with open(snap_path, "w", encoding="utf-8") as f:
        f.write("// Generated by docs/build_assets.py from the sibling repositories' docs/assets/data.js files (each built from that project's raw data). Do not edit by hand.\n")
        f.write("window.PROFILE = " + json.dumps(snap, separators=(",", ":")) + ";\n")
    print("data.js:", {k: len(json.dumps(v)) for k, v in snap.items()}, snap_path.stat().st_size, "bytes")


# ---------------- animated README hero from the page's own particle shapes ----------------
HEAD = [("2,774", "cathodes screened", "#22d3ee"), ("26 mV", "PyBaMM fit, own data", "#f97316"), ("180 → 3.3 %", "CVD non-uniformity", "#fb7185"), ("−8.75 kcal/mol", "IL binding at the CNT wall", "#a78bfa"), ("27.99 %", "simulated ZnSe/CdTe cell", "#f59e0b"), ("1.0 → 1.25 W/m·K", "4680 cascade threshold", "#f97316"), ("0.35 s → 14 s", "ALD pulse, blanket vs 3D-NAND wafer", "#34d399")]


def hero_shapes(shapes_path, force=False):
    """docs/assets/hero_shapes.json: 300 projected particles per shape from the live page. Reused when newer than the scene and
    its data; otherwise regenerated with node + global playwright, or with the Python Playwright tool when node is unavailable."""
    deps = [OUT / "scene.js", OUT / "data.js", OUT / "three-kit.js"]
    if not force and shapes_path.exists() and shapes_path.stat().st_mtime >= max(d.stat().st_mtime for d in deps if d.exists()):
        print("hero_shapes.json is newer than scene.js and data.js; reusing it"); return
    try: run(["node", *TOOL, "--hero-json", str(shapes_path)])
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print("node tool unavailable (%s); using the Python Playwright tool" % e); run([*PYTOOL, "--hero-json", str(shapes_path)])


def build_hero(force=False):
    shapes_path = OUT / "hero_shapes.json"; hero_shapes(shapes_path, force)
    shapes = json.loads(shapes_path.read_text()); K = len(shapes); n = min(len(s["points"]) for s in shapes)
    assert K == len(HEAD), "HEAD has %d captions for %d shapes" % (len(HEAD), K)
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
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 500" width="1600" height="500" role="img" aria-label="Soham Kavathekar: one cloud of particles morphing between seven shapes built from seven projects' own data, next to each project's headline number">
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
<text x="80" y="244" class="sub">Seven projects, each with a live 3D page and an audit trail from claim to script.</text>
{stats}
<text x="80" y="440" class="foot">The particles are the same seven shapes the live page morphs between, built from each project's own data.</text>
<text x="80" y="464" class="foot">github.com/Soham-ChemE · soham-cheme.github.io/Soham-ChemE</text>
</g>
<g>{''.join(circles)}</g>
</svg>'''
    (OUT / "hero.svg").write_text(svg, encoding="utf-8"); print("wrote hero.svg", (OUT / "hero.svg").stat().st_size, "bytes,", n, "particles per shape")


# ---------------- social preview ----------------
def build_preview():
    from PIL import Image, ImageDraw, ImageFont
    COLS = ["#22d3ee", "#f97316", "#fb7185", "#a78bfa", "#f59e0b", "#f97316", "#34d399"]; BG = "#0a0a0b"; K = len(COLS)
    im = Image.new("RGB", (1280, 640), BG); d = ImageDraw.Draw(im)
    for i, c in enumerate(COLS): d.rectangle([round(i * 1280 / K), 0, round((i + 1) * 1280 / K), 18], fill=c)
    def font(sz, bold=True):
        cands = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "DejaVuSans-Bold.ttf"] if bold else ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf", "DejaVuSans.ttf"]
        for f in cands:
            try: return ImageFont.truetype(f, sz)
            except Exception: pass
        return ImageFont.load_default()
    d.text((70, 80), "SOHAM KAVATHEKAR", fill="#8b98a9", font=font(22))
    d.text((70, 130), "Energy materials and process engineering,", fill="#e6edf3", font=font(46)); d.text((70, 190), "with models that survive being re-run.", fill="#e6edf3", font=font(46))
    d.text((70, 275), "MS Chemical & Biomolecular Engineering, University of Pennsylvania  ·  batteries  ·  semiconductor processing", fill="#c9d4e2", font=font(20, False))
    # seven labels across 1280 px: 70 px margins, 163 px pitch, 142 px bar
    labels = [("2,774", "cathodes screened"), ("26 mV", "PyBaMM fit, own data"), ("180 → 3.3 %", "CVD non-uniformity"), ("−8.75", "kcal/mol, IL at CNT wall"), ("27.99 %", "simulated ZnSe/CdTe"), ("1.0 → 1.25", "W/m·K, 4680 threshold"), ("0.35 → 14 s", "ALD pulse, 56× wall area")]
    assert len(labels) == K; pitch = (1280 - 140 - 142) // (K - 1)
    for i, (big, small) in enumerate(labels):
        x = 70 + i * pitch; d.rectangle([x, 380, x + 142, 384], fill=COLS[i]); d.text((x, 400), big, fill="#e6edf3", font=font(24)); d.text((x, 438), small, fill="#8b98a9", font=font(13, False))
    d.text((70, 560), "github.com/Soham-ChemE  ·  soham-cheme.github.io/Soham-ChemE", fill="#8b98a9", font=font(18, False))
    im.save(OUT / "social-preview.png", optimize=True); print("wrote social-preview.png")


def quantise(paths, colors=256, max_w=1400):
    from PIL import Image
    for p in paths:
        im = Image.open(p).convert("RGBA")
        if im.width > max_w: im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        q = im.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG); q.save(p, optimize=True); print("quantised", p.name, p.stat().st_size, "bytes")


def qa_readme(report):
    lines = ["# QA for the live page", "", "Served from docs/ by docs/tools/page-qa.mjs (node) or docs/tools/hero_shapes.py (Python Playwright), loaded in headless Chromium (software WebGL, so frame timing is not representative). Screenshots in both themes: the hero at the top and scrolled to its last project, the first two body scenes, the ALD card thumbnail, the 375 px hero.", ""]
    for page, pr in report.get("pages", {}).items():
        lines += [f"## {page}", ""]
        if "lighthouse" in pr:
            lh = pr["lighthouse"]; lines += [f"Lighthouse (desktop preset): performance {lh['performance']}, accessibility {lh['accessibility']}, best practices {lh['bestPractices']}, SEO {lh['seo']}", "", "| Metric | Value |", "|---|---|", f"| First Contentful Paint | {lh['fcp']} |", f"| Largest Contentful Paint | {lh['lcp']} |", f"| Speed Index | {lh['si']} |", f"| Total Blocking Time | {lh['tbt']} |", f"| Cumulative Layout Shift | {lh['cls']} |", f"| Total byte weight | {lh['bytes']} |", ""]
        lines += ["| Theme | Console errors | Failed requests | Images loaded | Transfer (bytes) | Body scenes captured |", "|---|---|---|---|---|---|"]
        for theme in ("dark", "light"):
            t = pr.get(theme)
            if t: lines.append(f"| {theme} | {len(t['errors']) + len(t.get('mobileErrors', []))} | {len(t['failed'])} | {t['imagesLoaded']} | {t['transferBytes']:,} | {', '.join(t['scenes'])} |")
        lines.append("")
        for theme in ("dark", "light"):
            t = pr.get(theme, {}); he = t.get("heroEnd")
            if he: lines.append(f"Hero scrolled to its end ({theme}): focus panel `{he['num']}`, panel in focus {str(he['on']).lower()}, readout \"{he['now']}\", scroll progress {he['t']}.")
        lines.append("")
    lines += ["Files: `light/` and `dark/` hold `index-hero.png` (hero at the top of the page), `index-hero-end.png` (hero scrolled to the last project), `index-scene1-*.png`, `index-scene2-*.png`, `index-card-ald.png` (the ALD card thumbnail) and `index-mobile-375-hero.png`; `lighthouse.report.html` and `.json` are the Lighthouse run (round 3, not re-run in round 4); `qa.json` is the machine-readable summary."]
    (DOCS / "qa" / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv):
    only = [a for a in argv if a.startswith("--")]; do_all = not only
    if do_all or "--data" in only: build_data()
    if do_all or "--preview" in only: build_preview()
    if do_all or "--hero" in only or "--hero-shapes" in only: build_hero(force="--hero-shapes" in only)
    if do_all or "--hero-png" in only:
        run(["node", *TOOL, "--hero-png"]); quantise([OUT / "hero.png"], max_w=1600)
    if do_all or "--snap" in only:
        run(["node", *TOOL, "--snap"]); quantise(sorted(OUT.glob("viz_*_*.png")))
    flags = [f for f in ("--qa", "--lighthouse") if do_all or f in only]
    if flags:
        run(["node", *TOOL, *flags]); qa_readme(json.loads((DOCS / "qa" / "qa.json").read_text()))


if __name__ == "__main__":
    main(sys.argv[1:])
