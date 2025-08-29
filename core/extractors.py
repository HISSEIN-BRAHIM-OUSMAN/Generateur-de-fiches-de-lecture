from dataclasses import dataclass
from typing import Optional, Tuple
import re, io, requests
from pypdf import PdfReader
from readability import Document
import trafilatura

@dataclass
class ExtractedDoc:
    text: str
    title: Optional[str] = None
    author: Optional[str] = None
    source: Optional[str] = None
    date: Optional[str] = None

def from_url(url: str) -> ExtractedDoc:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    html = resp.text
    # Try readability
    doc = Document(html)
    title = doc.short_title()
    content_html = doc.summary()
    # Fallback to trafilatura if needed
    text = trafilatura.extract(html, url=url) or _strip_html(content_html)
    return ExtractedDoc(text=text or "", title=title, source=url)

def from_pdf_bytes(data: bytes, source_name: str = "document.pdf") -> ExtractedDoc:
    reader = PdfReader(io.BytesIO(data))
    pages = [p.extract_text() or "" for p in reader.pages]
    text = "\n\n".join(pages)
    return ExtractedDoc(text=text, title=source_name, source=source_name)

def from_text(text: str, title: str = "Texte collé") -> ExtractedDoc:
    return ExtractedDoc(text=text, title=title, source="clipboard")

def _strip_html(html: str) -> str:
    return re.sub("<[^<]+?>", "", html or "").strip()
