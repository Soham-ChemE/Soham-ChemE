#!/usr/bin/env python3
"""Headless captures of the live page with Python Playwright: the twin of docs/tools/page-qa.mjs for machines without a
global playwright for node. Serves docs/ on a local port and opens index.html in headless Chromium with SwiftShader and
window.__forceGL set, so the live WebGL scenes render (slowly) instead of the software-renderer fallback path.

  python docs/tools/hero_shapes.py --docs docs --hero-json docs/assets/hero_shapes.json
      300 particles of each hero shape projected through the scene's own camera (window.__hero.project), for build_assets.py --hero
  python docs/tools/hero_shapes.py --docs docs --snap ald[,cvd,...]      # assets/viz_<name>_<theme>.png, both themes, quantised
  python docs/tools/hero_shapes.py --docs docs --hero-png                # assets/hero.png: the hero canvas, dark theme, 1600x900
  python docs/tools/hero_shapes.py --docs docs --qa                      # both themes: console check, hero at start and end,
                                                                         # the focus panel's final number, the first two card scenes,
                                                                         # the ALD card thumbnail, the 375 px hero; qa/qa.json + README

Needs: pip install playwright pillow && python -m playwright install chromium."""
from __future__ import annotations
import argparse, functools, http.server, json, sys, threading, time
from pathlib import Path

GL_ARGS = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]
SHOT = 180_000   # ms: software GL at 56,000 particles with bloom and depth of field is slow


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def end_headers(self): self.send_header("cache-control", "no-cache"); super().end_headers()


def serve(docs):
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(docs)))
    threading.Thread(target=srv.serve_forever, daemon=True).start(); return srv, f"http://127.0.0.1:{srv.server_address[1]}/"


def open_page(browser, base, page_name, theme, viewport):
    ctx = browser.new_context(viewport=viewport, device_scale_factor=2 if viewport["width"] < 500 else 1, reduced_motion="no-preference", color_scheme=theme)
    ctx.add_init_script(f"window.__forceGL = true; try {{ localStorage.setItem('theme', '{theme}'); }} catch (e) {{}}")
    page = ctx.new_page(); errors, failed = [], []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("requestfailed", lambda r: failed.append(r.url))
    page.goto(base + page_name, wait_until="networkidle"); page.wait_for_function("window.SITE && window.SITE.ready"); time.sleep(1.2)
    return ctx, page, errors, failed


SCROLL_TO = """([s, fr]) => { const el = document.querySelector(s); const r = el.getBoundingClientRect(); const y = r.top + scrollY - (innerHeight - r.height) * fr;
  if (window.SITE && window.SITE.lenis) window.SITE.lenis.scrollTo(y, { immediate: true, force: true }); window.scrollTo(0, y); if (window.ScrollTrigger) ScrollTrigger.update(); }"""
SETTLE = """() => { if (window.ScrollTrigger) { ScrollTrigger.update(); ScrollTrigger.refresh(); } if (window.__viz) window.__viz.force(1); document.querySelectorAll('.reveal').forEach(e => e.classList.add('in')); }"""
HERO_END = """() => { const tr = document.querySelector('.hero-track'); const y = tr.offsetTop + tr.offsetHeight - innerHeight;
  if (window.SITE && window.SITE.lenis) window.SITE.lenis.scrollTo(y, { immediate: true, force: true }); window.scrollTo(0, y); if (window.ScrollTrigger) ScrollTrigger.update(); return y; }"""


def scroll_to(page, sel, frac=.5):
    page.evaluate(SCROLL_TO, [sel, frac]); page.evaluate(SETTLE)


def hero_json(browser, base, page_name, out):
    ctx, page, *_ = open_page(browser, base, page_name, "dark", {"width": 1280, "height": 800})
    page.wait_for_function("window.__hero")
    data = page.evaluate("() => window.__hero.PROJECTS.map((p, i) => ({ key: p.key, name: p.name, points: window.__hero.project(i, 300) }))")
    Path(out).write_text(json.dumps(data, separators=(",", ":"))); print("hero json", out, [len(d["points"]) for d in data], [d["key"] for d in data]); ctx.close()


def snap(browser, base, page_name, docs, names):
    outs = []
    for theme in ("dark", "light"):
        ctx, page, errors, _ = open_page(browser, base, page_name, theme, {"width": 1280, "height": 860})
        for name in names:
            sel = f'[data-viz="{name}"]'; scroll_to(page, sel); page.evaluate("() => window.__viz && window.__viz.force(1)"); time.sleep(.9)
            out = docs / "assets" / f"viz_{name}_{theme}.png"; page.query_selector(sel).screenshot(path=str(out), timeout=SHOT); print("snap", out); outs.append(out)
        if errors: print("console errors during snap", theme, errors)
        ctx.close()
    return outs


