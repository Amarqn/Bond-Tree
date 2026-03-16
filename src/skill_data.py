# skill_data.py — Définition de tous les talents et construction du graphe

from src.skill_graph import SkillGraph, SkillNode, Branch, ActivityCondition, WorldEffect

def cond(cid: str, label: str, desc: str) -> ActivityCondition:
    return ActivityCondition(id=cid, label=label, description=desc)

def build_skill_tree() -> SkillGraph:
    graph = SkillGraph()

    graph.add_node(SkillNode(
        id="approche_calme",
        name="Approche Calme",
        icon="🌙",
        description="Le cheval ne fuit plus à votre approche. Il reconnaît votre silhouette dans la brume nocturne.",
        narrative_effect="Les villageois murmurent qu'une ombre hante les écuries… mais aucun cheval n'a été blessé.",
        branch=Branch.CONFIANCE, tier=1,
        terror_delta=0, empathy_delta=5,
        requires=[],
        world_change_text="Un palefrenier laisse désormais la porte de l'écurie entrouverte le soir.",
        conditions=[
            cond("ac_nuits", "3 nuits consécutives près du cheval",
                 "Passer du temps près de lui sans le toucher, trois nuits d'affilée. Rester immobile, laisser la peur s'éteindre d'elle-même."),
        ],
    ))

    graph.add_node(SkillNode(
        id="premier_contact",
        name="Premier Contact",
        icon="✋",
        description="Vous posez la main sur son encolure. Il ne bronche pas. Un souvenir d'enfance remonte à la surface.",
        narrative_effect="Le cheval hennit doucement. Pour la première fois depuis la malédiction, vous ressentez de la chaleur.",
        branch=Branch.CONFIANCE, tier=2,
        terror_delta=0, empathy_delta=5,
        requires=["approche_calme"],
        world_change_text="Un enfant du village prétend avoir vu le Cavalier caresser son cheval au clair de lune.",
        conditions=[
            cond("pc_pommes", "Trouver des pommes sauvages en forêt",
                 "Les cueillir soi-même, sans acheter ni voler. Le geste compte autant que le fruit."),
            cond("pc_offrir", "Les offrir au cheval à l'aube",
                 "Au lever du soleil, tendre les pommes à plat dans la main. Ne pas forcer le contact."),
        ],
    ))

    graph.add_node(SkillNode(
        id="toilettage",
        name="Toilettage",
        icon="✨",
        description="Brosser sa crinière, nettoyer ses sabots. Les gestes simples reconstruisent ce qui a été brisé.",
        narrative_effect="Le pelage du cheval retrouve son éclat. Même la mort ne peut ternir ce lien.",
        branch=Branch.CONFIANCE, tier=3,
        terror_delta=0, empathy_delta=10,
        requires=["premier_contact"],
        world_change_text="Le forgeron du village forgera une brosse en cadeau si on lui rapporte du minerai rare.",
        conditions=[
            cond("toi_brosse", "Obtenir une brosse (échange ou commerce honnête)",
                 "Ni vol, ni intimidation. Une transaction juste — le cheval le sentirait."),
            cond("toi_seance", "Consacrer une heure entière au toilettage",
                 "Sans interruption. Sans surveillance. Juste vous deux."),
        ],
    ))

    graph.add_node(SkillNode(
        id="repos_partage",
        name="Repos Partagé",
        icon="💤",
        description="Dormir dos contre son flanc. Vos cauchemars sont moins violents quand il est là.",
        narrative_effect="Vous rêvez de prairies dorées et d'un garçon qui court pieds nus aux côtés d'un poulain.",
        branch=Branch.CONFIANCE, tier=4,
        terror_delta=0, empathy_delta=15,
        requires=["toilettage"],
        world_change_text="On dit qu'après cette nuit-là, les corbeaux ont cessé de tourner au-dessus du Cavalier.",
        conditions=[
            cond("rp_danger", "Fuir ensemble un danger mortel",
                 "Survivre à une embuscade, une tempête, ou une créature de la nuit — ensemble."),
            cond("rp_dormir", "Se reposer côte à côte dans un lieu sûr",
                 "Choisir un abri, s'y allonger, faire confiance au cheval pour monter la garde."),
        ],
    ))

    graph.add_node(SkillNode(
        id="langage_corporel",
        name="Langage Corporel",
        icon="🫀",
        description="Le cheval lit vos gestes. Un pas en arrière : danger. Deux tapes sur la selle : allons-y.",
        narrative_effect="Un enfant jure avoir vu le cheval hocher la tête comme s'il répondait à quelqu'un.",
        branch=Branch.COMMUNICATION, tier=2,
        terror_delta=-5, empathy_delta=10,
        requires=["premier_contact"],
        world_change_text="Les habitants d'un village vous laissent désormais traverser sans barrer les portes.",
        conditions=[
            cond("lc_village", "Traverser un village sans provoquer de panique",
                 "Pas de course, pas de cri, pas de torche brandissante. Simplement passer, comme une ombre tranquille."),
        ],
    ))

    graph.add_node(SkillNode(
        id="traducteur_equin",
        name="Traducteur Équin",
        icon="🗣️",
        description="Le cheval hennit, gratte le sol, pousse du museau. Les PNJ comprennent ses intentions basiques.",
        narrative_effect="Le marchand raconte à la taverne qu'un cheval spectral lui a sauvé la mise. On le prend pour un ivrogne.",
        branch=Branch.COMMUNICATION, tier=3,
        terror_delta=-5, empathy_delta=15,
        requires=["langage_corporel"],
        world_change_text="Un marchand itinérant laisse désormais des carottes à votre intention aux carrefours.",
        conditions=[
            cond("te_marchand", "Aider un marchand en détresse",
                 "Trouver quelqu'un dans le besoin. Laisser le cheval communiquer à votre place. Ne pas intervenir directement."),
            cond("te_compris", "Être compris sans un mot",
                 "La transaction ou l'aide doit aboutir sans que vous produisiez aucun son ni geste lisible."),
        ],
    ))

    graph.add_node(SkillNode(
        id="chant_silencieux",
        name="Chant Silencieux",
        icon="🎵",
        description="Vous n'avez pas de voix, mais le vent qui traverse votre armure produit une mélodie mélancolique.",
        narrative_effect="Un berger croit entendre un fantôme chanter. Il laisse du pain et du vin à votre intention.",
        branch=Branch.COMMUNICATION, tier=3,
        terror_delta=5, empathy_delta=10,
        requires=["langage_corporel"],
        blocks=["traducteur_equin"],
        world_change_text="Les nuits sans lune, on entend parfois une mélodie venir des collines. Les loups se taisent.",
        conditions=[
            cond("cs_falaise", "Rester immobile au sommet d'une falaise venteuse",
                 "Attendre le coucher du soleil complet. Ne pas bouger. Laisser le vent jouer dans les jointures de l'armure."),
        ],
    ))

    graph.add_node(SkillNode(
        id="lien_empathique",
        name="Lien Empathique",
        icon="🔮",
        description="Vous ressentez ce que le cheval ressent. Sa peur. Sa joie. Sa douleur. Et lui ressent les vôtres.",
        narrative_effect="Quand le cavalier souffre, le cheval gémit. Quand le cheval est heureux, l'armure semble briller.",
        branch=Branch.COMMUNICATION, tier=4,
        terror_delta=0, empathy_delta=20,
        requires=["traducteur_equin", "repos_partage"],
        world_change_text="Les guérisseurs du coin prétendent que votre cheval peut diagnostiquer les maladies de l'âme.",
        conditions=[
            cond("le_blessure", "Soigner le cheval après une blessure grave",
                 "Trouver des herbes médicinales, prendre soin de lui toute une nuit. Ne pas quitter son chevet."),
            cond("le_attente", "Attendre sa guérison complète avant de repartir",
                 "Résister à l'urgence. Rester. Même si la quête attend."),
        ],
        min_empathy=25,
    ))

    graph.add_node(SkillNode(
        id="galop_nocturne",
        name="Galop Nocturne",
        icon="🌑",
        description="Le cheval court sans peur dans les ténèbres. La nuit est votre domaine.",
        narrative_effect="Les voyageurs parlent d'une ombre fulgurante sur les routes de nuit. Certains y voient un présage.",
        branch=Branch.TRAVERSEE, tier=2,
        terror_delta=10, empathy_delta=5,
        requires=["approche_calme"],
        world_change_text="Les bandits de grand chemin évitent désormais les routes après minuit.",
        conditions=[
            cond("gn_lune", "Chevaucher sous la pleine lune",
                 "Attendre la pleine lune. Partir à minuit. Ne pas s'arrêter avant l'aube."),
        ],
    ))

    graph.add_node(SkillNode(
        id="sentier_oublie",
        name="Sentier Oublié",
        icon="🗺️",
        description="Le cheval retrouve des chemins que les vivants ont oubliés depuis des siècles.",
        narrative_effect="Le sentier mène à un sanctuaire en ruines. Des inscriptions parlent d'un pacte entre homme et bête.",
        branch=Branch.TRAVERSEE, tier=3,
        terror_delta=0, empathy_delta=10,
        requires=["galop_nocturne", "toilettage"],
        world_change_text="Un cartographe royal paie une fortune pour des copies de vos itinéraires.",
        conditions=[
            cond("so_confiance", "Laisser le cheval guider sans jamais intervenir",
                 "Une nuit entière. Les mains lâchées. Nulle part où aller — laisser le cheval choisir."),
        ],
    ))

    graph.add_node(SkillNode(
        id="saut_abime",
        name="Saut de l'Abîme",
        icon="🦅",
        description="Franchir des gouffres que nul mortel n'oserait tenter. La confiance absolue en action.",
        narrative_effect="Le vent hurle dans le vide où devrait être votre tête. Mais le cheval n'a jamais douté.",
        branch=Branch.TRAVERSEE, tier=4,
        terror_delta=5, empathy_delta=10,
        requires=["sentier_oublie"],
        world_change_text="Des zones autrefois inaccessibles s'ouvrent. Des secrets enfouis refont surface.",
        conditions=[
            cond("sa_pont", "Trouver un pont ou passage effondré",
                 "Explorer les vieilles routes jusqu'à trouver une coupure dans le monde."),
            cond("sa_saut", "Le franchir d'un seul bond sans hésiter",
                 "Pas de recul. Pas de calcul. Un élan — et le vide."),
        ],
        min_empathy=20,
    ))

    graph.add_node(SkillNode(
        id="charge_spectrale",
        name="Charge Spectrale",
        icon="💀",
        description="Ensemble, vous devenez une force imparable. Les barricades cèdent, les ennemis fuient.",
        narrative_effect="Cette nuit-là, le Cavalier Sans Tête n'était pas le monstre. Il était le rempart entre vivants et morts.",
        branch=Branch.TRAVERSEE, tier=5,
        terror_delta=15, empathy_delta=15,
        requires=["saut_abime", "lien_empathique"],
        world_change_text="Des villages en périphérie placent désormais une effigie du Cavalier à leurs portes. Gardien ou avertissement.",
        conditions=[
            cond("cs_attaque", "Défendre un village contre une attaque",
                 "Rester pour protéger. Ne pas fuir. Même si la survie serait plus simple."),
            cond("cs_victoire", "Survivre et voir les habitants sains et saufs",
                 "Ce n'est pas la bataille qui compte. C'est ce qu'il en reste."),
        ],
        min_terror=20,
    ))

    graph.add_node(SkillNode(
        id="fragment_enfance",
        name="Fragment d'Enfance",
        icon="🧒",
        description="Un flash : un garçon qui court dans un champ doré. Le poulain galope à ses côtés, libre.",
        narrative_effect="Le cheval s'arrête net devant un chêne centenaire. C'est ici que tout a commencé.",
        branch=Branch.MEMOIRE, tier=3,
        terror_delta=0, empathy_delta=10,
        requires=["repos_partage"],
        world_change_text="Un vieux berger vous reconnaît. Il pleure en silence et s'en va sans parler.",
        conditions=[
            cond("fe_champ", "Retrouver le champ d'enfance (exploration libre)",
                 "Laisser le cheval vous y emmener. Ne pas chercher — se souvenir."),
        ],
    ))

    graph.add_node(SkillNode(
        id="nom_oublie",
        name="Le Nom Oublié",
        icon="📛",
        description="Comment s'appelait le cheval ? Comment vous appeliez-vous ? Les noms ont un pouvoir ancien.",
        narrative_effect="Les pages sont jaunies mais l'écriture est la vôtre. Vous aviez une vie. Vous aviez un nom.",
        branch=Branch.MEMOIRE, tier=4,
        terror_delta=0, empathy_delta=20,
        requires=["fragment_enfance", "lien_empathique"],
        world_change_text="Prononcer votre ancien nom fait tressaillir les animaux dans un rayon de cent pas.",
        conditions=[
            cond("no_ruines", "Trouver les ruines de votre ancien foyer",
                 "Elles existent quelque part. Chercher les fondations, les pierres noircies, les herbes folles."),
            cond("no_journal", "Récupérer un objet personnel (journal, bijou, outil)",
                 "Un seul suffit. Quelque chose qui vous appartenait avant."),
        ],
    ))

    graph.add_node(SkillNode(
        id="voix_defunts",
        name="Voix des Défunts",
        icon="👻",
        description="Les morts vous parlent. Non pas parce que vous êtes mort, mais parce que vous êtes entre les deux mondes.",
        narrative_effect="Une voix murmure votre vrai nom. Vous l'avez oublié, mais pas les morts.",
        branch=Branch.MEMOIRE, tier=4,
        terror_delta=10, empathy_delta=10,
        requires=["fragment_enfance", "chant_silencieux"],
        blocks=["renaissance"],
        world_change_text="Les nécromants de la région cherchent à vous rencontrer. Pas pour vous combattre.",
        conditions=[
            cond("vd_cimetiere", "Passer une nuit dans un cimetière ancien",
                 "Pas n'importe lequel — un cimetière qui date d'avant la malédiction."),
            cond("vd_ecoute", "Écouter le silence jusqu'à entendre quelque chose",
                 "Rester éveillé jusqu'à l'aube. Ne rien forcer. Attendre."),
        ],
        requires_world_effect=WorldEffect.LEGENDE_SOMBRE,
    ))

    graph.add_node(SkillNode(
        id="pacte_originel",
        name="Le Pacte Originel",
        icon="🩸",
        description="Vous vous souvenez. La sorcière. Le marché. Votre tête contre la vie du poulain mourant.",
        narrative_effect="La malédiction prend tout son sens. Vous n'étiez pas une victime — vous étiez prêt à tout sacrifier.",
        branch=Branch.MEMOIRE, tier=5,
        terror_delta=0, empathy_delta=30,
        requires=["nom_oublie", "voix_defunts", "charge_spectrale"],
        world_change_text="La sorcière à l'origine du pacte envoie un messager. Elle veut vous parler.",
        conditions=[
            cond("po_sanctuaire", "Atteindre le sanctuaire maudit",
                 "Trouver le lieu où le pacte a été conclu. Le cheval vous y mènera — il s'en souvient."),
            cond("po_verite", "Affronter la vérité sans fuir",
                 "Rester sur place après la révélation. Ne pas détruire le sanctuaire. Comprendre."),
        ],
    ))

    graph.add_node(SkillNode(
        id="instinct_bestial",
        name="Instinct Bestial",
        icon="🐺",
        description="Sans yeux pour voir, vous percevez le monde autrement. Le cheval est vos sens.",
        narrative_effect="Vous percevez les battements de cœur des créatures proches. Le monde vibre différemment sans tête.",
        branch=Branch.SURVIE, tier=2,
        terror_delta=10, empathy_delta=0,
        requires=["premier_contact"],
        world_change_text="Les chasseurs du coin évitent certaines zones — là où le Cavalier patrouille sans être vu.",
        conditions=[
            cond("ib_foret", "Naviguer une forêt dense les mains lâchées",
                 "Choisir la forêt la plus sombre. Lâcher les rênes. Se laisser guider entièrement."),
        ],
    ))

    graph.add_node(SkillNode(
        id="armure_vivante",
        name="Armure Vivante",
        icon="🛡️",
        description="Votre armure n'est pas que du métal. La malédiction l'a fusionnée à votre être. Elle vous protège… et vous emprisonne.",
        narrative_effect="Les bandits fuient en hurlant. Votre armure a bougé seule pour parer un coup mortel.",
        branch=Branch.SURVIE, tier=3,
        terror_delta=15, empathy_delta=0,
        requires=["instinct_bestial"],
        blocks=["flamme_interieure"],
        world_change_text="Les armuriers refusent de travailler sur votre équipement. Ils disent qu'il les regarde.",
        conditions=[
            cond("av_embuscade", "Survivre à une embuscade sans arme offensive",
                 "Se faire attaquer. Ne pas attaquer en retour. Laisser l'armure répondre."),
            cond("av_observer", "Observer l'armure se mouvoir seule",
                 "Après le combat, rester immobile et regarder. Accepter ce que vous êtes."),
        ],
        min_terror=15,
    ))

    graph.add_node(SkillNode(
        id="flamme_interieure",
        name="Flamme Intérieure",
        icon="🔥",
        description="Une lueur brûle dans votre poitrail — pas un cœur, mais quelque chose de plus ancien.",
        narrative_effect="Le feu dans votre armure réchauffe le cheval pendant les nuits glaciales. Même maudit, vous donnez de la chaleur.",
        branch=Branch.SURVIE, tier=3,
        terror_delta=5, empathy_delta=15,
        requires=["instinct_bestial", "toilettage"],
        world_change_text="On vous apporte parfois des chandeliers éteints. Vous les rallumez sans y toucher.",
        conditions=[
            cond("fi_feu", "Méditer devant un feu de camp",
                 "Allumer un feu vous-même, de vos mains (ou de ce qu'il en reste). Vous y fixer jusqu'à l'aube."),
            cond("fi_rythme", "Attendre que les flammes dansent à votre rythme",
                 "Pas un tour de passe-passe — un alignement réel. Vous le saurez quand ça arrive."),
        ],
    ))

    graph.add_node(SkillNode(
        id="renaissance",
        name="Renaissance",
        icon="🌅",
        description="La malédiction ne définit pas qui vous êtes. Vous choisissez ce que vous devenez.",
        narrative_effect="L'enfant ne crie pas. Il vous prend la main et dit merci. Le village tout entier se tait.",
        branch=Branch.SURVIE, tier=5,
        terror_delta=-10, empathy_delta=25,
        requires=["flamme_interieure", "charge_spectrale"],
        world_change_text="Pour la première fois, un village vous offre un repas. La table est dressée dehors — pour vous deux.",
        conditions=[
            cond("ren_enfant", "Trouver un enfant perdu dans la forêt maudite",
                 "L'enfant doit être vraiment perdu, en danger. Pas une rencontre arrangée."),
            cond("ren_retour", "Le ramener sain et sauf sans qu'il ait peur de vous",
                 "C'est la condition impossible. Et pourtant."),
        ],
        requires_world_effect=WorldEffect.PROTECTEUR,
    ))

    issues = graph.validate()
    if issues:
        raise ValueError("Validation de l'arbre échouée :\n" + "\n".join(issues))

    return graph


def compute_layout(graph, canvas_w: int = 1200, canvas_h: int = 800) -> dict[str, tuple[int, int]]:
    """Fixed pumpkin-shaped layout. canvas_w/h ignored — positions tuned for 1060x640."""

    fixed = {
        "approche_calme":    (500,  95),
        "premier_contact":   (415, 210),
        "toilettage":        (385, 330),
        "repos_partage":     (380, 450),
        "langage_corporel":  (535, 205),
        "traducteur_equin":  (490, 330),
        "chant_silencieux":  (580, 330),
        "lien_empathique":   (535, 440),
        "galop_nocturne":    (295, 225),
        "sentier_oublie":    (268, 345),
        "saut_abime":        (275, 460),
        "charge_spectrale":  (310, 555),
        "fragment_enfance":  (650, 320),
        "nom_oublie":        (620, 435),
        "voix_defunts":      (695, 440),
        "pacte_originel":    (530, 560),
        "instinct_bestial":  (760, 220),
        "armure_vivante":    (775, 340),
        "flamme_interieure": (755, 455),
        "renaissance":       (720, 550),
    }

    return {nid: fixed.get(nid, (canvas_w // 2, canvas_h // 2)) for nid in graph.nodes}
