#!/usr/bin/env python3
html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blob It</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0f0f0f; color: #e0e0e0; font-family: 'Inter', system-ui, sans-serif; display: flex; height: 100vh; overflow: hidden; }
#canvas-area { flex: 1; position: relative; display: flex; align-items: center; justify-content: center; background: #111; }
#main-canvas { cursor: crosshair; }
#toolbar { position: absolute; top: 16px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px; background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 8px; padding: 6px; z-index: 10; }
.tool-btn { background: transparent; border: 1px solid transparent; color: #888; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; transition: all 0.15s; }
.tool-btn:hover { background: #222; color: #ccc; }
.tool-btn.active { background: #2a2a2a; border-color: #444; color: #fff; }
#upload-label { background: transparent; border: 1px solid #333; color: #888; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; }
#upload-label:hover { border-color: #555; color: #ccc; }
#file-input { display: none; }
#panel { width: 260px; background: #141414; border-left: 1px solid #1e1e1e; padding: 20px 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; }
.panel-section h3 { font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; color: #555; margin-bottom: 12px; }
.param-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px; }
.param-row label { font-size: 12px; color: #888; }
.param-row span { font-size: 11px; color: #555; min-width: 32px; text-align: right; }
input[type=range] { width: 100%; accent-color: #666; margin-bottom: 10px; }
.color-row { display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; }
.color-swatch { width: 24px; height: 24px; border-radius: 50%; cursor: pointer; border: 2px solid transparent; transition: border-color 0.15s; }
.color-swatch.active { border-color: #fff; }
.action-btn { width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #2a2a2a; background: #1a1a1a; color: #ccc; cursor: pointer; font-size: 12px; transition: all 0.15s; margin-bottom: 6px; }
.action-btn:hover { background: #222; border-color: #444; color: #fff; }
.action-btn.primary { background: #2a2a2a; border-color: #444; }
#status { position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%); font-size: 11px; color: #444; pointer-events: none; white-space: nowrap; }
</style>
</head>
<body>
<div id="canvas-area">
  <div id="toolbar">
    <button class="tool-btn active" id="btn-draw">Draw</button>
    <button class="tool-btn" id="btn-select">Select</button>
    <button class="tool-btn" id="btn-clear">Clear</button>
    <label id="upload-label">Upload<input type="file" id="file-input" accept="image/*"></label>
  </div>
  <canvas id="main-canvas"></canvas>
  <div id="status">Draw a path to generate organic shapes</div>
</div>
<div id="panel">
  <div class="panel-section">
    <h3>Blob Shape</h3>
    <div class="param-row"><label>Smoothness</label><span id="val-smooth">60</span></div>
    <input type="range" id="sl-smooth" min="0" max="100" value="60">
    <div class="param-row"><label>Noise Amount</label><span id="val-noise">40</span></div>
    <input type="range" id="sl-noise" min="0" max="100" value="40">
    <div class="param-row"><label>Noise Scale</label><span id="val-nscale">50</span></div>
    <input type="range" id="sl-nscale" min="1" max="100" value="50">
    <div class="param-row"><label>Blob Width</label><span id="val-width">30</span></div>
    <input type="range" id="sl-width" min="5" max="120" value="30">
  </div>
  <div class="panel-section">
    <h3>Branches</h3>
    <div class="param-row"><label>Density</label><span id="val-bdensity">30</span></div>
    <input type="range" id="sl-bdensity" min="0" max="100" value="30">
    <div class="param-row"><label>Length</label><span id="val-blength">40</span></div>
    <input type="range" id="sl-blength" min="0" max="100" value="40">
    <div class="param-row"><label>Thickness</label><span id="val-bthick">50</span></div>
    <input type="range" id="sl-bthick" min="10" max="100" value="50">
    <div class="param-row"><label>Recursion</label><span id="val-brecurse">2</span></div>
    <input type="range" id="sl-brecurse" min="0" max="4" value="2">
  </div>
  <div class="panel-section">
    <h3>Color</h3>
    <div class="color-row">
      <div class="color-swatch active" style="background:linear-gradient(135deg,#ff6b9d,#ff9a3c)" data-colors="#ff6b9d,#ff9a3c"></div>
      <div class="color-swatch" style="background:linear-gradient(135deg,#667eea,#764ba2)" data-colors="#667eea,#764ba2"></div>
      <div class="color-swatch" style="background:linear-gradient(135deg,#43e97b,#38f9d7)" data-colors="#43e97b,#38f9d7"></div>
      <div class="color-swatch" style="background:linear-gradient(135deg,#fa709a,#fee140)" data-colors="#fa709a,#fee140"></div>
      <div class="color-swatch" style="background:linear-gradient(135deg,#a18cd1,#fbc2eb)" data-colors="#a18cd1,#fbc2eb"></div>
      <div class="color-swatch" style="background:linear-gradient(135deg,#2af598,#009efd)" data-colors="#2af598,#009efd"></div>
      <div class="color-swatch" style="background:linear-gradient(135deg,#f093fb,#f5576c)" data-colors="#f093fb,#f5576c"></div>
      <div class="color-swatch" style="background:linear-gradient(135deg,#ffecd2,#fcb69f)" data-colors="#ffecd2,#fcb69f"></div>
    </div>
    <div class="param-row"><label>Opacity</label><span id="val-opacity">85</span></div>
    <input type="range" id="sl-opacity" min="10" max="100" value="85">
    <div class="param-row"><label>Glow</label><span id="val-glow">40</span></div>
    <input type="range" id="sl-glow" min="0" max="100" value="40">
  </div>
  <div class="panel-section">
    <h3>Actions</h3>
    <button class="action-btn primary" id="btn-generate">Generate Blob</button>
    <button class="action-btn" id="btn-randomize">Randomize</button>
    <button class="action-btn" id="btn-export-png">Export PNG</button>
    <button class="action-btn" id="btn-export-svg">Export SVG</button>
  </div>
</div>
<script>
const canvas = document.getElementById('main-canvas');
const ctx = canvas.getContext('2d');
const canvasArea = document.getElementById('canvas-area');
let mode = 'draw', isDrawing = false, rawPoints = [], shapes = [], selectedShape = null;
let dragOffset = {x:0,y:0}, currentColors = ['#ff6b9d','#ff9a3c'];

function resizeCanvas() {
  canvas.width = canvasArea.clientWidth;
  canvas.height = canvasArea.clientHeight;
  render();
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

function p(id) { return parseInt(document.getElementById(id).value); }
function bindSlider(id, valId) {
  const sl = document.getElementById(id), vl = document.getElementById(valId);
  sl.addEventListener('input', () => { vl.textContent = sl.value; render(); });
}
['smooth','noise','nscale','width','bdensity','blength','bthick','brecurse','opacity','glow'].forEach(n => bindSlider('sl-'+n,'val-'+n));

document.querySelectorAll('.color-swatch').forEach(sw => {
  sw.addEventListener('click', () => {
    document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('active'));
    sw.classList.add('active');
    currentColors = sw.dataset.colors.split(',');
    render();
  });
});

document.getElementById('btn-draw').addEventListener('click', () => setMode('draw'));
document.getElementById('btn-select').addEventListener('click', () => setMode('select'));
document.getElementById('btn-clear').addEventListener('click', () => {
  shapes = []; rawPoints = []; render();
  document.getElementById('status').textContent = 'Canvas cleared';
});

function setMode(m) {
  mode = m;
  canvas.style.cursor = m === 'draw' ? 'crosshair' : 'default';
  document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('btn-'+m).classList.add('active');
}

function getPos(e) {
  const rect = canvas.getBoundingClientRect();
  const src = e.touches ? e.touches[0] : e;
  return { x: src.clientX - rect.left, y: src.clientY - rect.top };
}

canvas.addEventListener('mousedown', e => {
  if (mode === 'draw') { isDrawing = true; rawPoints = [getPos(e)]; }
  else if (mode === 'select') {
    const pos = getPos(e); selectedShape = null;
    for (let i = shapes.length-1; i >= 0; i--) {
      if (pointInShape(pos, shapes[i])) {
        selectedShape = i;
        dragOffset = { x: pos.x-(shapes[i].cx||0), y: pos.y-(shapes[i].cy||0) };
        break;
      }
    }
  }
});

canvas.addEventListener('mousemove', e => {
  if (mode === 'draw' && isDrawing) { rawPoints.push(getPos(e)); renderPreview(); }
  else if (mode === 'select' && selectedShape !== null && e.buttons === 1) {
    const pos = getPos(e), s = shapes[selectedShape];
    const dx = pos.x - dragOffset.x - (s.cx||0), dy = pos.y - dragOffset.y - (s.cy||0);
    s.points = s.points.map(pt => ({x: pt.x+dx, y: pt.y+dy}));
    if (s.cx !== undefined) { s.cx += dx; s.cy += dy; }
    render();
  }
});

canvas.addEventListener('mouseup', () => {
  if (mode === 'draw' && isDrawing) {
    isDrawing = false;
    if (rawPoints.length > 5) {
      shapes.push({ points: [...rawPoints], seed: Math.random()*10000 });
      document.getElementById('status').textContent = 'Path captured — adjust params or Generate';
    }
    render();
  }
  selectedShape = null;
});

function renderPreview() {
  render();
  if (rawPoints.length < 2) return;
  ctx.save();
  ctx.strokeStyle = 'rgba(255,255,255,0.25)';
  ctx.lineWidth = 1.5; ctx.setLineDash([4,4]);
  ctx.beginPath(); ctx.moveTo(rawPoints[0].x, rawPoints[0].y);
  for (let i=1;i<rawPoints.length;i++) ctx.lineTo(rawPoints[i].x, rawPoints[i].y);
  ctx.stroke(); ctx.restore();
}

function noise2d(x, y, s) {
  const xi = Math.floor(x/s), yi = Math.floor(y/s);
  const xf = x/s-xi, yf = y/s-yi;
  const r = (a,b) => (Math.sin(a*127.1+b*311.7)*43758.5453)%1;
  const lerp = (a,b,t) => a+t*(b-a);
  const fade = t => t*t*(3-2*t);
  return lerp(lerp(r(xi,yi),r(xi+1,yi),fade(xf)),lerp(r(xi,yi+1),r(xi+1,yi+1),fade(xf)),fade(yf));
}

function resample(pts, count) {
  if (pts.length < 2) return pts;
  let total = 0;
  for (let i=1;i<pts.length;i++) { const dx=pts[i].x-pts[i-1].x,dy=pts[i].y-pts[i-1].y; total+=Math.sqrt(dx*dx+dy*dy); }
  const step = total/count;
  const result = [pts[0]];
  let dist=0, pi=0;
  for (let i=1;i<count;i++) {
    const target = i*step;
    while (pi < pts.length-2) {
      const dx=pts[pi+1].x-pts[pi].x, dy=pts[pi+1].y-pts[pi].y;
      const seg=Math.sqrt(dx*dx+dy*dy);
      if (dist+seg >= target) { const t=(target-dist)/seg; result.push({x:pts[pi].x+dx*t,y:pts[pi].y+dy*t}); break; }
      dist+=seg; pi++;
    }
  }
  return result;
}

function catmullRom(pts) {
  if (pts.length < 3) return pts;
  const result = [];
  const loop = [...pts, pts[0], pts[1], pts[2]];
  for (let i=0;i<loop.length-3;i++) {
    const p0=loop[i],p1=loop[i+1],p2=loop[i+2],p3=loop[i+3];
    for (let t=0;t<=1;t+=0.04) {
      const t2=t*t,t3=t2*t;
      result.push({
        x:0.5*((2*p1.x)+(-p0.x+p2.x)*t+(2*p0.x-5*p1.x+4*p2.x-p3.x)*t2+(-p0.x+3*p1.x-3*p2.x+p3.x)*t3),
        y:0.5*((2*p1.y)+(-p0.y+p2.y)*t+(2*p0.y-5*p1.y+4*p2.y-p3.y)*t2+(-p0.y+3*p1.y-3*p2.y+p3.y)*t3)
      });
    }
  }
  return result;
}

function convexHull(pts) {
  if (pts.length < 3) return pts;
  const sorted = [...pts].sort((a,b)=>a.x-b.x||a.y-b.y);
  const cross = (o,a,b) => (a.x-o.x)*(b.y-o.y)-(a.y-o.y)*(b.x-o.x);
  const lower=[],upper=[];
  for (const pt of sorted) { while(lower.length>=2&&cross(lower[lower.length-2],lower[lower.length-1],pt)<=0)lower.pop(); lower.push(pt); }
  for (let i=sorted.length-1;i>=0;i--) { const pt=sorted[i]; while(upper.length>=2&&cross(upper[upper.length-2],upper[upper.length-1],pt)<=0)upper.pop(); upper.push(pt); }
  upper.pop(); lower.pop();
  return lower.concat(upper);
}

function pointInShape(pt, shape) {
  const bpts = getBlobPoints(shape);
  let inside = false;
  for (let i=0,j=bpts.length-1;i<bpts.length;j=i++) {
    const xi=bpts[i].x,yi=bpts[i].y,xj=bpts[j].x,yj=bpts[j].y;
    if(((yi>pt.y)!==(yj>pt.y))&&(pt.x<(xj-xi)*(pt.y-yi)/(yj-yi)+xi)) inside=!inside;
  }
  return inside;
}

function getBlobPoints(shape) {
  const noiseAmt = p('sl-noise')/100;
  const noiseScale = p('sl-nscale')*2+5;
  const blobWidth = p('sl-width');
  const s = shape.seed||0;
  const pts = shape.points;
  if (pts.length < 3) return pts;
  const resampled = resample(pts, 80);
  const cx = resampled.reduce((a,pt)=>a+pt.x,0)/resampled.length;
  const cy = resampled.reduce((a,pt)=>a+pt.y,0)/resampled.length;
  shape.cx = cx; shape.cy = cy;
  const expanded = resampled.map(pt => {
    const dx=pt.x-cx, dy=pt.y-cy;
    const dist=Math.sqrt(dx*dx+dy*dy)||1;
    const nx=dx/dist, ny=dy/dist;
    const n = noise2d(pt.x*0.008+s, pt.y*0.008+s, noiseScale)*2-1;
    const offset = blobWidth + n*noiseAmt*blobWidth*2;
    return { x: pt.x+nx*offset, y: pt.y+ny*offset };
  });
  return catmullRom(expanded);
}

function drawBranches(blobPts, cx, cy) {
  const density = p('sl-bdensity')/100;
  const lenFactor = p('sl-blength')/100;
  const thickFactor = p('sl-bthick')/100;
  const recurse = p('sl-brecurse');
  if (density === 0 || lenFactor === 0) return;
  const count = Math.max(1, Math.floor(density*20));
  const step = Math.max(1, Math.floor(blobPts.length/count));
  for (let i=0;i<blobPts.length;i+=step) {
    const pt = blobPts[i];
    const dx=pt.x-cx, dy=pt.y-cy;
    const dist=Math.sqrt(dx*dx+dy*dy)||1;
    const len=(15+Math.random()*35)*lenFactor;
    const thick=(1+Math.random()*2)*thickFactor;
    drawBranch(pt.x, pt.y, dx/dist, dy/dist, len, thick, recurse);
  }
}

function drawBranch(x, y, nx, ny, len, thick, depth) {
  if (depth < 0 || len < 2 || thick < 0.2) return;
  const angle = Math.atan2(ny, nx);
  const ex = x+nx*len+(Math.random()-0.5)*len*0.3;
  const ey = y+ny*len+(Math.random()-0.5)*len*0.3;
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.quadraticCurveTo(x+nx*len*0.5+(Math.random()-0.5)*len*0.3, y+ny*len*0.5+(Math.random()-0.5)*len*0.3, ex, ey);
  const alpha = Math.floor(p('sl-opacity')*0.5*2.55).toString(16).padStart(2,'0');
  ctx.strokeStyle = currentColors[0]+alpha;
  ctx.lineWidth = thick; ctx.lineCap = 'round'; ctx.stroke();
  if (depth > 0) {
    const spread = 0.45+Math.random()*0.2;
    drawBranch(ex, ey, Math.cos(angle+spread), Math.sin(angle+spread), len*0.6, thick*0.65, depth-1);
    if (Math.random()>0.35) drawBranch(ex, ey, Math.cos(angle-spread), Math.sin(angle-spread), len*0.55, thick*0.6, depth-1);
  }
}

function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  shapes.forEach((shape, idx) => {
    const blobPts = getBlobPoints(shape);
    if (blobPts.length < 3) return;
    const cx = shape.cx||canvas.width/2, cy = shape.cy||canvas.height/2;
    const glow = p('sl-glow');
    if (glow > 0) { ctx.shadowColor = currentColors[0]; ctx.shadowBlur = glow*0.8; }
    const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, 180);
    grad.addColorStop(0, currentColors[0]+'ff');
    grad.addColorStop(1, (currentColors[1]||currentColors[0])+'66');
    ctx.globalAlpha = p('sl-opacity')/100;
    ctx.beginPath();
    ctx.moveTo(blobPts[0].x, blobPts[0].y);
    for (let i=1;i<blobPts.length;i++) ctx.lineTo(blobPts[i].x, blobPts[i].y);
    ctx.closePath();
    ctx.fillStyle = grad; ctx.fill();
    ctx.shadowBlur = 0; ctx.globalAlpha = 1;
    drawBranches(blobPts, cx, cy);
    if (selectedShape === idx) {
      ctx.save(); ctx.strokeStyle='rgba(255,255,255,0.4)'; ctx.lineWidth=1; ctx.setLineDash([4,4]);
      ctx.beginPath(); ctx.moveTo(blobPts[0].x, blobPts[0].y);
      for (let i=1;i<blobPts.length;i++) ctx.lineTo(blobPts[i].x, blobPts[i].y);
      ctx.closePath(); ctx.stroke(); ctx.restore();
    }
  });
}

document.getElementById('btn-generate').addEventListener('click', () => {
  shapes.forEach(s => s.seed = Math.random()*10000);
  render();
  document.getElementById('status').textContent = 'Generated!';
});

document.getElementById('btn-randomize').addEventListener('click', () => {
  const rnd = (id,min,max) => { const v=Math.floor(Math.random()*(max-min)+min); document.getElementById('sl-'+id).value=v; document.getElementById('val-'+id).textContent=v; };
  rnd('noise',10,80); rnd('nscale',10,80); rnd('width',10,70);
  rnd('bdensity',0,70); rnd('blength',10,80); rnd('bthick',20,80);
  const swatches = document.querySelectorAll('.color-swatch');
  const pick = swatches[Math.floor(Math.random()*swatches.length)];
  document.querySelectorAll('.color-swatch').forEach(s=>s.classList.remove('active'));
  pick.classList.add('active'); currentColors = pick.dataset.colors.split(',');
  shapes.forEach(s => s.seed = Math.random()*10000);
  render();
});

document.getElementById('btn-export-png').addEventListener('click', () => {
  const link = document.createElement('a');
  link.download = 'blobit.png'; link.href = canvas.toDataURL('image/png'); link.click();
});

document.getElementById('btn-export-svg').addEventListener('click', () => {
  let defs='', paths='';
  shapes.forEach((shape,i) => {
    const blobPts = getBlobPoints(shape);
    if (blobPts.length < 3) return;
    const d = blobPts.map((pt,j)=>(j===0?`M${pt.x.toFixed(1)},${pt.y.toFixed(1)}`:`L${pt.x.toFixed(1)},${pt.y.toFixed(1)}`)).join(' ')+' Z';
    const gid='g'+i;
    defs+=`<radialGradient id="${gid}" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="${currentColors[0]}"/><stop offset="100%" stop-color="${currentColors[1]||currentColors[0]}" stop-opacity="0.4"/></radialGradient>`;
    paths+=`<path d="${d}" fill="url(#${gid})" opacity="${p('sl-opacity')/100}"/>`;
  });
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${canvas.width}" height="${canvas.height}"><rect width="100%" height="100%" fill="#0f0f0f"/><defs>${defs}</defs>${paths}</svg>`;
  const blob=new Blob([svg],{type:'image/svg+xml'});
  const link=document.createElement('a'); link.download='blobit.svg'; link.href=URL.createObjectURL(blob); link.click();
});

document.getElementById('file-input').addEventListener('change', e => {
  const file = e.target.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => { const img=new Image(); img.onload=()=>extractAndBlobify(img); img.src=ev.target.result; };
  reader.readAsDataURL(file);
});

function extractAndBlobify(img) {
  const maxW=400,maxH=400; let w=img.width,h=img.height;
  if(w>maxW){h=h*maxW/w;w=maxW;} if(h>maxH){w=w*maxH/h;h=maxH;}
  w=Math.floor(w); h=Math.floor(h);
  const off=document.createElement('canvas'); off.width=w; off.height=h;
  const oc=off.getContext('2d'); oc.drawImage(img,0,0,w,h);
  const data=oc.getImageData(0,0,w,h); const pts=[];
  for(let y=0;y<h;y+=4) for(let x=0;x<w;x+=4) { const i=(y*w+x)*4; if(data.data[i+3]>128) pts.push({x,y}); }
  if(pts.length<5){document.getElementById('status').textContent='Could not extract shape';return;}
  const hull=convexHull(pts);
  const ox=canvas.width/2-w/2, oy=canvas.height/2-h/2;
  shapes.push({points:hull.map(pt=>({x:pt.x+ox,y:pt.y+oy})),seed:Math.random()*10000});
  render();
  document.getElementById('status').textContent='Image processed — adjust params';
}
</script>
</body>
</html>"""

with open('/Users/mogsmini/Documents/blobit/index.html', 'w') as f:
    f.write(html)

lines = html.count('\n')
print(f"Written: {len(html)} chars, {lines} lines")
print("Last line:", repr(html[-50:]))
