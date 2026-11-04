"""Build the landing page's assets: card thumbnails from the five project pages' hero renders and a 1280x640 social preview.

Reads docs/assets/hero.png from each sibling project clone (../<repo>/docs/assets/hero.png, produced by each repo's own
page render) when present; otherwise skips that card image. Writes docs/assets/card_*.png and docs/assets/social-preview.png.
Run from the repository root:  python docs/build_assets.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, "docs", "assets"); os.makedirs(OUT, exist_ok=True)
PARENT = os.path.dirname(ROOT)
CARDS = {"cathodeai": "CathodeAI-Battery-Materials-Screener", "lmo": "LMO-Cathode-Rate-Model-PyBaMM", "cvd": "CVD-Reactor-Uniformity-COMSOL", "md": "MD-IL-CNT-Interfacial-Interactions", "scaps": "Perovskite-Solar-Cell-SCAPS1D-Optimization"}
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
