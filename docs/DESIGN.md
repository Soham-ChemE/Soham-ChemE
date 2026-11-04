# Design notes for the live page

This file records what was researched before the page was rebuilt, which techniques were chosen and why, and how the
page is checked. It is the engineering rationale behind `docs/index.html`, `docs/assets/site.css`, `docs/assets/site.js`
and `docs/assets/scene.js`. The same design system is used across all of Soham Kavathekar's project pages; the hero
scene and the sticky figure are specific to each repository.

## 1. What was researched

Scroll-driven 3D pages, in the order they were read:

| Source | What was taken from it |
|---|---|
| Codrops, *How to Build Cinematic 3D Scroll Experiences with GSAP* (Nov 2025), https://tympanus.net/codrops/2025/11/19/how-to-build-cinematic-3d-scroll-experiences-with-gsap/ and the companion repo https://github.com/JosephASG/codrops-cinematic-scroll-animations | One tall scroll container (several hundred vh) spaces the "shots"; a single scrubbed GSAP timeline is the director for camera position, mesh transforms and material uniforms; `scrub` values around 0.8–1 smooth the scrub without lagging. The article uses ScrollSmoother (Club GSAP); this page uses Lenis for the same job because it is MIT and on a public CDN. |
| Lenis README, https://github.com/darkroomengineering/lenis/blob/main/README.md | The canonical GSAP sync: `lenis.on('scroll', ScrollTrigger.update)`, drive `lenis.raf` from `gsap.ticker` (seconds × 1000), `gsap.ticker.lagSmoothing(0)`. One loop drives smooth scroll, ScrollTrigger and the WebGL scene. |
| GSAP docs, `gsap.matchMedia()` and `prefers-reduced-motion`, https://www.gsap.com/docs/v3/GSAP/gsap.matchMedia()/ | Put every scrubbed tween and pin inside `mm.add("(prefers-reduced-motion: no-preference)", …)`, and set final states directly in the `reduce` branch. |
| three.js forum threads on post-processing resolution, https://discourse.threejs.org/t/solved-why-the-image-looks-so-low-res-after-applied-unrealbloompass/17361 and https://discourse.threejs.org/t/postprocessing-adds-a-lot-of-pixelation/55813 | Set the renderer's pixel ratio and size before constructing `EffectComposer`; resize through `composer.setSize`, never the passes by hand; clamp `devicePixelRatio` because every pass costs 4× at 2× ratio. |
| GPU particle gallery on three.js r160, https://github.com/danlex/particles, and a DOF + selective-bloom portfolio, https://discourse.threejs.org/t/futamura-dev-personal-portfolio-where-every-page-is-a-different-webgl-experiment/93642 | Bloom at half resolution is enough for a glow; depth of field only where the scene has real depth layering, otherwise it reads as blur. Detect the device tier before building the heavy scene and serve a lighter version. |
| Apple-style pinned stage write-ups, https://ddingpy.github.io/mynote/posts/building-an-apple-style-scroll-experience-like-the-macbook-neo-page and https://theplusaddons.com/blog/scrollytelling/ | A 200–500 vh track with a sticky stage; a static fallback frame; a reduced-motion variant; do not stack more than a few pinned sections on one page; decide mobile behaviour deliberately. |
| A practitioner guide to scroll-driven 3D, https://svilenkovic.com/3d/how-to-make-scroll-driven-3d | Master timeline wrapped in one ScrollTrigger with `scrub`; camera on a spline; scroll-driven builds feel sluggish on mobile unless the scene is reduced. |
| Animated SVG in GitHub READMEs, https://blog.scalar.com/p/how-we-created-an-animated-responsive and https://dev.to/sieis/animate-svgs-for-github-readmes-420d | GitHub's image proxy strips scripts but keeps CSS `@keyframes` and `animation` when the `<style>` block is inside the SVG file itself and the file is loaded through `<img>`. SMIL is not relied on. |
| Lighthouse guidance on deferring scripts, https://www.debugbear.com/docs/how-to-defer-javascript-on-your-website | Keep the LCP element (the hero heading) in plain HTML, load the 3D as a module (deferred by definition) so first paint does not wait for three.js. |

