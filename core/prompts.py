SYSTEM_FICHE = """Tu es un expert en lecture active et en synthèse.
Tu produis des fiches de lecture structurées, concises, neutres, en français.
Si le texte est long, tu relies et résumes sans halluciner; cite "inconnu" si l'info manque.
"""

TEMPLATE_SECTION_SUMMARY = """Résume la section ci-dessous en 5 à 8 puces denses et 3 citations courtes s'il y en a.
Texte:
{chunk}
Réponds en JSON:
{{
 "bullets": ["..."],
 "quotes": [{{"quote":"...","location":"..."}}]
}}
"""

TEMPLATE_SYNTHESIS = """À partir des résumés de sections (JSON), produis la fiche complète:
- Thèse (2–3 phrases)
- 5–8 idées clés (sans redondance)
- 2–4 citations marquantes avec emplacement si fourni
- Résumé court ~150 mots
- Résumé détaillé 400–600 mots
- Concepts clés (5–10)
- Mots-clés (5–10)
- 3–5 questions de discussion
- Difficulté (1–5) et audience recommandée

Données de base:
Titre: "{title}"
Auteur: "{author}"
Source: "{source}"
Date: "{date}"

Sections (JSON):
{section_json}

Réponds UNIQUEMENT en JSON conforme au schéma:
{{
 "thesis": "...",
 "key_ideas": ["..."],
 "highlights": [{{"quote":"...","location":"..."}}],
 "short_summary": "...",
 "detailed_summary": "...",
 "key_concepts": ["..."],
 "keywords": ["..."],
 "discussion_questions": ["..."],
 "difficulty": 3,
 "audience": "..."
}}
"""
