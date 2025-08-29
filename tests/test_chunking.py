from core.chunking import split_text

def test_split_text_basic():
    text = "A " * 10000
    parts = split_text(text, target_chars=1000, overlap=100)
    assert len(parts) > 5