What was rejected and why:

- **GSAP ScrollSmoother**: Club plugin, not on a public CDN under a permissive licence. Lenis does the job.
- **pmndrs/postprocessing**: faster single-pass merging, but mixing it with three's `EffectComposer` is a known footgun and the page only needs bloom plus one optional pass. three's own composer from the same pinned release keeps every import at one version.
- **WebGPU renderer**: not yet universal on the laptops and phones a recruiter opens this on; WebGL 2 is.
- **SMIL in the README hero**: unreliable through GitHub's proxy. CSS keyframes only.
- **A video-scrubbed hero** (the current apple.com technique): the data here is real geometry, and a video would hide that it is.

## 2. The chosen stack, pinned

| Piece | Version | Why this one |
|---|---|---|
| three.js (ES modules via import map from jsDelivr) | 0.186.1 (2026-09-24) | latest release older than two weeks at build time; `EffectComposer`, `RenderPass`, `UnrealBloomPass`, `BokehPass`, `OutputPass`, `OrbitControls`, `RoomEnvironment` from the same release |
| GSAP + ScrollTrigger | 3.15.0 | master timeline, pin, scrub, count-ups, `matchMedia` for reduced motion |
| Lenis | 1.3.27 | smooth scroll with the documented ScrollTrigger sync |

Everything else is hand-written in the three files under `docs/assets/`.

## 3. Page architecture

1. **Pinned hero.** `.hero-track` is 320 vh tall on desktop (240 vh on phones). Inside it `.hero` is `position: sticky` so the WebGL stage stays in view while the stats band and the first section scroll over it with a translucent backdrop. The sticky element, not a ScrollTrigger pin, holds the stage: it survives Lenis, resize and iOS toolbar collapse without re-measuring.
2. **Master timeline.** One `gsap.timeline()` with a `ScrollTrigger` on the track, `scrub: 0.8`, animates a plain object `{t, fade, glow, …}`. The scene reads that object every frame: `t` moves the camera along a `CatmullRomCurve3` of keyframed positions and lerps the look-at target; `glow` and material parameters follow it. The copy block fades and lifts in the same timeline so text and camera are one gesture.
3. **Count-ups.** Every `[data-count]` tweens a proxy value with `ScrollTrigger` at `top 85%`, `once: true`, with the final value written as text for reduced motion and for crawlers.
4. **Sticky method figure.** The method section is a two-column grid: a sticky figure (canvas or figure) and a column of steps. Each step has its own `ScrollTrigger` with `onEnter`/`onEnterBack` at the viewport centre that sets the figure state; the figure animates toward that state in its own render loop.
5. **Theme.** Light and dark follow the OS and a toggle; `themechange` events let the scenes swap background and material tints and the figures swap their `_light`/`_dark` SVGs.
6. **Rendering discipline.** `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))` (1.5 on phones); `ResizeObserver` → `renderer.setSize(w, h, false)` + `composer.setSize(w, h)`; the hero renders only while it is on screen (`IntersectionObserver`) and only when something changed (scroll progress, controls damping, autorotate); `pagehide` disposes geometries, materials, render targets and the renderer. If `WebGLRenderer` throws, the static `hero.png` fallback is shown and the page is complete without it.
7. **Reduced motion.** Under `prefers-reduced-motion: reduce` the timeline is not scrubbed, the camera sits at its final keyframe, autorotate and bloom pulsing are off, count-ups print their final value, and Lenis is not started.
8. **Mobile (375 px).** Same scene, reduced: only the vignette in view and its neighbours are rendered, orbit disabled, pixel ratio 1.5, bloom kept, depth of field off, bands hidden, hero track shorter.

## 4. Performance budget and QA

