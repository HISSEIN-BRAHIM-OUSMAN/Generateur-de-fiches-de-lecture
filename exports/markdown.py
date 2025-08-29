from core.pipeline import FicheLecture

def fiche_to_markdown(f: FicheLecture) -> str:
    quotes = "\n".join([f'- “{c.quote}” ({c.location or "n/a"})'
                        for c in f.highlights])
    bullets = "\n".join([f"- {b}" for b in f.key_ideas])
    concepts = ", ".join(f.key_concepts)
    keywords = ", ".join(f.keywords)
    questions = "\n".join([f"- {q}" for q in f.discussion_questions])

    return f"""# {f.title}
**Auteur·e :** {f.author or "—"} — **Source :** {f.source or "—"} — **Date :** {f.date or "—"}

## Thèse
{f.thesis}

## Idées clés
{bullets}

## Citations
{quotes or "—"}

## Résumé (court)
{f.short_summary}

## Résumé (détaillé)
{f.detailed_summary}

## Concepts clés
{concepts}

## Mots-clés
{keywords}

## Questions de discussion
{questions}

**Difficulté :** {f.difficulty}/5 — **Public cible :** {f.audience or "—"}
"""
