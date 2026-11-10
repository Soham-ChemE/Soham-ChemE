/* Body scenes for the landing page: each project card carries a live 3D thumbnail drawn by the shared Viz renderer
   (assets/viz.js) from the same seven shapes the hero morphs between (buildShapes in scene.js), subsampled. */
import { Viz } from './viz.js';
import { THREE } from './three-kit.js';
import { buildShapes, PROJECTS } from './scene.js';
const S = window.SITE; const NC = S.phone ? 2500 : 7000;
let shapes = { dark: null, light: null }; const get = dark => (shapes[dark ? 'dark' : 'light'] ||= buildShapes(NC, dark));
const sprite = (() => { const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d'); const r = g.createRadialGradient(32, 32, 0, 32, 32, 32); r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(.45, 'rgba(255,255,255,.9)'); r.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = r; g.fillRect(0, 0, 64, 64); const t = new THREE.CanvasTexture(c); return t; })();
PROJECTS.forEach((p, i) => Viz.view(`[data-viz="${p.key}"]`, v => {
  const s = get(v.dark)[i]; const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(s.pos, 3)); geo.setAttribute('color', new THREE.BufferAttribute(s.col.slice(), 3));
  const m = new THREE.PointsMaterial({ size: .11, vertexColors: true, map: sprite, transparent: true, alphaTest: .3, depthWrite: true, sizeAttenuation: true, blending: v.dark ? THREE.AdditiveBlending : THREE.NormalBlending, opacity: v.dark ? .9 : 1 });
  const pts = new THREE.Points(geo, m); pts.scale.setScalar(.001); v.rig.add(pts);
  v.onTheme = (vv, dark) => { const t = get(dark)[i]; geo.attributes.color.array.set(t.col); geo.attributes.color.needsUpdate = true; m.blending = dark ? THREE.AdditiveBlending : THREE.NormalBlending; m.opacity = dark ? .9 : 1; m.needsUpdate = true; };
  v.update = vv => { const k = .001 + .999 * (1 - Math.pow(1 - vv.p, 3)); if (Math.abs(pts.scale.x - k) > 1e-4) { pts.scale.setScalar(k); return true; } return false; };
  v.spin = .18; v.tilt = .15; v.rot = i * .7;
}, { camera: [0, 1.4, 8.4], target: [0, -.2, 0], fov: 38, envIntensity: 0 }));
