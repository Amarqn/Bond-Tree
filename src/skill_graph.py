from __future__ import annotations
import json
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
from typing import Optional


class NodeStatus(Enum):
    LOCKED    = "locked"
    AVAILABLE = "available"
    UNLOCKED  = "unlocked"
    BLOCKED   = "blocked"


class Branch(Enum):
    CONFIANCE     = "confiance"
    COMMUNICATION = "communication"
    TRAVERSEE     = "traversee"
    MEMOIRE       = "memoire"
    SURVIE        = "survie"

    @property
    def display_name(self) -> str:
        return {
            Branch.CONFIANCE:     "Confiance",
            Branch.COMMUNICATION: "Communication",
            Branch.TRAVERSEE:     "Traversée",
            Branch.MEMOIRE:       "Mémoire",
            Branch.SURVIE:        "Survie",
        }[self]

    @property
    def color(self) -> str:
        return {
            Branch.CONFIANCE:     "#c9a84c",
            Branch.COMMUNICATION: "#8fbf6a",
            Branch.TRAVERSEE:     "#c97a4a",
            Branch.MEMOIRE:       "#c96a6a",
            Branch.SURVIE:        "#8a6a4a",
        }[self]

    @property
    def icon(self) -> str:
        return {
            Branch.CONFIANCE:     "🤝",
            Branch.COMMUNICATION: "💬",
            Branch.TRAVERSEE:     "🌍",
            Branch.MEMOIRE:       "📖",
            Branch.SURVIE:        "⚔️",
        }[self]

    @property
    def glyph(self) -> str:
        return {
            Branch.CONFIANCE:     "C",
            Branch.COMMUNICATION: "K",
            Branch.TRAVERSEE:     "T",
            Branch.MEMOIRE:       "M",
            Branch.SURVIE:        "S",
        }[self]


class WorldEffect(Enum):
    NEUTRE         = "neutre"
    LEGENDE_SOMBRE = "legende_sombre"
    PROTECTEUR     = "protecteur"
    INCOMPRIS      = "incompris"
    REDEMPTION     = "redemption"
    EQUILIBRE      = "equilibre"


@dataclass
class ActivityCondition:
    id: str
    label: str
    description: str
    completed: bool = False

    def to_dict(self) -> dict:
        return {
            "id":          self.id,
            "label":       self.label,
            "description": self.description,
            "completed":   self.completed,
        }


@dataclass
class SkillNode:
    id: str
    name: str
    icon: str
    description: str
    narrative_effect: str
    branch: Branch
    tier: int
    terror_delta: int = 0
    empathy_delta: int = 0
    requires: list[str] = field(default_factory=list)
    conditions: list[ActivityCondition] = field(default_factory=list)
    blocks: list[str] = field(default_factory=list)
    requires_world_effect: Optional[WorldEffect] = None
    world_change_text: str = ""
    min_empathy: int = 0
    min_terror: int = 0

    status: NodeStatus = field(default=NodeStatus.LOCKED, repr=False)

    @property
    def unlock_activity(self) -> str:
        if not self.conditions:
            return ""
        if len(self.conditions) == 1:
            return self.conditions[0].label
        return " · ".join(c.label for c in self.conditions)

    @property
    def conditions_met(self) -> bool:
        return all(c.completed for c in self.conditions)

    def to_dict(self) -> dict:
        return {
            "id":                    self.id,
            "name":                  self.name,
            "icon":                  self.icon,
            "description":           self.description,
            "unlock_activity":       self.unlock_activity,
            "narrative_effect":      self.narrative_effect,
            "branch":                self.branch.value,
            "branch_glyph":          self.branch.glyph,
            "tier":                  self.tier,
            "terror_delta":          self.terror_delta,
            "empathy_delta":         self.empathy_delta,
            "requires":              self.requires,
            "blocks":                self.blocks,
            "conditions":            [c.to_dict() for c in self.conditions],
            "conditions_met":        self.conditions_met,
            "requires_world_effect": self.requires_world_effect.value if self.requires_world_effect else None,
            "world_change_text":     self.world_change_text,
            "min_empathy":           self.min_empathy,
            "min_terror":            self.min_terror,
            "status":                self.status.value,
        }


