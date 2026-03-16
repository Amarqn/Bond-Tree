# 🐴 Le Cavalier Sans Tête — Arbre du Lien

**Système de progression narratif** pour un jeu vidéo où un cavalier sans tête reconstruit son lien avec son cheval d'enfance pour briser une malédiction.

> Projet portfolio — Candidature Master en Informatique, 2026

---

## 🎮 Concept

L'**Arbre du Lien** remplace le système d'XP traditionnel. Au lieu de tuer des monstres pour accumuler des points, le joueur progresse en accomplissant des **activités narratives** : soigner le cheval, explorer ensemble, retrouver des souvenirs du passé.

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

## 🚀 Lancer l'application

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📊 Algorithmes implémentés

### Tri topologique (Kahn)
Calcule un ordre valide de déblocage respectant toutes les dépendances. Vérifie l'absence de cycles dans le graphe.

### BFS — Accessibilité
Depuis un nœud donné, détermine tous les talents accessibles en aval. Utilisé pour calculer l'impact stratégique d'un choix.

### BFS inversé — Plus court chemin
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

---

## 📸 Images

Chaque talent a un emplacement réservé pour un visuel. Pour ajouter des images :
1. Placer les fichiers dans `images/`
2. Nommer chaque fichier selon l'`id` du talent (ex: `approche_calme.png`)
3. Les images apparaîtront dans les nœuds de l'arbre

---

*Le Cavalier Sans Tête — Game Design Document — 2026*
