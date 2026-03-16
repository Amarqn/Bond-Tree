import json


def build_tree_html(tree_json: str, positions_json: str, stats: dict, canvas_w: int = 1200, canvas_h: int = 800) -> str:

    world_label = stats.get("world_label", "Monde Indifférent")
    world_color = stats.get("world_color", "#6a5a3a")
    blocked_ct  = stats.get("blocked", 0)
    blocked_html = f'<div style="text-align:center;"><div style="font-size:15px;font-weight:700;color:#8a5a3a;">{blocked_ct}</div><div style="font-size:9px;letter-spacing:0.1em;color:#5a3a2a;text-transform:uppercase;">Bloqués</div></div>' if blocked_ct > 0 else ""

    return f"""
<div id="tree-root" style="width:100%;display:flex;flex-direction:column;align-items:center;font-family:'Cinzel',serif;background:transparent;">

<div style="
    width:100%;max-width:{canvas_w}px;display:flex;justify-content:space-between;align-items:center;
    padding:10px 24px;
    background:#120c04;
    border-bottom:1px solid rgba(180,140,60,0.15);
">
    <div style="display:flex;gap:20px;align-items:center;">
        <div style="text-align:center;">
            <div style="font-size:21px;font-weight:900;color:#c9a84c;">{stats['unlocked']}</div>
            <div style="font-size:9px;letter-spacing:0.12em;color:#6a5a3a;text-transform:uppercase;">Talents</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:21px;font-weight:900;color:#c96a6a;">{stats['terror']}</div>
            <div style="font-size:9px;letter-spacing:0.12em;color:#6a3a3a;text-transform:uppercase;">Terreur</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:21px;font-weight:900;color:#8fbf6a;">{stats['empathy']}</div>
            <div style="font-size:9px;letter-spacing:0.12em;color:#4a6a3a;text-transform:uppercase;">Empathie</div>
        </div>
        {blocked_html}
    </div>
    <div style="text-align:right;">
        <div style="font-size:11px;color:{world_color};font-weight:700;letter-spacing:0.08em;">{world_label}</div>
        <div style="font-size:10px;color:#5a4e3a;">{stats['title']} · {stats['unlocked']}/{stats['total']}</div>
    </div>
</div>

<div style="width:100%;max-width:{canvas_w}px;height:3px;background:rgba(10,6,2,0.4);overflow:hidden;">
    <div style="width:{int(stats['ratio']*100)}%;height:100%;background:linear-gradient(90deg,#5a3010,#c9a84c,#e8d78a);transition:width 0.6s ease;"></div>
</div>

<canvas id="skillCanvas" width="{canvas_w}" height="{canvas_h}" style="display:block;cursor:default;background:#0e0a04;border-radius:10px;"></canvas>

<div id="tooltip" style="
    display:none;position:fixed;z-index:9999;pointer-events:none;
    max-width:320px;
    background:rgba(10,6,2,0.90);
    backdrop-filter:blur(12px);
    border:1px solid rgba(180,140,60,0.28);
    border-radius:8px;
    box-shadow:0 8px 32px rgba(0,0,0,0.7);
    overflow:hidden;
    font-family:'Cormorant Garamond',serif;
">
    <div id="tt-header" style="padding:10px 14px 8px;background:rgba(180,140,60,0.05);border-bottom:1px solid rgba(180,140,60,0.12);">
        <div style="display:flex;align-items:center;gap:8px;">
            <div id="tt-dot" style="width:10px;height:10px;border-radius:50%;flex-shrink:0;"></div>
            <span id="tt-name" style="font-family:'Cinzel',serif;font-size:12px;font-weight:700;color:#e8d5a3;letter-spacing:0.05em;"></span>
        </div>
        <div id="tt-branch" style="font-size:9px;color:#6a5a3a;letter-spacing:0.1em;text-transform:uppercase;margin-top:2px;margin-left:18px;"></div>
    </div>
    <div style="padding:10px 14px;">
        <p id="tt-desc" style="font-size:13px;color:#a09070;line-height:1.5;margin:0 0 8px;font-style:italic;"></p>
        <div id="tt-conditions" style="margin-bottom:8px;"></div>
        <div id="tt-effects" style="display:flex;gap:10px;font-size:11px;margin-bottom:7px;"></div>
        <div id="tt-conflicts" style="display:none;background:rgba(180,80,40,0.07);border:1px solid rgba(180,80,40,0.18);border-radius:4px;padding:5px 8px;margin-bottom:7px;font-size:11px;color:#c97a4a;"></div>
        <div id="tt-world-req" style="display:none;background:rgba(140,100,40,0.07);border:1px solid rgba(140,100,40,0.18);border-radius:4px;padding:5px 8px;margin-bottom:7px;font-size:11px;color:#c9a84c;"></div>
        <div id="tt-status" style="padding-top:6px;border-top:1px solid rgba(180,140,60,0.1);font-family:'Cinzel',serif;font-size:9px;letter-spacing:0.1em;text-transform:uppercase;text-align:center;"></div>
    </div>
</div>

<div id="detail-panel" style="
    width:100%;max-width:{canvas_w}px;margin-top:10px;display:none;
    background:rgba(10,6,2,0.85);backdrop-filter:blur(12px);
    border:1px solid rgba(180,140,60,0.18);border-radius:8px;padding:16px 24px;
">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
        <div id="dp-dot" style="width:14px;height:14px;border-radius:50%;flex-shrink:0;box-shadow:0 0 8px currentColor;"></div>
        <div>
            <div id="dp-name" style="font-family:'Cinzel',serif;font-size:14px;font-weight:700;color:#e8d5a3;"></div>
            <div id="dp-branch" style="font-size:9px;color:#6a5a3a;letter-spacing:0.1em;text-transform:uppercase;"></div>
        </div>
        <div id="dp-world-badge" style="display:none;margin-left:auto;padding:3px 9px;border-radius:4px;font-family:'Cinzel',serif;font-size:9px;letter-spacing:0.08em;text-transform:uppercase;"></div>
    </div>
    <div id="dp-narrative" style="border-left:2px solid rgba(180,140,60,0.3);padding:9px 14px;margin:9px 0;font-family:'Cormorant Garamond',serif;font-style:italic;color:#a09070;font-size:14px;line-height:1.6;background:rgba(180,140,60,0.02);border-radius:0 5px 5px 0;"></div>
    <div id="dp-world-change" style="display:none;margin:7px 0;padding:7px 11px;background:rgba(140,100,40,0.05);border:1px dashed rgba(140,100,40,0.16);border-radius:4px;font-size:12px;color:#8a7a5a;font-style:italic;font-family:'Cormorant Garamond',serif;"></div>
    <div id="dp-conditions-full" style="margin-top:9px;"></div>
    <div id="dp-path" style="font-size:11px;color:#5a4e3a;margin-top:7px;font-family:'Cormorant Garamond',serif;"></div>
    <div id="dp-conflicts-full" style="display:none;margin-top:7px;padding:7px 11px;background:rgba(180,80,40,0.04);border:1px solid rgba(180,80,40,0.12);border-radius:4px;font-size:12px;color:#c97a4a;font-family:'Cormorant Garamond',serif;"></div>
</div>

<div style="width:100%;max-width:{canvas_w}px;display:flex;justify-content:center;gap:18px;flex-wrap:wrap;margin-top:8px;padding:6px 0;font-family:'Cinzel',serif;font-size:9px;letter-spacing:0.06em;color:rgba(100,85,55,0.65);">
    <span><span style="color:#c9a84c;">●</span> Confiance</span>
    <span><span style="color:#8fbf6a;">●</span> Communication</span>
    <span><span style="color:#c97a4a;">●</span> Traversée</span>
    <span><span style="color:#c96a6a;">●</span> Mémoire</span>
    <span><span style="color:#8a6a4a;">●</span> Survie</span>
    <span style="margin-left:6px;color:rgba(180,140,60,0.5);">◉ Disponible</span>
    <span style="color:rgba(180,140,60,0.9);">● Débloqué</span>
    <span style="color:rgba(80,65,40,0.5);">○ Verrouillé</span>
    <span style="color:rgba(180,80,40,0.6);">⊗ Bloqué</span>
</div>

</div>

<script>
(function() {{
    const treeData  = {tree_json};
    const positions = {positions_json};
    const CANVAS_W  = {canvas_w};
    const CANVAS_H  = {canvas_h};

    const canvas = document.getElementById('skillCanvas');
    const ctx    = canvas.getContext('2d');
    const tooltip     = document.getElementById('tooltip');
    const detailPanel = document.getElementById('detail-panel');

    const dpr = window.devicePixelRatio || 1;
    canvas.width  = CANVAS_W * dpr;
    canvas.height = CANVAS_H * dpr;
    canvas.style.width  = CANVAS_W + 'px';
    canvas.style.height = CANVAS_H + 'px';
    ctx.scale(dpr, dpr);

    let hoveredNode  = null;
    let selectedNode = null;
    let animFrame    = 0;

    const branchColors = {{}};
    for (const [k, v] of Object.entries(treeData.branches)) branchColors[k] = v.color;

    // Node sizes by status
    const R_UNLOCKED  = 18;
    const R_AVAILABLE = 14;
    const R_LOCKED    = 7;
    const R_BLOCKED   = 7;
    const HIT_R       = 22;   // generous hit area

    // Floating dust
    const dust = Array.from({{length:25}}, () => ({{
        x: Math.random() * CANVAS_W,
        y: Math.random() * CANVAS_H,
        r: Math.random() * 0.9 + 0.2,
        speed: Math.random() * 0.18 + 0.05,
        opacity: Math.random() * 0.18 + 0.03,
        drift: (Math.random() - 0.5) * 0.15,
    }}));

    function drawPumpkin() {{
        const cx = 530, cy = 340;
        ctx.save();
        ctx.globalAlpha = 0.07;

        // Main body — 5 ridge lobes using bezier curves
        const lobes = [
            {{ x: cx - 245, rx: 68, ry: 195 }},  // far-left
            {{ x: cx - 120, rx: 75, ry: 210 }},  // left
            {{ x: cx,       rx: 78, ry: 220 }},  // center
            {{ x: cx + 120, rx: 75, ry: 210 }},  // right
            {{ x: cx + 245, rx: 68, ry: 195 }},  // far-right
        ];

        for (const lobe of lobes) {{
            ctx.beginPath();
            ctx.ellipse(lobe.x, cy + 20, lobe.rx, lobe.ry, 0, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(200,130,30,0.9)';
            ctx.lineWidth = 1.5;
            ctx.stroke();
        }}

        // Outer silhouette
        ctx.beginPath();
        ctx.ellipse(cx, cy + 20, 275, 225, 0, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(200,130,30,0.5)';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Stem
        ctx.beginPath();
        ctx.moveTo(cx - 10, 145);
        ctx.bezierCurveTo(cx - 20, 100, cx + 30, 80, cx + 15, 55);
        ctx.strokeStyle = 'rgba(80,160,60,0.8)';
        ctx.lineWidth = 6;
        ctx.lineCap = 'round';
        ctx.stroke();

        // Left eye (triangle-ish)
        ctx.beginPath();
        ctx.moveTo(340, 220); ctx.lineTo(390, 185); ctx.lineTo(440, 220);
        ctx.lineTo(420, 285); ctx.lineTo(360, 285); ctx.closePath();
        ctx.strokeStyle = 'rgba(240,160,20,0.7)';
        ctx.lineWidth = 1.2;
        ctx.stroke();

        // Right eye
        ctx.beginPath();
        ctx.moveTo(620, 220); ctx.lineTo(670, 185); ctx.lineTo(720, 220);
        ctx.lineTo(700, 285); ctx.lineTo(640, 285); ctx.closePath();
        ctx.stroke();

        // Nose triangle
        ctx.beginPath();
        ctx.moveTo(510, 350); ctx.lineTo(530, 320); ctx.lineTo(550, 350);
        ctx.lineTo(530, 375); ctx.closePath();
        ctx.stroke();

        // Mouth — jagged
        ctx.beginPath();
        ctx.moveTo(345, 490);
        ctx.lineTo(385, 520); ctx.lineTo(415, 490);
        ctx.lineTo(455, 540); ctx.lineTo(495, 500);
        ctx.lineTo(530, 545); ctx.lineTo(565, 500);
        ctx.lineTo(605, 540); ctx.lineTo(645, 490);
        ctx.lineTo(675, 520); ctx.lineTo(715, 490);
        ctx.strokeStyle = 'rgba(240,160,20,0.7)';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        ctx.restore();
    }}

    function drawDust() {{
        for (const p of dust) {{
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            const flicker = 0.5 + 0.5 * Math.sin(animFrame * 0.012 + p.x * 0.008);
            ctx.fillStyle = `rgba(180,140,60,${{p.opacity * flicker}})`;
            ctx.fill();
            p.y -= p.speed; p.x += p.drift;
            if (p.y < -4) {{ p.y = CANVAS_H + 4; p.x = Math.random() * CANVAS_W; }}
            if (p.x < 0 || p.x > CANVAS_W) p.x = Math.random() * CANVAS_W;
        }}
    }}

    function drawEdges() {{
        for (const [pid, cid] of treeData.edges) {{
            const p1 = positions[pid];
            const p2 = positions[cid];
            if (!p1 || !p2) continue;

            const pn = treeData.nodes[pid];
            const cn = treeData.nodes[cid];
            const lit     = pn?.status === 'unlocked' && cn?.status === 'unlocked';
            const active  = pn?.status === 'unlocked' && cn?.status === 'available';
            const blocked = cn?.status === 'blocked';

            ctx.beginPath();
            ctx.moveTo(p1[0], p1[1]);

            // Straight lines for a clean tree
            const midX = (p1[0] + p2[0]) / 2;
            const midY = (p1[1] + p2[1]) / 2;
            ctx.lineTo(p2[0], p2[1]);

            ctx.setLineDash([]);
            if (blocked) {{
                ctx.strokeStyle = 'rgba(160,60,30,0.2)';
                ctx.lineWidth   = 0.8;
                ctx.setLineDash([3, 5]);
                ctx.shadowBlur  = 0;
            }} else if (lit) {{
                const color = branchColors[pn.branch] || '#c9a84c';
                ctx.strokeStyle = color + 'cc';
                ctx.lineWidth   = 1.5;
                ctx.shadowColor = color;
                ctx.shadowBlur  = 6;
            }} else if (active) {{
                const color = branchColors[pn.branch] || '#c9a84c';
                ctx.strokeStyle = color + '55';
                ctx.lineWidth   = 1;
                ctx.shadowBlur  = 0;
            }} else {{
                ctx.strokeStyle = 'rgba(70,58,35,0.25)';
                ctx.lineWidth   = 0.8;
                ctx.shadowBlur  = 0;
            }}
            ctx.stroke();
            ctx.setLineDash([]);
            ctx.shadowBlur = 0;
        }}
    }}

    function getNodeR(status) {{
        if (status === 'unlocked')  return R_UNLOCKED;
        if (status === 'available') return R_AVAILABLE;
        if (status === 'blocked')   return R_BLOCKED;
        return R_LOCKED;
    }}

    function drawNode(nid) {{
        const node = treeData.nodes[nid];
        const pos  = positions[nid];
        if (!node || !pos) return;

        const [x, y] = pos;
        const hov    = hoveredNode === nid;
        const color  = branchColors[node.branch] || '#c9a84c';
        const status = node.status;
        const r      = getNodeR(status) + (hov ? 2 : 0);

        ctx.save();

        if (status === 'unlocked') {{
            const pulse = 0.6 + 0.3 * Math.sin(animFrame * 0.03 + x * 0.015);
            const grad = ctx.createRadialGradient(x, y, r, x, y, r + 14);
            grad.addColorStop(0, color + Math.round(pulse * 80).toString(16).padStart(2,'0'));
            grad.addColorStop(1, color + '00');
            ctx.beginPath();
            ctx.arc(x, y, r + 14, 0, Math.PI * 2);
            ctx.fillStyle = grad;
            ctx.fill();

            // Core dot — fully lit
            ctx.beginPath();
            ctx.arc(x, y, r, 0, Math.PI * 2);
            ctx.fillStyle = color;
            ctx.shadowColor = color;
            ctx.shadowBlur  = hov ? 22 : 14;
            ctx.fill();
            ctx.shadowBlur  = 0;

            ctx.beginPath();
            ctx.arc(x - r * 0.22, y - r * 0.22, r * 0.38, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(255,255,255,0.5)';
            ctx.fill();

        }} else if (status === 'available') {{
            const pulse = 0.6 + 0.4 * Math.sin(animFrame * 0.055);
            ctx.beginPath();
            ctx.arc(x, y, r + 8, 0, Math.PI * 2);
            ctx.strokeStyle = color + Math.round(pulse * 180).toString(16).padStart(2,'0');
            ctx.lineWidth   = 1.5;
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(x, y, r, 0, Math.PI * 2);
            ctx.fillStyle   = color + '88';
            ctx.shadowColor = color;
            ctx.shadowBlur  = hov ? 20 : 12;
            ctx.fill();
            ctx.shadowBlur  = 0;

            ctx.beginPath();
            ctx.arc(x, y, r, 0, Math.PI * 2);
            ctx.strokeStyle = color + 'dd';
            ctx.lineWidth   = 2;
            ctx.stroke();

        }} else if (status === 'blocked') {{
            ctx.beginPath();
            ctx.arc(x, y, r, 0, Math.PI * 2);
            ctx.fillStyle   = 'rgba(160,60,30,0.25)';
            ctx.strokeStyle = 'rgba(160,60,30,0.35)';
            ctx.lineWidth   = 0.8;
            ctx.fill();
            ctx.stroke();

        }} else {{
            ctx.beginPath();
            ctx.arc(x, y, r, 0, Math.PI * 2);
            ctx.fillStyle   = 'rgba(80,65,40,0.55)';
            ctx.strokeStyle = 'rgba(120,100,60,0.6)';
            ctx.lineWidth   = 1.2;
            ctx.fill();
            ctx.stroke();
        }}

        ctx.restore();

        // Name label
        ctx.save();
        ctx.font = `600 10px 'Cinzel', serif`;
        ctx.textAlign    = 'center';
        ctx.textBaseline = 'top';
        if      (status === 'unlocked')  ctx.fillStyle = color;
        else if (status === 'available') ctx.fillStyle = color + 'cc';
        else if (status === 'blocked')   ctx.fillStyle = 'rgba(160,80,40,0.55)';
        else                              ctx.fillStyle = 'rgba(140,115,70,0.7)';
        ctx.fillText(node.name, x, y + r + 5);
        ctx.restore();
    }}

    function render() {{
        animFrame++;
        ctx.clearRect(0, 0, CANVAS_W, CANVAS_H);
        drawDust();
        drawPumpkin();
        drawEdges();
        for (const status of ['locked', 'blocked', 'available', 'unlocked']) {{
            for (const nid of Object.keys(treeData.nodes)) {{
                if (treeData.nodes[nid].status === status) drawNode(nid);
            }}
        }}
        requestAnimationFrame(render);
    }}

    function nodeAt(mx, my) {{
        const ids = Object.keys(positions);
        for (let i = ids.length - 1; i >= 0; i--) {{
            const [nx, ny] = positions[ids[i]];
            if ((mx - nx) ** 2 + (my - ny) ** 2 <= HIT_R ** 2) return ids[i];
        }}
        return null;
    }}

    function conditionsHtml(node, compact) {{
        if (!node.conditions?.length) return '';
        const rows = node.conditions.map(c => {{
            const done = c.completed;
            return `<div style="display:flex;gap:6px;align-items:flex-start;margin:2px 0;">
                <span style="color:${{done ? '#8fbf6a' : '#6a5a3a'}};font-size:10px;flex-shrink:0;margin-top:1px;">${{done ? '✓' : '○'}}</span>
                <span style="font-size:${{compact ? 11 : 12}}px;color:${{done ? '#6a7a5a' : '#7a6a4a'}};text-decoration:${{done ? 'line-through' : 'none'}};line-height:1.4;">${{compact ? c.label : c.description}}</span>
            </div>`;
        }}).join('');
        return `<div style="margin-bottom:6px;"><div style="font-size:8.5px;color:#6a5a3a;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;">${{compact ? 'Conditions' : 'Conditions de déblocage'}}</div>${{rows}}</div>`;
    }}

    function showTooltip(nid, cx, cy) {{
        const node  = treeData.nodes[nid];
        if (!node) return;
        const color = branchColors[node.branch] || '#c9a84c';
        const br    = treeData.branches[node.branch];

        document.getElementById('tt-dot').style.background  = color;
        document.getElementById('tt-dot').style.boxShadow   = `0 0 6px ${{color}}`;
        document.getElementById('tt-name').textContent       = node.name;
        document.getElementById('tt-branch').textContent     = br?.name || node.branch;
        document.getElementById('tt-desc').textContent       = node.description;
        document.getElementById('tt-conditions').innerHTML   = conditionsHtml(node, true);

        let fx = '';
        if (node.terror_delta  > 0) fx += `<span style="color:#c96a6a;">Terreur +${{node.terror_delta}}</span>`;
        if (node.terror_delta  < 0) fx += `<span style="color:#8fbf6a;">Terreur ${{node.terror_delta}}</span>`;
        if (node.empathy_delta > 0) fx += `<span style="color:#8fbf6a;">Empathie +${{node.empathy_delta}}</span>`;
        if (node.empathy_delta < 0) fx += `<span style="color:#c96a6a;">Empathie ${{node.empathy_delta}}</span>`;
        document.getElementById('tt-effects').innerHTML = fx;

        const cfEl = document.getElementById('tt-conflicts');
        if (node.blocks?.length) {{
            cfEl.textContent  = `⚠ Bloque : ${{node.blocks.map(b => treeData.nodes[b]?.name || b).join(', ')}}`;
            cfEl.style.display = 'block';
        }} else cfEl.style.display = 'none';

        const wEl = document.getElementById('tt-world-req');
        if (node.requires_world_effect) {{
            wEl.textContent  = `Requiert : ${{node.requires_world_effect}}`;
            wEl.style.display = 'block';
        }} else wEl.style.display = 'none';

        const stEl = document.getElementById('tt-status');
        if      (node.status === 'unlocked')  stEl.innerHTML = `<span style="color:${{color}};">✦ Débloqué</span>`;
        else if (node.status === 'available') stEl.innerHTML = '<span style="color:#8a8a6a;">◉ Disponible — cliquez</span>';
        else if (node.status === 'blocked')   stEl.innerHTML = '<span style="color:#c97a4a;">⊗ Bloqué par conflit</span>';
        else {{
            const reqs = (node.requires || []).filter(r => treeData.nodes[r]?.status !== 'unlocked');
            const names = reqs.map(r => treeData.nodes[r]?.name || r).join(', ');
            stEl.innerHTML = names
                ? `<span style="color:#4a3e2e;">Requiert : ${{names}}</span>`
                : `<span style="color:#4a3e2e;">Conditions non remplies</span>`;
        }}

        tooltip.style.display = 'block';
        const tr = tooltip.getBoundingClientRect();
        let left = cx + 16, top = cy - 20;
        if (left + tr.width  > window.innerWidth  - 20) left = cx - tr.width  - 16;
        if (top  + tr.height > window.innerHeight - 20) top  = window.innerHeight - tr.height - 20;
        if (top < 10) top = 10;
        tooltip.style.left = left + 'px';
        tooltip.style.top  = top  + 'px';
    }}

    function showDetail(nid) {{
        const node  = treeData.nodes[nid];
        if (!node) return;
        const color = branchColors[node.branch] || '#c9a84c';
        const br    = treeData.branches[node.branch];

        const dpDot = document.getElementById('dp-dot');
        dpDot.style.background = color;
        dpDot.style.boxShadow  = `0 0 10px ${{color}}`;

        document.getElementById('dp-name').textContent     = node.name;
        document.getElementById('dp-branch').textContent   = br?.name || '';
        document.getElementById('dp-narrative').textContent = node.narrative_effect;

        const wcEl = document.getElementById('dp-world-change');
        if (node.world_change_text && node.status === 'unlocked') {{
            wcEl.textContent   = '↳ ' + node.world_change_text;
            wcEl.style.display = 'block';
        }} else wcEl.style.display = 'none';

        document.getElementById('dp-conditions-full').innerHTML = conditionsHtml(node, false);

        const reqs = (node.requires || []).map(r => treeData.nodes[r]?.name || r);
        document.getElementById('dp-path').innerHTML = reqs.length
            ? `Prérequis : ${{reqs.join(' → ')}}`
            : 'Talent racine';

        const cfEl = document.getElementById('dp-conflicts-full');
        if (node.blocks?.length) {{
            cfEl.innerHTML     = `Conflit : rend inaccessible <em>${{node.blocks.map(b => treeData.nodes[b]?.name || b).join(', ')}}</em>`;
            cfEl.style.display = 'block';
        }} else cfEl.style.display = 'none';

        const badge = document.getElementById('dp-world-badge');
        if (node.requires_world_effect) {{
            badge.textContent      = node.requires_world_effect;
            badge.style.display    = 'block';
            badge.style.background = 'rgba(140,100,40,0.1)';
            badge.style.border     = '1px solid rgba(140,100,40,0.25)';
            badge.style.color      = '#c9a84c';
        }} else badge.style.display = 'none';

        detailPanel.style.display = 'block';
    }}

    canvas.addEventListener('mousemove', e => {{
        const rect = canvas.getBoundingClientRect();
        const mx   = (e.clientX - rect.left) * (CANVAS_W / rect.width);
        const my   = (e.clientY - rect.top)  * (CANVAS_H / rect.height);
        const hit  = nodeAt(mx, my);
        hoveredNode = hit;
        canvas.style.cursor = hit ? 'pointer' : 'default';
        if (hit) showTooltip(hit, e.clientX, e.clientY);
        else tooltip.style.display = 'none';
    }});

    canvas.addEventListener('mouseleave', () => {{
        hoveredNode = null;
        tooltip.style.display = 'none';
    }});

    function sendToStreamlit(payload) {{
        const doc = window.parent.document;
        const inputs = doc.querySelectorAll('input[type="text"]');
        for (const inp of inputs) {{
            if (inp.value === '' || inp.getAttribute('data-canvas') === '1') {{
                inp.setAttribute('data-canvas', '1');
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(inp, JSON.stringify(payload));
                inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                break;
            }}
        }}
    }}

    canvas.addEventListener('contextmenu', e => {{
        e.preventDefault();
        const rect = canvas.getBoundingClientRect();
        const mx   = (e.clientX - rect.left) * (CANVAS_W / rect.width);
        const my   = (e.clientY - rect.top)  * (CANVAS_H / rect.height);
        const hit  = nodeAt(mx, my);
        if (!hit) return;
        const node = treeData.nodes[hit];
        if (node.status === 'unlocked') {{
            node.status = 'available';
            sendToStreamlit({{ action: 'forget', id: hit }});
        }}
    }});

    canvas.addEventListener('click', e => {{
        const rect = canvas.getBoundingClientRect();
        const mx   = (e.clientX - rect.left) * (CANVAS_W / rect.width);
        const my   = (e.clientY - rect.top)  * (CANVAS_H / rect.height);
        const hit  = nodeAt(mx, my);
        if (!hit) return;
        const node = treeData.nodes[hit];

        if (node.status === 'available') {{
            node.status = 'unlocked';
            const unlocked = new Set(Object.keys(treeData.nodes).filter(k => treeData.nodes[k].status === 'unlocked'));
            const blocked  = new Set();
            for (const uid of unlocked) for (const b of (treeData.nodes[uid].blocks || [])) blocked.add(b);
            for (const [nid, n] of Object.entries(treeData.nodes)) {{
                if (unlocked.has(nid)) continue;
                if (blocked.has(nid))  {{ n.status = 'blocked'; continue; }}
                n.status = (n.requires || []).every(r => unlocked.has(r)) ? 'available' : 'locked';
            }}
            sendToStreamlit({{ action: 'unlock', id: hit }});
        }} else {{
            sendToStreamlit({{ action: 'select', id: hit }});
        }}

        selectedNode = hit;
        showDetail(hit);
    }});

    render();
}})();
</script>
"""
