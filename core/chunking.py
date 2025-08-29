from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text: str, target_chars: int = 2000, overlap: int = 150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=target_chars,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text or "")
