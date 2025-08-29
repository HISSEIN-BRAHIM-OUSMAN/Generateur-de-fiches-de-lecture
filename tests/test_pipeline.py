from core.pipeline import summarize_sections, synthesize_fiche

def mock_chat_json(system, user):
    if '"bullets"' in user:
        return {"bullets":["pt1","pt2"], "quotes":[{"quote":"q","location":"p.1"}]}
    return {
        "thesis":"thèse",
        "key_ideas":["i1","i2","i3","i4","i5"],
        "highlights":[{"quote":"q","location":"p.1"}],
        "short_summary":"court",
        "detailed_summary":"long",
        "key_concepts":["c1","c2"],
        "keywords":["k1","k2"],
        "discussion_questions":["d1","d2","d3"],
        "difficulty":3,
        "audience":"étudiants"
    }

def test_pipeline_end_to_end():
    chunks = ["abc", "def"]
    sect = summarize_sections(chunks, mock_chat_json)
    fiche = synthesize_fiche({"title":"T","author":"A","source":"S","date":"D"}, sect, mock_chat_json)
    assert len(sect) == 2
    assert fiche.title == "T"
    assert len(fiche.key_ideas) >= 5
