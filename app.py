import os, io, json, streamlit as st
from dotenv import load_dotenv
from core.extractors import from_url, from_pdf_bytes, from_text
from core.chunking import split_text
from core.pipeline import summarize_sections, synthesize_fiche
from core.llm_openai import chat_json as openai_chat_json
from core.llm_hf import hf_chat_json
from exports.markdown import fiche_to_markdown

load_dotenv()

st.set_page_config(page_title="Générateur de fiches de lecture", layout="wide")
st.title("📚 Générateur de fiches de lecture")

# Choix du fournisseur
provider = st.sidebar.selectbox("Fournisseur LLM", ["openai", "hf"],
                                index=0 if os.getenv("DEFAULT_PROVIDER","openai")=="openai" else 1)
if provider == "openai":
    model = st.sidebar.text_input("Modèle OpenAI", os.getenv("DEFAULT_OPENAI_MODEL","gpt-4o-mini"))
    chat_fn = lambda sys,u: openai_chat_json(sys,u,model=model)
else:
    model = st.sidebar.text_input("Modèle HF", os.getenv("DEFAULT_HF_MODEL","meta-llama/Meta-Llama-3-8B-Instruct"))
    chat_fn = lambda sys,u: hf_chat_json(sys,u,model=model)

target_chars = st.sidebar.slider("Taille des morceaux (caractères)", 1000, 5000, 2000, 500)
overlap = st.sidebar.slider("Chevauchement", 0, 400, 150, 50)

tab_url, tab_pdf, tab_txt = st.tabs(["🌐 URL", "📄 PDF", "📝 Texte"])

extracted = None
with tab_url:
    url = st.text_input("Collez l’URL de l’article")
    if st.button("Extraire depuis l’URL", use_container_width=True) and url:
        with st.spinner("Extraction..."):
            extracted = from_url(url)

with tab_pdf:
    file = st.file_uploader("Déposez un PDF (chapitre/ouvrage)", type=["pdf"])
    if file and st.button("Extraire depuis le PDF", use_container_width=True):
        with st.spinner("Lecture du PDF..."):
            extracted = from_pdf_bytes(file.read(), source_name=file.name)

with tab_txt:
    raw = st.text_area("Collez du texte brut", height=250)
    title_txt = st.text_input("Titre (optionnel)", value="Texte collé")
    if st.button("Utiliser ce texte", use_container_width=True) and raw:
        extracted = from_text(raw, title=title_txt)

if extracted:
    st.success(f"Contenu chargé — {len(extracted.text)} caractères")
    meta_cols = st.columns(4)
    with meta_cols[0]: extracted.title   = st.text_input("Titre", value=extracted.title or "")
    with meta_cols[1]: extracted.author  = st.text_input("Auteur", value=extracted.author or "")
    with meta_cols[2]: extracted.source  = st.text_input("Source", value=extracted.source or "")
    with meta_cols[3]: extracted.date    = st.text_input("Date", value=extracted.date or "")

    if st.button("Générer la fiche de lecture ✨", type="primary", use_container_width=True):
        with st.spinner("Résumé en cours..."):
            chunks = split_text(extracted.text, target_chars, overlap)
            sect = summarize_sections(chunks, chat_fn)
            fiche = synthesize_fiche({
                "title": extracted.title,
                "author": extracted.author,
                "source": extracted.source,
                "date": extracted.date
            }, sect, chat_fn)

        st.subheader("Fiche générée")
        md = fiche_to_markdown(fiche)
        st.markdown(md)

        st.download_button("⬇️ Télécharger (Markdown)", data=md.encode("utf-8"),
                           file_name=f"{(fiche.title or 'fiche').replace(' ','_')}.md",
                           mime="text/markdown")

        st.download_button("⬇️ Données (JSON)", data=json.dumps(fiche.model_dump(), ensure_ascii=False, indent=2).encode("utf-8"),
                           file_name=f"{(fiche.title or 'fiche').replace(' ','_')}.json",
                           mime="application/json")