def hero_png(browser, base, page_name, docs):
    ctx, page, *_ = open_page(browser, base, page_name, "dark", {"width": 1600, "height": 900}); time.sleep(2.5)
    out = docs / "assets" / "hero.png"; page.query_selector("#heroCanvas").screenshot(path=str(out), timeout=SHOT); print("hero.png", out); ctx.close(); return out


def qa(browser, base, page_name, docs, last_key="ald", card_key="ald"):
    qa_json = docs / "qa" / "qa.json"; report = json.loads(qa_json.read_text()) if qa_json.exists() else {"pages": {}}; report.setdefault("pages", {})
    stem = page_name.replace(".html", "").replace("/", "_"); pr = report["pages"].setdefault(page_name, {}); ok = True
    for theme in ("dark", "light"):
        qd = docs / "qa" / theme; qd.mkdir(parents=True, exist_ok=True)
        ctx, page, errors, failed = open_page(browser, base, page_name, theme, {"width": 1440, "height": 900})
        page.screenshot(path=str(qd / f"{stem}-hero.png"), timeout=SHOT)
        # scroll the hero track to its end: the morph settles on the last shape and its focus panel counts up to the headline number
        page.evaluate(HERO_END)
        try: page.wait_for_function(f"""() => {{ const el = document.querySelector('[data-focus="{last_key}"] .num'); const p = window.__hero.PROJECTS[window.__hero.PROJECTS.length - 1]; return el && el.textContent === p.fmt(p.value); }}""", timeout=30_000); final_ok = True
        except Exception as e: final_ok = False; print("focus panel did not reach its final value:", e)
        time.sleep(2.5)   # camera lerp and the 20 % hold
        focus = page.evaluate(f"""() => ({{ num: document.querySelector('[data-focus="{last_key}"] .num').textContent, on: document.querySelector('[data-focus="{last_key}"]').classList.contains('on'), now: document.getElementById('heroNow').textContent, t: window.SITE.hero.t }})""")
        page.screenshot(path=str(qd / f"{stem}-hero-end.png"), timeout=SHOT)
        names = page.eval_on_selector_all("[data-viz]", "els => els.map(e => e.dataset.viz)")[:2]
        for i, name in enumerate(names, 1):
            scroll_to(page, f'[data-viz="{name}"]'); time.sleep(2.6); page.screenshot(path=str(qd / f"{stem}-scene{i}-{name}.png"), timeout=SHOT)
        scroll_to(page, f'[data-viz="{card_key}"]'); page.evaluate("() => window.__viz && window.__viz.force(1)"); time.sleep(1.5)
        page.query_selector(f'[data-viz="{card_key}"]').screenshot(path=str(qd / f"{stem}-card-{card_key}.png"), timeout=SHOT)
        imgs = page.eval_on_selector_all("img", "els => els.filter(i => i.src && !i.src.startsWith('data:')).map(i => ({ ok: i.complete && i.naturalWidth > 0, src: i.src.split('/').pop() }))")
        nbytes = page.evaluate("() => performance.getEntriesByType('resource').reduce((a, r) => a + (r.transferSize || r.encodedBodySize || 0), 0) + (performance.getEntriesByType('navigation')[0]?.transferSize || 0)")
        pr[theme] = {"errors": errors, "failed": failed, "imagesLoaded": f"{sum(1 for i in imgs if i['ok'])}/{len(imgs)}", "transferBytes": nbytes, "scenes": names, "heroEnd": focus, "heroEndReached": final_ok}
        ctx.close()
        mctx, mpage, merrors, _ = open_page(browser, base, page_name, theme, {"width": 375, "height": 812}); mpage.screenshot(path=str(qd / f"{stem}-mobile-375-hero.png"), timeout=SHOT); pr[theme]["mobileErrors"] = merrors; mctx.close()
        print("qa", theme, json.dumps(pr[theme])); ok = ok and final_ok and not errors and not merrors and not failed
    qa_json.parent.mkdir(parents=True, exist_ok=True); qa_json.write_text(json.dumps(report, indent=1)); return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--docs", default="docs"); ap.add_argument("--pages", default="index.html"); ap.add_argument("--hero-json"); ap.add_argument("--snap"); ap.add_argument("--hero-png", action="store_true"); ap.add_argument("--qa", action="store_true")
    a = ap.parse_args(); docs = Path(a.docs).resolve(); page_name = a.pages.split(",")[0]
    sys.path.insert(0, str(docs)); import build_assets   # quantise() and qa_readme(), shared with the node path
    from playwright.sync_api import sync_playwright
    srv, base = serve(docs); ok = True
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=GL_ARGS)
        if a.hero_json: hero_json(browser, base, page_name, a.hero_json)
        if a.snap: build_assets.quantise(snap(browser, base, page_name, docs, a.snap.split(",")))
        if a.hero_png: build_assets.quantise([hero_png(browser, base, page_name, docs)], max_w=1600)
        if a.qa: ok = qa(browser, base, page_name, docs); build_assets.qa_readme(json.loads((docs / "qa" / "qa.json").read_text()))
        browser.close()
    srv.shutdown(); sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
