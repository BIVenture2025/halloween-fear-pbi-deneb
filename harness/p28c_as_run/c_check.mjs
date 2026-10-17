// P28 C offline harness: renders each Deneb spec on node-canvas (same renderer family as Deneb in Desktop),
// writes PNGs, and checks every visible text item: font floor, inside the visual, no text-text overlap,
// no text-mark overlap (decor named bg_*, hit, line, card_link excluded; text named in_* may sit inside a shape).
// Fonts: DejaVu Sans registered AS "Segoe UI" (DejaVu is ~10 % wider -> conservative) and DejaVu Sans Bold AS "Arial Black".
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
// fonts: fontconfig aliases (run with FONTCONFIG_FILE=fc/fonts.conf): Segoe UI -> DejaVu Sans (all faces), Arial Black -> DejaVu Sans Bold
if (!process.env.FONTCONFIG_FILE) throw new Error('set FONTCONFIG_FILE');
const vega = await import('./v6/node_modules/vega/build/vega.node.js').catch(() => import('./v6/node_modules/vega/build/vega.module.js'));
import fs from 'fs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2]));
const MINF = cfg.minFont ?? 15;
const report = [];
function walk(scene, ox, oy, out, parentName) {
  for (const mark of scene.items || []) {
    for (const it of mark.items || []) {
      const vis = (it.opacity ?? 1) > 0.01;
      if (mark.marktype === 'group') {
        const gx = ox + (it.x || 0), gy = oy + (it.y || 0);
        if (vis && ((it.fillOpacity ?? 1) > 0.01 || (it.strokeOpacity ?? 1) > 0.01) && mark.name)
          out.push({ kind: 'mark', name: mark.name, x1: gx, y1: gy, x2: gx + (it.width || 0), y2: gy + (it.height || 0), group: true });
        walk(it, gx, gy, out, mark.name);
        continue;
      }
      if (!vis) continue;
      if (mark.marktype === 'text') {
        const txt = it.text == null ? '' : String(it.text);
        if (!txt.trim()) continue;
        let w = vega.textMetrics.width(it, txt);
        if (it.limit && w > it.limit) w = it.limit;
        const fs_ = it.fontSize, a = it.align || 'left';
        const x0 = a === 'center' ? -w / 2 : a === 'right' ? -w : 0;
        const box = [[x0, -0.78 * fs_], [x0 + w, -0.78 * fs_], [x0 + w, 0.22 * fs_], [x0, 0.22 * fs_]];
        const th = (it.angle || 0) * Math.PI / 180, c = Math.cos(th), s = Math.sin(th);
        const X = ox + (it.x || 0) + (it.dx || 0), Y = oy + (it.y || 0) + (it.dy || 0);
        const pts = box.map(([px, py]) => [X + px * c - py * s, Y + px * s + py * c]);
        out.push({ kind: 'text', name: mark.name || '', text: txt, size: fs_, pts, parent: parentName, w });
      } else {
        const b = it.bounds; if (!b || !isFinite(b.x1)) continue;
        if ((it.fillOpacity ?? 1) <= 0.01 && (it.strokeOpacity ?? 1) <= 0.01) continue;
        if (b.x2 - b.x1 <= 0 && b.y2 - b.y1 <= 0) continue;
        out.push({ kind: 'mark', name: mark.name || '', mt: mark.marktype, x1: ox + b.x1, y1: oy + b.y1, x2: ox + b.x2, y2: oy + b.y2 });
      }
    }
  }
}
const rectPts = m => [[m.x1, m.y1], [m.x2, m.y1], [m.x2, m.y2], [m.x1, m.y2]];
function sat(A, B, tol = 0.6) {
  for (const P of [A, B]) for (let i = 0; i < 4; i++) {
    const [x1, y1] = P[i], [x2, y2] = P[(i + 1) % 4]; const nx = y2 - y1, ny = x1 - x2; const L = Math.hypot(nx, ny) || 1;
    const pa = A.map(([x, y]) => (x * nx + y * ny) / L), pb = B.map(([x, y]) => (x * nx + y * ny) / L);
    if (Math.max(...pa) - tol <= Math.min(...pb) || Math.max(...pb) - tol <= Math.min(...pa)) return false;
  }
  return true;
}
const SKIP = n => /^(bg_|hit$|line$|card_link$|card$)/.test(n || '');
for (const job of cfg.jobs) {
  const spec = JSON.parse(fs.readFileSync(job.spec));
  for (const st of job.states) {
    const view = new vega.View(vega.parse(spec), { renderer: 'none' });
    await view.runAsync(); view.signal('clock', 99999); await view.runAsync();
    if (st.pick) { const src = view.data(st.pick.data); const dt = src.find(r => r[st.pick.field] === st.pick.value);
      if (!dt) throw new Error('pick not found ' + JSON.stringify(st.pick)); view.signal(st.pick.signal, dt); await view.runAsync(); }
    const cv = await view.toCanvas(job.scale || 1);
    fs.writeFileSync(`${cfg.out}/${job.id}_${st.name}.png`, cv.toBuffer('image/png'));
    const items = []; walk(view.scenegraph().root.items[0], 0, 0, items, null); if (!items.some(i => i.kind === "text")) throw new Error("checker read no text in " + job.id);
    const T = items.filter(i => i.kind === 'text'), M = items.filter(i => i.kind === 'mark' && !SKIP(i.name));
    const W = spec.width, H = spec.height, issues = [];
    for (const t of T) {
      if (t.size < MINF) issues.push(`FONT ${t.size}px "${t.text}"`);
      if (t.pts.some(([x, y]) => x < -0.5 || y < -0.5 || x > W + 0.5 || y > H + 0.5)) issues.push(`OUTSIDE "${t.text}" ${t.pts.map(p => p.map(Math.round).join(',')).join(' ')}`);
    }
    // in hover states only check card children against each other and against the card frame
    const hover = !!st.pick;
    const TT = hover ? T.filter(t => t.parent === 'card') : T;
    for (let i = 0; i < TT.length; i++) for (let j = i + 1; j < TT.length; j++)
      if (sat(TT[i].pts, TT[j].pts, -3)) issues.push(`TEXT×TEXT(<3px) "${TT[i].text}" × "${TT[j].text}"`);
    if (hover) {
      const card = items.find(i => i.kind === 'mark' && i.name === 'card' && i.group);
      if (!card) issues.push('CARD not visible');
      else for (const t of TT) if (t.pts.some(([x, y]) => x < card.x1 + 4 || x > card.x2 - 4 || y < card.y1 + 2 || y > card.y2 - 2)) issues.push(`OUT OF CARD "${t.text}"`);
      if (card && (card.x1 < 0 || card.y1 < 0 || card.x2 > W || card.y2 > H)) issues.push('CARD outside visual');
    } else {
      for (const t of T) for (const m of M) {
        if (t.name.startsWith('in_')) continue;
        if (sat(t.pts, rectPts(m), -2)) issues.push(`TEXT×${m.name || m.mt}(<2px) "${t.text}"`);
      }
    }
    report.push({ job: job.id, state: st.name, texts: T.length, marks: M.length, minFont: Math.min(...T.map(t => t.size)), issues });
    view.finalize();
  }
}
fs.writeFileSync(`${cfg.out}/report.json`, JSON.stringify(report, null, 1));
for (const r of report) console.log(`${r.job}/${r.state}: read ${r.texts} texts, ${r.marks} marks, min font ${r.minFont}px -> ${r.issues.length} issue(s)` + (r.issues.length ? '\n   ' + [...new Set(r.issues)].slice(0, 14).join('\n   ') : ''));