- Budget: first contentful paint under 2 s on a mid laptop, total transfer under 4 MB, 60 fps on an M1 MacBook Air.
- How it is met: the LCP element is the hero heading in static HTML; three.js and the scene load as a deferred module; the data file is a classic script so it parses in parallel; figures are SVG; PNGs are quantised to 256 colours; no web fonts (system stack).
- Checks committed under `docs/qa/`: full-page screenshots at 1440 px and 375 px from a headless Chromium with every image and canvas confirmed loaded and the console clean, and a Lighthouse report (`lighthouse.report.html` + `.json`, desktop preset) run against the page served from `docs/` exactly as GitHub Pages serves it. The headless browser renders WebGL in software, so its frame times are not representative; frame budget is verified by the renders-only-when-needed rule and the instance counts in `scene.js`.

## 5. This page's hero

The landing page threads the six project scenes along one camera path. Each vignette is built from an excerpt of that
project's own page data, written by `docs/build_assets.py` from the sibling repositories' `docs/assets/data.js` files into
`docs/assets/data.js` here (the excerpt is committed, with its provenance in `docs/CLAIMS.md`): 320 of the 787 CathodeAI
materials with the eleven validation cathodes; the four measured LMO discharge curves with the DFN dashed; the three CVD
wafer-plane profiles as a height map that morphs while that vignette is in view; the non-hydrogen atoms near the nanotube
mid-plane from the MD coordinates; the SCAPS layer stack with the ten-ETL ranking; and the 4680 pack coloured by the
surrogate's cascade trace. The scroll-scrubbed camera stops in front of each and drifts to the next; the band under the
headline and a small readout name the project in view and link to its page. Only the vignette in view and its two
neighbours are rendered. The README hero (`docs/assets/hero.svg`) is a strip of six small marks, one per project, drawn
with CSS keyframes from the same excerpt, generated by `docs/build_assets.py`.

## 6. Round 3: the particle journey

### What was researched