class SkillGraph:
    def __init__(self):
        self.nodes:   dict[str, SkillNode] = {}
        self.forward: dict[str, list[str]] = {}
        self.reverse: dict[str, list[str]] = {}

    def add_node(self, node: SkillNode) -> None:
        self.nodes[node.id] = node
        self.forward.setdefault(node.id, [])
        self.reverse.setdefault(node.id, [])
        for req in node.requires:
            self.forward.setdefault(req, [])
            self.forward[req].append(node.id)
            self.reverse[node.id].append(req)

    def get_roots(self) -> list[str]:
        return [nid for nid, parents in self.reverse.items() if not parents]

    def get_children(self, node_id: str) -> list[str]:
        return self.forward.get(node_id, [])

    def get_parents(self, node_id: str) -> list[str]:
        return self.reverse.get(node_id, [])

    def get_branch_nodes(self, branch: Branch) -> list[SkillNode]:
        return [n for n in self.nodes.values() if n.branch == branch]

    def compute_world_effect(self, unlocked: set[str]) -> WorldEffect:
        terror  = sum(self.nodes[n].terror_delta  for n in unlocked if n in self.nodes)
        empathy = sum(self.nodes[n].empathy_delta for n in unlocked if n in self.nodes)
        total   = terror + empathy
        if total == 0:
            return WorldEffect.NEUTRE
        if empathy > 80 and terror < 20:
            return WorldEffect.REDEMPTION
        if abs(terror - empathy) < 10 and total > 40:
            return WorldEffect.EQUILIBRE
        if terror >= 40:
            return WorldEffect.LEGENDE_SOMBRE
        if empathy >= 60:
            return WorldEffect.PROTECTEUR
        if total > 0 and terror > empathy * 2:
            return WorldEffect.INCOMPRIS
        return WorldEffect.NEUTRE

    def get_blocked_ids(self, unlocked: set[str]) -> set[str]:
        blocked = set()
        for nid in unlocked:
            node = self.nodes.get(nid)
            if node:
                blocked.update(node.blocks)
        return blocked

    def refresh_availability(self, unlocked: set[str]) -> None:
        blocked_ids  = self.get_blocked_ids(unlocked)
        world_effect = self.compute_world_effect(unlocked)
        terror  = sum(self.nodes[n].terror_delta  for n in unlocked if n in self.nodes)
        empathy = sum(self.nodes[n].empathy_delta for n in unlocked if n in self.nodes)
        for nid, node in self.nodes.items():
            if nid in unlocked:
                node.status = NodeStatus.UNLOCKED
                continue
            if nid in blocked_ids:
                node.status = NodeStatus.BLOCKED
                continue
            prereqs_ok    = all(r in unlocked for r in node.requires)
            conditions_ok = node.conditions_met
            world_ok      = node.requires_world_effect is None or node.requires_world_effect == world_effect
            reputation_ok = empathy >= node.min_empathy and terror >= node.min_terror
            node.status   = NodeStatus.AVAILABLE if (prereqs_ok and conditions_ok and world_ok and reputation_ok) else NodeStatus.LOCKED

    def complete_condition(self, node_id: str, condition_id: str, unlocked: set[str]) -> bool:
        node = self.nodes.get(node_id)
        if not node:
            return False
        for cond in node.conditions:
            if cond.id == condition_id:
                cond.completed = True
                self.refresh_availability(unlocked)
                return True
        return False

    def unlock(self, node_id: str, unlocked: set[str]) -> bool:
        node = self.nodes.get(node_id)
        if not node or node_id in unlocked:
            return False
        if node.status != NodeStatus.AVAILABLE:
            return False
        unlocked.add(node_id)
        self.refresh_availability(unlocked)
        return True

    def topological_sort(self) -> list[str]:
        in_degree = {nid: len(parents) for nid, parents in self.reverse.items()}
        queue     = deque([nid for nid, d in in_degree.items() if d == 0])
        result    = []
        while queue:
            current = queue.popleft()
            result.append(current)
            for child in self.forward.get(current, []):
                in_degree[child] -= 1
                if in_degree[child] == 0:
                    queue.append(child)
        if len(result) != len(self.nodes):
            raise ValueError("Cycle détecté dans le graphe.")
        return result

    def bfs_reachable(self, start: str) -> set[str]:
        visited = set()
        queue   = deque([start])
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            for child in self.forward.get(current, []):
                if child not in visited:
                    queue.append(child)
        visited.discard(start)
        return visited

    def shortest_path_to(self, target: str, unlocked: set[str]) -> list[str]:
        if target in unlocked:
            return []
        needed = set()
        queue  = deque([target])
        while queue:
            current = queue.popleft()
            if current in needed or current in unlocked:
                continue
            needed.add(current)
            for parent in self.reverse.get(current, []):
                if parent not in unlocked:
                    queue.append(parent)
        topo = self.topological_sort()
        return [nid for nid in topo if nid in needed]

    def compute_subtree_weight(self, node_id: str) -> dict:
        reachable = self.bfs_reachable(node_id) | {node_id}
        return {
            "nodes":         len(reachable),
            "total_terror":  sum(self.nodes[nid].terror_delta  for nid in reachable),
            "total_empathy": sum(self.nodes[nid].empathy_delta for nid in reachable),
        }

    def validate(self) -> list[str]:
        issues = []
        for nid, node in self.nodes.items():
            for req in node.requires:
                if req not in self.nodes:
                    issues.append(f"'{nid}' requiert '{req}' introuvable")
            for blk in node.blocks:
                if blk not in self.nodes:
                    issues.append(f"'{nid}' bloque '{blk}' introuvable")
        try:
            self.topological_sort()
        except ValueError as e:
            issues.append(str(e))
        if not self.get_roots():
            issues.append("Aucun nœud racine trouvé")
        return issues

    def get_all_edges(self) -> list[tuple[str, str]]:
        edges = []
        for parent, children in self.forward.items():
            for child in children:
                edges.append((parent, child))
        return edges

    def to_json(self, unlocked: set[str]) -> str:
        self.refresh_availability(unlocked)
        world_effect = self.compute_world_effect(unlocked)
        data = {
            "nodes":        {nid: node.to_dict() for nid, node in self.nodes.items()},
            "edges":        self.get_all_edges(),
            "branches":     {b.value: {"name": b.display_name, "color": b.color, "glyph": b.glyph} for b in Branch},
            "world_effect": world_effect.value,
        }
        return json.dumps(data, ensure_ascii=False)

    def get_stats(self, unlocked: set[str]) -> dict:
        total        = len(self.nodes)
        done         = len(unlocked)
        terror       = sum(self.nodes[n].terror_delta  for n in unlocked if n in self.nodes)
        empathy      = sum(self.nodes[n].empathy_delta for n in unlocked if n in self.nodes)
        ratio        = done / total if total > 0 else 0
        world_effect = self.compute_world_effect(unlocked)
        blocked      = len(self.get_blocked_ids(unlocked))

        if ratio == 0:       title = "Inconnus"
        elif ratio < 0.15:   title = "Étrangers Méfiants"
        elif ratio < 0.3:    title = "Compagnons Hésitants"
        elif ratio < 0.5:    title = "Partenaires de Route"
        elif ratio < 0.7:    title = "Âmes Liées"
        elif ratio < 0.9:    title = "Lien Indéfectible"
        else:                title = "Lien Transcendant ✦"

        world_labels = {
            WorldEffect.NEUTRE:         ("Monde Indifférent",     "#6a5e4a"),
            WorldEffect.LEGENDE_SOMBRE: ("Légende Sombre",        "#c96a6a"),
            WorldEffect.PROTECTEUR:     ("Protecteur des Faibles", "#8fbf6a"),
            WorldEffect.INCOMPRIS:      ("Monstre Incompris",      "#c97a4a"),
            WorldEffect.REDEMPTION:     ("Âme Rédemptée",          "#c9a84c"),
            WorldEffect.EQUILIBRE:      ("Force Équilibrée",       "#8a9a7a"),
        }
        world_label, world_color = world_labels.get(world_effect, ("Inconnu", "#6a5e4a"))

        return {
            "total":         total,
            "unlocked":      done,
            "ratio":         ratio,
            "terror":        terror,
            "empathy":       empathy,
            "total_terror":  terror,
            "total_empathy": empathy,
            "percent":       int(ratio * 100),
            "title":         title,
            "world_effect":  world_effect.value,
            "world_label":   world_label,
            "world_color":   world_color,
            "blocked":       blocked,
        }
