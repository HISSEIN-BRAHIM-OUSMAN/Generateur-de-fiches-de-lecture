import json
from typing import List
# from core import FicheLecture, Citation
from .prompts import SYSTEM_FICHE, TEMPLATE_SECTION_SUMMARY, TEMPLATE_SYNTHESIS
from .shemas import FicheLecture, Citation


def summarize_sections(chunks: List[str], chat_json_fn):
    section_summaries = []
    for i, ch in enumerate(chunks, start=1):
        user = TEMPLATE_SECTION_SUMMARY.format(chunk=ch[:12000])
        j = chat_json_fn(SYSTEM_FICHE, user)
        section_summaries.append({"index": i,
                                  "bullets": j.get("bullets", []),
                                  "quotes": j.get("quotes", [])})
    return section_summaries

def synthesize_fiche(meta, section_summaries, chat_json_fn) -> FicheLecture:
    user = TEMPLATE_SYNTHESIS.format(
        title=meta.get("title") or "Inconnu",
        author=meta.get("author") or "Inconnu",
        source=meta.get("source") or "Inconnu",
        date=meta.get("date") or "Inconnue",
        section_json=json.dumps(section_summaries, ensure_ascii=False)
    )
    j = chat_json_fn(SYSTEM_FICHE, user)
    # Validation pydantic
    return FicheLecture(
        title=meta.get("title") or "Inconnu",
        author=meta.get("author"),
        source=meta.get("source"),
        date=meta.get("date"),
        thesis=j["thesis"],
        key_ideas=j["key_ideas"],
        short_summary=j["short_summary"],
        detailed_summary=j["detailed_summary"],
        key_concepts=j["key_concepts"],
        keywords=j["keywords"],
        discussion_questions=j["discussion_questions"],
        difficulty=int(j.get("difficulty", 3)),
        audience=j.get("audience"),
        highlights=[Citation(**c) for c in j.get("highlights", [])]
    )
