# Silent Reins : Arbre du Lien

**Système de progression narratif** pour un jeu vidéo personnel où un cavalier sans tête reconstruit son lien avec son cheval d'enfance pour briser une malédiction.


---

## 🎮 Concept

Cette Web APP sert d'un concept de simulation d'un des mécanismes du jeu Silent Reins que je développe. Le destrier noir n'est pas une simple monture. C'est l'ancre émotionnelle du protagoniste. Puisque le chevalier ne peut s'exprimer, c'est le cheval qui interagit avec le monde ettraduit les intentions de son maître à travers
comportements et sons que les autres comprennent. La progression de ce lien est cruciale, car elle débloque de
nouvelles options d'interaction et influe directement sur ledénouement du jeu

Chaque talent débloqué influence la balance **Terreur / Empathie**, changeant la façon dont le monde perçoit le Cavalier Sans Tête.

---

## 🏗️ Architecture

```
arbre_du_lien/
├── app.py                  # Streamlit main — UI + state management
├── requirements.txt
├── README.md
├── images/                 # Slot pour les visuels des talents
└── src/
    ├── __init__.py
    ├── skill_graph.py      # DAG model + graph algorithms
    ├── skill_data.py       # Game data + layout computation
    └── renderer.py         # HTML/Canvas code generation
```

### Compétences techniques démontrées

| Domaine | Implémentation |
|---------|---------------|
| **Structures de données** | Graphe orienté acyclique (DAG) avec listes d'adjacence |
| **Algorithmes de graphe** | Tri topologique (Kahn), BFS, analyse d'accessibilité |
| **POO** | Dataclasses, enums, encapsulation, pattern Builder/Factory |
| **Design patterns** | State Machine (LOCKED→AVAILABLE→UNLOCKED), MVC |
| **Sérialisation** | JSON bidirectionnel Python ↔ JavaScript |
| **Frontend** | Canvas 2D, animation loop, hit detection, HiDPI |
| **UI/UX** | Tooltips, particles, glow effects, responsive design |
| **Architecture** | Séparation données/logique/rendu, code modulaire |

---




## 📊 Algorithmes implémentés

### Tri topologique (Kahn)
Calcule un ordre valide de déblocage respectant toutes les dépendances. Vérifie l'absence de cycles dans le graphe.

### BFS, Accessibilité
Depuis un nœud donné, détermine tous les talents accessibles en aval. Utilisé pour calculer l'impact stratégique d'un choix.

### BFS inversé, Plus court chemin
Remonte les dépendances depuis un objectif pour trouver la séquence minimale de déblocages nécessaires.

### Analyse de sous-arbre
Agrège les deltas Terreur/Empathie de tout un sous-arbre pour aider le joueur à planifier sa progression.

---

## 🎨 Design

L'interface s'inspire des arbres de talents de jeux comme **Heroes of the Storm** et **World of Warcraft** :
- Nœuds circulaires avec bordures dorées
- Connexions en courbes de Bézier
- Effets de lueur (glow) selon le statut
- Particules ambiantes
- Thème médiéval-fantastique sombre
Le positionnement spatial des nœuds dessine la forme globale d'une Citrouille (Objet Majeur du lore), mais le graphe est algorithmiquement impossible à compléter dans son intégralité, grâce au système complexe de conflits.

---


---

*Silent Reins - Jeu en cours de développement - 2026*
