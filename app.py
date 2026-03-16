# Le Cavalier Sans Tête : Arbre du Lien
# streamlit run app.py

import streamlit as st
import streamlit.components.v1 as components
import json
import base64
from pathlib import Path

from src.skill_graph import SkillGraph, NodeStatus, Branch, WorldEffect
from src.skill_data import build_skill_tree, compute_layout
from src.renderer import build_tree_html


def _bgm_uri() -> str:
    path = Path(__file__).parent / "images" / "bgm.png"
    if path.exists():
        data = base64.b64encode(path.read_bytes()).decode()
        return f"data:image/png;base64,{data}"
    return ""

BGM_DATA_URI = _bgm_uri()

st.set_page_config(
    page_title="Le Cavalier Sans Tête · Arbre du Lien",
    page_icon="🐴",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap');

:root {{
    --gold:      #c9a84c;
    --gold-dim:  rgba(180,140,60,0.15);
    --text-prim: #e0cfa0;
    --text-body: #a09070;
    --text-muted:#6a5a3a;
    --terror:    #c96a6a;
    --vert:      #8fbf6a;
    --ocre:      #c97a4a;
    --border:    rgba(180,140,60,0.10);
    --surface:   #100a04;
}}

html, body {{ background: transparent !important; }}
.stApp {{
    background: #0e0a04 !important;
    /* bgm: url('{BGM_DATA_URI}') center center / cover fixed; */
    color: var(--text-body);
    font-family: 'Cormorant Garamond', serif;
}}
#MainMenu, footer, header,
section[data-testid="stSidebar"],
[data-testid="collapsedControl"] {{ visibility:hidden !important; display:none !important; }}
.main .block-container,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{ max-width:100% !important; padding:0 !important; background:transparent !important; }}

.wrap {{ max-width:1440px; margin:0 auto; padding:0 24px 48px; }}

.hdr {{
    display:flex; align-items:center; justify-content:space-between;
    padding:22px 0 14px; border-bottom:1px solid var(--border); margin-bottom:18px;
}}
.hdr-title {{
    font-family:'Cinzel',serif; font-size:1.5rem; font-weight:700;
    color:var(--text-prim); letter-spacing:0.14em; margin:0;
}}
.hdr-sub {{ font-style:italic; font-size:0.85rem; color:var(--text-muted); margin:2px 0 0; }}
.hdr-pills {{ display:flex; gap:8px; align-items:center; }}
.pill {{
    background:#0e0a04; border:1px solid var(--border);
    border-radius:5px;
    padding:4px 12px; text-align:center;
    font-family:'Cinzel',serif; font-size:9px; letter-spacing:0.08em; color:var(--text-muted);
}}
.pill strong {{ display:block; font-size:14px; color:var(--text-prim); margin-bottom:1px; }}
.pill.t strong {{ color:var(--terror); }}
.pill.e strong {{ color:var(--vert); }}
.pill.g strong {{ color:var(--gold); }}
.pill.w strong {{ font-size:10px; }}