| Source | What was taken from it |
|---|---|
| Three.js Journey, *Particles morphing shader* lesson, https://www.threejs-journey.com/lessons/particles-morphing-shader | Morph on the GPU: keep two position attributes and mix them in the vertex shader with a uniform, never rewrite the attribute per frame; give every particle its own delay and duration from a random attribute so the cloud streams between shapes instead of snapping; make the particles grow while in flight. This page swaps the two attributes only when the scroll segment changes (five swaps across the whole page). |
| Ashima Arts / Ian McEwan, 3D simplex noise in GLSL (webgl-noise), via the vertex-displacement write-up https://www.clicktorelease.com/blog/vertex-displacement-noise-3d-webgl-glsl-three-js.html | The `snoise` implementation inlined in the vertex shader. Noise sampled at the particle's position plus time drives a swirl that peaks mid-morph (`sin(π·mix)`) and a small idle shimmer, so the cloud never looks frozen. |
| Codrops, *Crafting a Dreamy Particle Effect with Three.js and GPGPU*, https://tympanus.net/codrops/tag/gpgpu | Soft radial sprites, depth-aware sizing (`size / -mv.z`), and bloom as the glow instead of larger points. GPGPU simulation (positions in textures) was considered and rejected: the shapes here are fixed data, so attribute morphing is simpler and cheaper. |
| Bruno Simon, *Portfolio case study*, https://medium.com/@bruno_simon/bruno-simon-portfolio-case-study-960402cc259b, and the Codrops corridor portfolio, https://tympanus.net/codrops/2026/06/11/sketching-the-impossible-a-3d-portfolio-built-without-a-single-3d-model/ | One continuous world instead of pages; cheap primitives in place of models; input (there: driving or an Observer, here: scroll) as the only control. The journey is one cloud at the origin with the camera travelling a closed loop of viewpoints, so moving between projects is a camera move, not a scene swap. |
| Awwwards, *Dracarys* (WebGL and three.js GPGPU particles, post-processing, shaders), https://www.awwwards.com/sites/dracarys, and the ValiCred particle-morphing lore scroller, https://discourse.threejs.org/t/valicred-kinetic-3d-particle-morphing-webgl-lore-scroller/93787 | The current bar for a particle hero: morphing between meaningful shapes, scroll as the timeline, numbers and copy that arrive with the shape. Here every shape is built from the project's own data rather than from a model. |
| futamura.dev portfolio write-up, https://discourse.threejs.org/t/futamura-dev-personal-portfolio-where-every-page-is-a-different-webgl-experiment/93642 | Depth of field reads as blur unless the scene has real depth layering; particles have it, so `BokehPass` focuses on the cloud's centre with a small aperture on desktop and is off on phones. |
| three.js *webgl_multiple_elements* example (see the shared runtime note in each project's DESIGN.md) | The six card thumbnails are live views of the same shapes drawn by one scissor-clipped renderer. |

### What was built

- **One particle system, six shapes.** `buildShapes()` in `assets/scene.js` turns `assets/data.js` into six position-and-colour sets of 56,000 particles (16,000 on phones): particles clustered on the sampled CathodeAI materials coloured by DSI; the four LMO discharge curves as ribbons by rate; the CVD wafer-plane profile before the fix as a surface of revolution with a wafer disc under it; the ionic-liquid atoms near the nanotube mid-plane; the SCAPS stack as filled slabs with the ten-ETL ranking behind it; the twenty 4680 cells as shells coloured by the reduced-order model's end-of-hour maximum temperature. A seeded generator makes the shapes identical on every load, which is what lets the README hero be generated from the same positions.
- **Scroll is the timeline.** The pinned hero track is 720 vh. Scroll progress `t` maps to a shape index `u = 5t`; the integer part picks the from/to attributes and the fraction, with a 20 % hold at each end, is the mix uniform. The camera follows a `CatmullRom` loop of six viewpoints around the origin with a lerp, and depth of field focuses on the cloud's centre.
- **Numbers that count up in focus.** A focus panel per project fades in as its shape resolves and its headline number counts from zero with a cubic ease: 2,774; 26 mV; 3.3 %; −8.75 kcal/mol; 27.99 %; 1.25 W/m·K. Each links to the live page; the band strip under the copy mirrors the six and marks the one in view.
- **Both themes.** Additive blending and bloom on the dark stage; normal blending, a darker palette and bloom restricted to HDR pixels on the pale stage, through the shared stage's per-theme block. Shapes are rebuilt with the theme's palette on toggle.
- **Fallbacks.** Reduced motion pins the morph at the last shape and the camera at its last viewpoint; without WebGL the static `hero.png` is shown. The six card thumbnails have their own static PNGs.
- **Software renderers.** `site.js` reads the unmasked WebGL renderer string; SwiftShader, llvmpipe and the Microsoft basic renderer cannot animate a full-screen particle system at interactive rates, so on those the page serves its reduced path (the cloud at its last shape, static thumbnails for the cards). Lighthouse's headless Chromium is one of them, so the committed report measures that path; the QA screenshots are taken with `window.__forceGL` set so they show the live scenes.
- **Card thumbnails.** The six project cards carry live views of the same shapes drawn by the shared `assets/viz.js` renderer (one fixed canvas, scissor-clipped per card, the three.js *webgl_multiple_elements* pattern, https://github.com/mrdoob/three.js/blob/master/examples/webgl_multiple_elements.html), with static PNG fallbacks captured by `docs/build_assets.py --snap`.
- **Light mode.** The shared stage applies exposure 0.82, bloom restricted to HDR pixels (threshold 1.0, strength × 0.18), environment × 0.55 and the pale stage colour; the particle material switches from additive to normal blending and the shapes are rebuilt with the darker palette. Hero copy uses the page ink colour in both themes.
- **README hero.** `docs/build_assets.py` asks the headless page for 300 particles of each shape projected through the scene's own camera (`window.__hero.project`) and writes `docs/assets/hero.svg`, in which every particle is a circle with its own CSS keyframe path through the six shapes (24 s loop, CSS only, no SMIL, no scripts), so the README animates on github.com with the same geometry the page uses.
