from core.shemas import FicheLecture, Citation

def test_fiche_model():
    f = FicheLecture(
        title="Test",
        thesis="Thèse",
        key_ideas=["A","B"],
        short_summary="court",
        detailed_summary="long",
        key_concepts=["x","y"],
        keywords=["k1","k2"],
        discussion_questions=["q1","q2"],
        difficulty=3,
        highlights=[Citation(quote="...", location="p.12")]
    )
    assert f.title == "Test"
    assert 1 <= f.difficulty <= 5
