/* Landing-page hero (round 3): one GPU particle system that morphs between seven shapes, each built from an excerpt of that
   project's own page data (window.PROFILE from assets/data.js, written by docs/build_assets.py from the sibling repositories).
   Scroll scrubs the morph and a camera path; the headline number of the project in focus counts up beside it.
   Technique: two position attributes (from, to) swapped on the CPU when the scroll segment changes, a per-particle delay so the
   cloud streams rather than snaps, 3D simplex noise in the vertex shader for the in-flight swirl, soft sprites with depth
   writes so the depth-of-field pass can focus on the cloud, bloom in dark mode only. See docs/DESIGN.md §6. */
import { THREE, createStage, cameraPath, palette } from './three-kit.js';
const D = window.PROFILE, S = window.SITE, reduced = S.reduced, phone = S.phone;
const N = phone ? 16000 : 56000;
const mulberry = a => () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const viridis = t => { const s = [[68, 1, 84], [59, 82, 139], [33, 145, 140], [94, 201, 98], [253, 231, 37]]; t = Math.max(0, Math.min(1, t)) * 4; const i = Math.floor(t), f = t - i, a = s[i], b = s[Math.min(i + 1, 4)]; return [(a[0] + (b[0] - a[0]) * f) / 255, (a[1] + (b[1] - a[1]) * f) / 255, (a[2] + (b[2] - a[2]) * f) / 255]; };
const interp = (rc, r) => { let i = 1; while (i < rc.length - 1 && rc[i][0] < r) i++; const a = rc[i - 1], b = rc[i]; const t = (r - a[0]) / ((b[0] - a[0]) || 1); return a[1] + (b[1] - a[1]) * Math.max(0, Math.min(1, t)); };
const gauss = rnd => { const u = 1 - rnd(), v = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
const hex = h => { const c = new THREE.Color(h); return [c.r, c.g, c.b]; };

/* ---------- the seven shapes: positions in a 5-unit box, colours per theme ---------- */
export const PROJECTS = [
  { key: 'cathodeai', name: 'CathodeAI', value: 2774, fmt: v => Math.round(v).toLocaleString('en-US'), unit: 'Li-ion cathodes screened', line: 'Degradation Screening Index, Spearman ρ = 0.76 on 11 experimental cathodes', url: 'https://soham-cheme.github.io/CathodeAI-Battery-Materials-Screener/', col: 'cyan' },
  { key: 'lmo', name: 'LMO half cell, PyBaMM', value: 26, fmt: v => Math.round(v) + ' mV', unit: 'training RMSE on my own cell data', line: 'three fitted parameters; blind 2C voltage within 17 mV', url: 'https://soham-cheme.github.io/LMO-Cathode-Rate-Model-PyBaMM/', col: 'hot' },
  { key: 'cvd', name: 'CVD reactor, COMSOL', value: 3.3, fmt: v => v.toFixed(1) + ' %', unit: 'wafer non-uniformity, from 179.6 %', line: 'root-caused as mass-transfer limited, fixed at the inlet, 14-run central composite design', url: 'https://soham-cheme.github.io/CVD-Reactor-Uniformity-COMSOL/', col: 'rose' },
  { key: 'md', name: 'Ionic liquids at nanotube walls', value: -8.75, fmt: v => v.toFixed(2) + ' kcal/mol', unit: 'per ion, [OMIM]⁺ at the CNT wall', line: 'all-atom NAMD, four imidazolium ionic liquids; Structural Chemistry 2024', url: 'https://soham-cheme.github.io/MD-IL-CNT-Interfacial-Interactions/', col: 'violet' },
  { key: 'scaps', name: 'ZnSe/CdTe cell, SCAPS-1D', value: 27.99, fmt: v => v.toFixed(2) + ' %', unit: 'simulated efficiency, Cs₂BiAgI₆ ETL', line: 'ten electron-transport layers and nine contacts in a six-parameter design of experiments', url: 'https://soham-cheme.github.io/Perovskite-Solar-Cell-SCAPS1D-Optimization/', col: 'warm' },
  { key: 'tr4680', name: '4680 pack propagation, COMSOL', value: 1.25, fmt: v => v.toFixed(2) + ' W/m·K', unit: 'cascade threshold in through-layer conductivity', line: '20-cell pack, twelve one-hour studies, adiabatic stress test', url: 'https://soham-cheme.github.io/4680-Thermal-Runaway-Propagation-COMSOL/', col: 'hot' },
  { key: 'ald', name: 'ALD chamber-to-feature model, OpenFOAM', value: 14.05, fmt: v => v.toFixed(2) + ' s', unit: 'saturating pulse on the patterned wafer, from 0.35 s blanket', line: 'supply rule within 25 % over AR 20–100; checked against measured ALD on 940 m² of powder', url: 'https://soham-cheme.github.io/ald-conformality/', col: 'green' }
];

export function buildShapes(n, dark) {
  const pal = palette(dark), out = [];
  const make = () => ({ pos: new Float32Array(n * 3), col: new Float32Array(n * 3) });
  const put = (s, k, x, y, z, c) => { s.pos[3 * k] = x; s.pos[3 * k + 1] = y; s.pos[3 * k + 2] = z; s.col[3 * k] = c[0]; s.col[3 * k + 1] = c[1]; s.col[3 * k + 2] = c[2]; };
  // 1 · CathodeAI: every particle sits in a small cloud around one of the sampled materials; colour = DSI (viridis)
  { const s = make(), rnd = mulberry(1), P = D.cathodeai.points, m = P.length; const sx = v => Math.min(v, 20) / 20 * 4.4 - 2.2, sy = v => Math.min(v, 300) / 300 * 3.2 - 1.6, sz = v => Math.min(v, 5) / 5 * 4.4 - 2.2;
    for (let k = 0; k < n; k++) { const p = P[k % m]; const c = dark ? viridis(p[3]) : viridis(p[3] * .85); put(s, k, sx(p[0]) + gauss(rnd) * .05, sy(p[1]) + gauss(rnd) * .05, sz(p[2]) + gauss(rnd) * .05, c); } out.push(s); }
  // 2 · LMO: the four measured discharge curves as particle ribbons, one per rate
  { const s = make(), rnd = mulberry(2), RC = { 'C/10': pal.cyan, 'C/5': pal.green, 'C/2': pal.warm, '2C': pal.rose }, C = D.lmo.curves; const X = v => v / 1.5 * 4.6 - 2.3, Y = v => (v - 3.4) / 1.2 * 3.0 - 1.5, Z = i => 1.5 - i * 1.0;
    for (let k = 0; k < n; k++) { const ci = k % C.length, pts = C[ci].measured, t = rnd() * (pts.length - 1), i = Math.floor(t), f = t - i, a = pts[i], b = pts[Math.min(pts.length - 1, i + 1)]; put(s, k, X(a[0] + (b[0] - a[0]) * f), Y(a[1] + (b[1] - a[1]) * f) + gauss(rnd) * .012, Z(ci) + (rnd() - .5) * .34, hex(RC[C[ci].rate])); } out.push(s); }
  // 3 · CVD: the wafer-plane concentration profile before the fix as a surface of revolution (the 179.6 % cone), colour = height
  { const s = make(), rnd = mulberry(3), rc = D.cvd.before; const vmax = Math.max(...rc.map(p => p[1]));
    for (let k = 0; k < n; k++) { const r = Math.sqrt(rnd()) * 138, th = rnd() * Math.PI * 2, v = interp(rc, r) / vmax, h = 2.6 * v - 1.2, onWafer = k % 9 === 0; const x = Math.cos(th) * r / 138 * 2.5, z = Math.sin(th) * r / 138 * 2.5; put(s, k, x, onWafer ? -1.45 + gauss(rnd) * .01 : h + gauss(rnd) * .02, z, onWafer ? hex(pal.steel) : (dark ? viridis(v) : viridis(v * .85))); } out.push(s); }
  // 4 · MD: the non-hydrogen atoms near the nanotube mid-plane (ring of carbons, ions inside and outside)
  { const s = make(), rnd = mulberry(4), A = D.md.atoms, m = A.length, COL = { 0: pal.steel, 1: pal.violet, 2: pal.blue, 4: pal.green, 5: pal.cyan }, SC = .11;
    for (let k = 0; k < n; k++) { const a = A[k % m]; put(s, k, a[0] * SC + gauss(rnd) * .035, a[1] * SC + gauss(rnd) * .035, a[2] * SC * 1.8 + gauss(rnd) * .035, hex(COL[a[3]] || pal.steel)); } out.push(s); }
  // 5 · SCAPS: the five-layer stack as filled slabs, with the ten-ETL ranking as bars behind it
  { const s = make(), rnd = mulberry(5), LC = { FTO: pal.blue, ZnSe: pal.green, CdTe: pal.warm, Cs2BiAgI6: pal.rose, Ni: pal.steel }, vis = t => t === 0 ? .25 : Math.max(.16, .42 * Math.log10(1 + t * 40)); const layers = []; let y = -1.6; [...D.scaps.stack].reverse().forEach(L => { const h = vis(L.t_um); layers.push({ y0: y, h, c: hex(LC[L.name] || pal.steel), w: h }); y += h; }); const tot = layers.reduce((a, l) => a + l.w, 0); const rk = D.scaps.ranking;
    for (let k = 0; k < n; k++) { if (k % 7 === 0) { const i = k % rk.length, h = Math.max(.04, rk[i][1] / 28 * 2.4); put(s, k, -2.3 + i * .5 + (rnd() - .5) * .3, -1.6 + rnd() * h, -2.4 + (rnd() - .5) * .3, hex(i === 0 ? pal.rose : pal.warm)); continue; } let u = rnd() * tot, L = layers[0]; for (const l of layers) { if (u < l.w) { L = l; break; } u -= l.w; } put(s, k, (rnd() - .5) * 3.6, L.y0 + rnd() * L.h, (rnd() - .5) * 2.4, L.c); } out.push(s); }
  // 6 · 4680: the twenty cells as particle shells, coloured by the reduced-order model's end-of-hour maximum temperature
  { const s = make(), rnd = mulberry(6), T = D.tr4680, last = T.cell_max_C[T.cell_max_C.length - 1], cool = new THREE.Color(pal.cool), hot = new THREE.Color(pal.hot), tmp = new THREE.Color();
    for (let k = 0; k < n; k++) { if (k % 8 === 0) { put(s, k, (rnd() - .5) * 3.1, -1.55 + gauss(rnd) * .01, (rnd() - .5) * 2.5, hex(pal.blue)); continue; } const c = k % 20, ix = c % 5, iy = Math.floor(c / 5), th = rnd() * Math.PI * 2, top = rnd() < .18; const u = Math.min(1, Math.max(0, (last[c] - 30) / 330)); tmp.copy(cool).lerp(hot, Math.min(1, u * 1.6)); const r = top ? Math.sqrt(rnd()) * .25 : .25, yy = top ? .5 : rnd() * 1.0 - .5; put(s, k, ix * .55 - 1.1 + Math.cos(th) * r, yy - .6 + .5, iy * .55 - .83 + Math.sin(th) * r, [tmp.r, tmp.g, tmp.b]); } out.push(s); }
  // 7 · ALD: one AR-100 hole cut open (a half cylinder, its open side toward this shape's viewpoint) coloured by the hole model's
  //     coverage from mouth to bottom at t = 8 s of the TMA pulse (green coated, steel bare), standing beside the 300 mm wafer as a
  //     disc: its flat surface coloured by the chamber run's thetaFlat at the same time (saturated), the hole bottoms under it by thetaBottom (bare)
  { const s = make(), rnd = mulberry(7), A = D.ald, H = A.hole, C = A.cov, th = H.theta[H.times.indexOf(8)], tf = C.thetaFlat[C.times.indexOf(8)], tb = C.thetaBottom[C.times.indexOf(8)], bare = hex(pal.steel), coated = hex(pal.green);
    const cov = u => { u = Math.max(0, Math.min(1, u)); return [bare[0] + (coated[0] - bare[0]) * u, bare[1] + (coated[1] - bare[1]) * u, bare[2] + (coated[2] - bare[2]) * u]; };
    const along = (arr, u) => { const t = Math.max(0, Math.min(arr.length - 1, u * (arr.length - 1))), i = Math.floor(t), f = t - i; return arr[i] + ((arr[Math.min(arr.length - 1, i + 1)] - arr[i]) * f); };
    const radial = (arr, rmm) => { const R = C.radii_mm; let i = 1; while (i < R.length - 1 && R[i] < rmm) i++; const f = Math.max(0, Math.min(1, (rmm - R[i - 1]) / (R[i] - R[i - 1]))); return arr[i - 1] + (arr[i] - arr[i - 1]) * f; };
    const HX = -.95, HZ = .15, HR = .72, TOP = 1.75, BOT = -1.6, open = Math.atan2(Math.cos(6 * 1.05 - .4), Math.sin(6 * 1.05 - .4)) + Math.PI / 2;   // viewpoint 7 of the camera loop, as in window.__hero.project
    const WX = 1.35, WZ = .45, WR = 1.25, WY = -1.5;
    for (let k = 0; k < n; k++) { const u = rnd();
      if (u < .58) { const d = rnd(), ph = open + rnd() * Math.PI, r = HR + gauss(rnd) * .015; put(s, k, HX + Math.cos(ph) * r, TOP - d * (TOP - BOT), HZ + Math.sin(ph) * r, cov(along(th, d))); }
      else if (u < .63) { const ph = open + rnd() * Math.PI, r = Math.sqrt(rnd()) * HR; put(s, k, HX + Math.cos(ph) * r, BOT + gauss(rnd) * .01, HZ + Math.sin(ph) * r, cov(th[th.length - 1])); }
      else { const r = Math.sqrt(rnd()) * WR, ph = rnd() * Math.PI * 2, under = rnd() < .3, rmm = r / WR * 150; put(s, k, WX + Math.cos(ph) * r, (under ? WY - .14 : WY) + gauss(rnd) * .01, WZ + Math.sin(ph) * r, cov(under ? radial(tb, rmm) : radial(tf, rmm))); } }
    out.push(s); }
  return out;
}

const NOISE = `vec3 mod289(vec3 x){return x-floor(x*(1.0/289.0))*289.0;}vec4 mod289(vec4 x){return x-floor(x*(1.0/289.0))*289.0;}vec4 permute(vec4 x){return mod289(((x*34.0)+1.0)*x);}vec4 taylorInvSqrt(vec4 r){return 1.79284291400159-0.85373472095314*r;}
float snoise(vec3 v){const vec2 C=vec2(1.0/6.0,1.0/3.0);const vec4 D=vec4(0.0,0.5,1.0,2.0);vec3 i=floor(v+dot(v,C.yyy));vec3 x0=v-i+dot(i,C.xxx);vec3 g=step(x0.yzx,x0.xyz);vec3 l=1.0-g;vec3 i1=min(g.xyz,l.zxy);vec3 i2=max(g.xyz,l.zxy);vec3 x1=x0-i1+C.xxx;vec3 x2=x0-i2+C.yyy;vec3 x3=x0-D.yyy;i=mod289(i);vec4 p=permute(permute(permute(i.z+vec4(0.0,i1.z,i2.z,1.0))+i.y+vec4(0.0,i1.y,i2.y,1.0))+i.x+vec4(0.0,i1.x,i2.x,1.0));float n_=0.142857142857;vec3 ns=n_*D.wyz-D.xzx;vec4 j=p-49.0*floor(p*ns.z*ns.z);vec4 x_=floor(j*ns.z);vec4 y_=floor(j-7.0*x_);vec4 x=x_*ns.x+ns.yyyy;vec4 y=y_*ns.x+ns.yyyy;vec4 h=1.0-abs(x)-abs(y);vec4 b0=vec4(x.xy,y.xy);vec4 b1=vec4(x.zw,y.zw);vec4 s0=floor(b0)*2.0+1.0;vec4 s1=floor(b1)*2.0+1.0;vec4 sh=-step(h,vec4(0.0));vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy;vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;vec3 p0=vec3(a0.xy,h.x);vec3 p1=vec3(a0.zw,h.y);vec3 p2=vec3(a1.xy,h.z);vec3 p3=vec3(a1.zw,h.w);vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));p0*=norm.x;p1*=norm.y;p2*=norm.z;p3*=norm.w;vec4 m=max(0.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.0);m=m*m;return 42.0*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));}`;
const VERT = `attribute vec3 aA; attribute vec3 aB; attribute vec3 aColA; attribute vec3 aColB; attribute float aRand;
uniform float uMix, uTime, uSize, uDpr, uSwirl; varying vec3 vCol; varying float vSw;
${NOISE}
void main(){
  float m = smoothstep(0.0, 1.0, clamp((uMix - aRand * 0.4) / 0.6, 0.0, 1.0));
  vec3 p = mix(aA, aB, m); float sw = sin(m * 3.14159265);
  vec3 q = p * 0.55 + vec3(0.0, 0.0, aRand * 3.0);
  vec3 nz = vec3(snoise(q + uTime * 0.12), snoise(q + 17.0 + uTime * 0.12), snoise(q + 31.0 + uTime * 0.12));
  p += nz * (sw * uSwirl + 0.012);
  vCol = mix(aColA, aColB, m); vSw = sw;
  vec4 mv = modelViewMatrix * vec4(p, 1.0);
  gl_PointSize = uSize * uDpr * (0.7 + 0.6 * aRand) * (1.0 + sw * 0.6) / -mv.z;
  gl_Position = projectionMatrix * mv;
}`;
const FRAG = `uniform float uAlpha; varying vec3 vCol; varying float vSw;
void main(){ float d = length(gl_PointCoord - 0.5); float a = smoothstep(0.5, 0.18, d); if (a < 0.3) discard;
  gl_FragColor = vec4(vCol * (1.0 + vSw * 0.35), a * uAlpha);
  #include <tonemapping_fragment>
  #include <colorspace_fragment>
}`;

(function () {
  const canvas = document.getElementById('heroCanvas'); if (!canvas) return;
  const st = createStage(canvas, { fov: 42, bloom: { strength: .55, radius: .6, threshold: .6 }, dof: { aperture: .0009, maxblur: .006, focus: 9 }, exposure: 1.05, env: false });
  if (st.failed) return; const { scene, camera } = st;
  let shapes = buildShapes(N, st.dark);
  const geo = new THREE.BufferGeometry(); const aA = new THREE.BufferAttribute(new Float32Array(N * 3), 3), aB = new THREE.BufferAttribute(new Float32Array(N * 3), 3), cA = new THREE.BufferAttribute(new Float32Array(N * 3), 3), cB = new THREE.BufferAttribute(new Float32Array(N * 3), 3);
  const rnd = mulberry(99), rand = new Float32Array(N); for (let i = 0; i < N; i++) rand[i] = rnd();
  geo.setAttribute('position', aA); geo.setAttribute('aA', aA); geo.setAttribute('aB', aB); geo.setAttribute('aColA', cA); geo.setAttribute('aColB', cB); geo.setAttribute('aRand', new THREE.BufferAttribute(rand, 1)); geo.boundingSphere = new THREE.Sphere(new THREE.Vector3(), 6);
  const mat = new THREE.ShaderMaterial({ vertexShader: VERT, fragmentShader: FRAG, transparent: true, depthWrite: true, blending: st.dark ? THREE.AdditiveBlending : THREE.NormalBlending, uniforms: { uMix: { value: 0 }, uTime: { value: 0 }, uSize: { value: phone ? 34 : 30 }, uDpr: { value: Math.min(devicePixelRatio || 1, 2) }, uSwirl: { value: .9 }, uAlpha: { value: st.dark ? .85 : .95 } } });
  mat.toneMapped = true; const pts = new THREE.Points(geo, mat); pts.frustumCulled = false; scene.add(pts);
  let seg = -1; const load = s => { const last = shapes.length - 1, a = shapes[Math.min(last, s)], b = shapes[Math.min(last, s + 1)]; aA.array.set(a.pos); aB.array.set(b.pos); cA.array.set(a.col); cB.array.set(b.col); aA.needsUpdate = aB.needsUpdate = cA.needsUpdate = cB.needsUpdate = true; seg = s; st.dirty = true; };
  st.onTheme = dark => { shapes = buildShapes(N, dark); mat.blending = dark ? THREE.AdditiveBlending : THREE.NormalBlending; mat.uniforms.uAlpha.value = dark ? .85 : .95; mat.needsUpdate = true; load(seg < 0 ? 0 : seg); };
  // camera: a loop of viewpoints, one per project, scrubbed by scroll; the cloud stays at the origin
  const K = PROJECTS.length; const pts3 = [], tg = []; for (let i = 0; i < K; i++) { const a = i * 1.05 - .4; pts3.push([Math.sin(a) * 8.2, 1.6 + Math.sin(i * 1.7) * 1.4, Math.cos(a) * 8.2]); tg.push([0, -.1, 0]); }
  const path = cameraPath(pts3, tg); const pos = new THREE.Vector3(), tgt = new THREE.Vector3(); path.at(reduced ? 1 : 0, pos, tgt); camera.position.copy(pos); camera.lookAt(tgt);
  // focus panels: headline number counts up while its project is in focus
  const panels = PROJECTS.map((p, i) => document.querySelector(`[data-focus="${p.key}"]`)); const nowEl = document.getElementById('heroNow'); const bands = [...document.querySelectorAll('.band')]; let cur = -1, lastT = -1, lastU = -1;
  const ease = t => 1 - Math.pow(1 - t, 3);
  load(0);
  window.__hero = { shapes: () => shapes, N, PROJECTS, project: (i, n) => { const s = shapes[i], step = Math.max(1, Math.floor(N / n)), out = [], v = new THREE.Vector3(), cam = new THREE.PerspectiveCamera(42, 1.6, .1, 100); cam.position.set(Math.sin(i * 1.05 - .4) * 8.2, 1.6, Math.cos(i * 1.05 - .4) * 8.2); cam.lookAt(0, -.1, 0); cam.updateMatrixWorld(); for (let k = 0; k < N; k += step) { v.set(s.pos[3 * k], s.pos[3 * k + 1], s.pos[3 * k + 2]).project(cam); out.push([+((v.x + 1) / 2).toFixed(3), +((1 - v.y) / 2).toFixed(3), [s.col[3 * k], s.col[3 * k + 1], s.col[3 * k + 2]].map(c => +c.toFixed(2))]); } return out; } };
  st.loop((t, dt) => {
    const T = reduced ? 1 : S.hero.t; let changed = false;
    const u = T * (K - 1); const s = Math.min(K - 2, Math.floor(u)); const f = u - s; const mix = reduced ? 1 : Math.min(1, Math.max(0, (f - .2) / .6));
    if (s !== seg) load(s);
    if (Math.abs(mix - mat.uniforms.uMix.value) > 1e-4) { mat.uniforms.uMix.value = mix; changed = true; }
    if (!reduced) { mat.uniforms.uTime.value = t; changed = true; }
    path.at(T, pos, tgt); if (camera.position.distanceToSquared(pos) > 1e-6) { camera.position.lerp(pos, reduced ? 1 : .12); camera.lookAt(tgt); changed = true; }
    const idx = Math.round(u); const vis = Math.max(0, Math.min(1, 1 - Math.abs(u - idx) * 2.2));
    if (idx !== cur || Math.abs(u - lastU) > 1e-3) {
      panels.forEach((el, i) => { if (!el) return; const on = i === idx; el.classList.toggle('on', on); el.style.opacity = on ? vis : 0; if (on) { const num = el.querySelector('.num'); if (num) num.textContent = PROJECTS[i].fmt(PROJECTS[i].value * ease(Math.min(1, vis * 1.25))); } });
      if (idx !== cur) { cur = idx; bands.forEach((b, i) => b.classList.toggle('on', i === idx)); if (nowEl) nowEl.innerHTML = `<b>${PROJECTS[idx].name}</b> · ${idx + 1} of ${K} · <a href="${PROJECTS[idx].url}">open the live page</a>`; }
      lastU = u; changed = true;
    }
    st.setBloom(.45 + .3 * S.hero.glow); if (st.bokeh) st.bokeh.uniforms.focus.value = camera.position.length() - .6;
    if (Math.abs(T - lastT) > 1e-4) { lastT = T; changed = true; }
    return changed;
  });
})();