.progbar-track {{ height:3px; background:rgba(8,5,2,0.5); border-radius:2px; overflow:hidden; margin-bottom:16px; }}
.progbar-fill {{ height:100%; background:linear-gradient(90deg,#5a3010,#c9a84c,#e8d78a); transition:width .5s ease; }}

.panel {{
    background:#100a04; border:1px solid var(--border);
    border-radius:10px; padding:16px 18px;
    margin-bottom:10px;
}}
.ptitle {{
    font-family:'Cinzel',serif; font-size:9px; font-weight:700;
    letter-spacing:0.14em; text-transform:uppercase;
    color:var(--gold); margin:0 0 12px;
    padding-bottom:7px; border-bottom:1px solid var(--border);
}}

.detail-name {{
    font-family:'Cinzel',serif; font-size:14px; font-weight:700;
    color:var(--text-prim); letter-spacing:0.05em; margin-bottom:3px;
}}
.detail-branch {{ font-size:9px; letter-spacing:0.1em; text-transform:uppercase; color:var(--text-muted); margin-bottom:10px; }}
.detail-desc {{
    font-style:italic; font-size:13.5px; line-height:1.6; color:var(--text-body);
    margin-bottom:12px; border-left:2px solid var(--border); padding-left:12px;
}}
.detail-narrative {{
    font-style:italic; font-size:12.5px; line-height:1.6; color:var(--text-muted);
    background:rgba(180,140,60,0.03); border-radius:5px; padding:10px 12px; margin-bottom:10px;
}}
.detail-fx {{ display:flex; gap:12px; font-size:11.5px; margin-bottom:10px; }}
.fx-t {{ color:var(--terror); }}
.fx-e {{ color:var(--vert); }}

.status-badge {{
    display:inline-block; padding:3px 10px; border-radius:4px;
    font-family:'Cinzel',serif; font-size:8.5px; letter-spacing:0.1em;
    text-transform:uppercase; margin-bottom:10px;
}}
.badge-unlocked  {{ background:rgba(180,140,60,0.12); color:var(--gold);  border:1px solid rgba(180,140,60,0.25); }}
.badge-available {{ background:rgba(100,140,80,0.10); color:var(--vert);  border:1px solid rgba(100,140,80,0.20); }}
.badge-locked    {{ background:rgba(80,65,40,0.10);   color:var(--text-muted); border:1px solid rgba(80,65,40,0.20); }}
.badge-blocked   {{ background:rgba(180,80,40,0.10);  color:var(--ocre); border:1px solid rgba(180,80,40,0.20); }}

.world-name {{ font-family:'Cinzel',serif; font-size:11px; font-weight:700; letter-spacing:0.07em; margin-bottom:4px; }}
.world-desc {{ font-style:italic; font-size:12.5px; line-height:1.5; color:var(--text-muted); }}

.jentry {{ border-left:2px solid var(--border); padding:8px 12px; margin:5px 0; border-radius:0 4px 4px 0; }}
.jentry.latest {{ border-left-color:var(--gold); background:rgba(180,140,60,0.02); }}
.jname {{ font-family:'Cinzel',serif; font-size:10px; color:var(--text-prim); letter-spacing:0.05em; margin-bottom:3px; }}
.jnarr {{ font-style:italic; font-size:12.5px; line-height:1.5; color:var(--text-muted); }}

.stButton > button {{
    font-family:'Cinzel',serif !important; font-size:10px !important;
    letter-spacing:0.06em !important; background:rgba(8,5,2,0.7) !important;
    color:var(--text-prim) !important; border:1px solid var(--border) !important;
    border-radius:6px !important; padding:8px 12px !important; transition:all .2s ease !important;
}}
.stButton > button:hover {{
    border-color:rgba(180,140,60,0.4) !important; color:var(--gold) !important;
    box-shadow:0 0 12px rgba(180,140,60,0.1) !important;
}}

.foot {{
    text-align:center; color:rgba(180,140,60,0.09);
    font-family:'Cinzel',serif; font-size:7px; letter-spacing:0.15em;
    padding:24px 0 0; border-top:1px solid var(--border); margin-top:32px;
}}

/* Hide the event input */
div[data-testid="stTextInput"] {{ display:none !important; }}

/* Node action buttons row */
div[data-testid="stHorizontalBlock"] .stButton > button {{
    font-size:9px !important;
    padding:5px 8px !important;
    white-space:nowrap !important;
    overflow:hidden !important;
    text-overflow:ellipsis !important;
}}
/* Forget buttons (× prefix) — reddish tint */
div[data-testid="stHorizontalBlock"] .stButton > button[data-testid*="forget"] {{
    border-color:rgba(180,80,40,0.3) !important;
    color:rgba(180,80,40,0.7) !important;
}}
div[data-testid="stHorizontalBlock"] .stButton > button[data-testid*="forget"]:hover {{
    border-color:rgba(180,80,40,0.6) !important;
    color:rgba(220,100,50,1) !important;
}}
/* Learn buttons (✦ prefix) — gold tint */
div[data-testid="stHorizontalBlock"] .stButton > button[data-testid*="learn"] {{
    border-color:rgba(180,140,60,0.35) !important;
    color:var(--gold) !important;
}}
</style>
""", unsafe_allow_html=True)


if "unlocked" not in st.session_state:
    st.session_state.unlocked = set()
if "log" not in st.session_state:
    st.session_state.log = []
if "selected" not in st.session_state:
    st.session_state.selected = None


graph = build_skill_tree()
for node in graph.nodes.values():
    for cond in node.conditions:
        cond.completed = True

graph.refresh_availability(st.session_state.unlocked)
stats       = graph.get_stats(st.session_state.unlocked)
blocked_ids = graph.get_blocked_ids(st.session_state.unlocked)

pct         = stats["percent"]
unlocked_ct = stats["unlocked"]
total_ct    = stats["total"]
terror_val  = stats["terror"]
empathy_val = stats["empathy"]
world_label = stats["world_label"]
world_color = stats["world_color"]
world_effect= stats["world_effect"]

WORLD_DESCS = {
    "neutre":         "Le monde vous ignore.",
    "legende_sombre": "Votre nom est devenu synonyme de peur.",
    "protecteur":     "On vous laisse de la nourriture aux portes des villages.",
    "incompris":      "Chaque acte de protection est mal interprété.",
    "redemption":     "Quelque chose change. Peut-être que la malédiction n'est pas une fin.",
    "equilibre":      "Ni monstre ni saint. Une force que le monde apprend à respecter.",
}
world_desc = WORLD_DESCS.get(world_effect, "")

st.markdown('<div class="wrap">', unsafe_allow_html=True)

header = (
    '<div class="hdr">'
    '<div><div class="hdr-title">L\'ARBRE DU LIEN</div>'
    '<div class="hdr-sub">Le Cavalier Sans Tête · Simulation de Progression</div></div>'
    '<div class="hdr-pills">'
    '<div class="pill g"><strong>' + str(unlocked_ct) + '/' + str(total_ct) + '</strong>Talents</div>'
    '<div class="pill t"><strong>' + str(terror_val) + '</strong>Terreur</div>'
    '<div class="pill e"><strong>' + str(empathy_val) + '</strong>Empathie</div>'
    '<div class="pill"><strong>' + str(pct) + '%</strong>Progression</div>'
    '<div class="pill w" style="border-color:' + world_color + '33;">'
    '<strong style="color:' + world_color + ';">' + world_label + '</strong>Monde</div>'
    '</div></div>'
    '<div class="progbar-track">'
    '<div class="progbar-fill" style="width:' + str(pct) + '%;"></div></div>'
)
st.markdown(header, unsafe_allow_html=True)

CANVAS_W, CANVAS_H = 1060, 640
positions      = compute_layout(graph, CANVAS_W, CANVAS_H)
tree_json      = graph.to_json(st.session_state.unlocked)
positions_json = json.dumps(positions)
html_content   = build_tree_html(tree_json, positions_json, stats, CANVAS_W, CANVAS_H)

components.html(
    '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900'
    '&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">'
    + html_content,
    height=CANVAS_H + 60,
    scrolling=False,
)

# Available nodes — rendered as small inline buttons below the canvas
available_nodes = [n for n in graph.nodes.values() if n.status == NodeStatus.AVAILABLE]
unlocked_nodes  = [n for n in graph.nodes.values() if n.status == NodeStatus.UNLOCKED]

if available_nodes or unlocked_nodes:
    cols_avail = st.columns(len(available_nodes) + len(unlocked_nodes) if (len(available_nodes) + len(unlocked_nodes)) <= 10 else 10)
    idx = 0

    for node in unlocked_nodes:
        with cols_avail[idx % 10]:
            if st.button(
                "× " + node.name,
                key="forget_" + node.id,
                help="Oublier ce talent",
                use_container_width=True,
            ):
                st.session_state.unlocked.discard(node.id)
                changed = True
                while changed:
                    changed = False
                    for uid in list(st.session_state.unlocked):
                        n = graph.nodes.get(uid)
                        if n and not all(r in st.session_state.unlocked for r in n.requires):
                            st.session_state.unlocked.discard(uid)
                            changed = True
                st.rerun()
        idx += 1

    for node in available_nodes:
        with cols_avail[idx % 10]:
            if st.button(
                "✦ " + node.name,
                key="learn_" + node.id,
                use_container_width=True,
            ):
                if graph.unlock(node.id, st.session_state.unlocked):
                    st.rerun()
        idx += 1

st.markdown('</div>', unsafe_allow_html=True)
