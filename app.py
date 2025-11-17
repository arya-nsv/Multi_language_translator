# app.py (Streamlit)
import streamlit as st
import torch
import json
from transformers import pipeline

st.set_page_config(page_title="Multilingual Translator", layout="centered")

# decide device: use GPU if available, otherwise CPU
device = 0 if torch.cuda.is_available() else -1

MODEL_NAME = "facebook/nllb-200-distilled-600M"

st.title("Multilingual Translator")
st.write("Translate English text to many languages using FLORES codes (model: facebook/nllb-200-distilled-600M).")

# load languages file
@st.cache_data
def load_languages(path="language.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # map display name -> FLORES code
    lang_map = {entry["Language"]: entry["FLORES-200 code"] for entry in data}
    return lang_map

language_map = load_languages()

# Build UI
input_text = st.text_area("Input text (English)", height=150)
dest_language = st.selectbox("Destination language", sorted(language_map.keys()))

col1, col2 = st.columns([1, 1])
with col1:
    do_translate = st.button("Translate")
with col2:
    use_small_model = st.checkbox("Use smaller CPU-friendly model (if available)", value=False)

# Create pipeline (cached) — avoid bfloat16 and let device be chosen
@st.cache_resource
def create_pipeline(model_name, device, use_small=False):
    try:
        # if user wants a smaller CPU-friendly model, change model_name accordingly here
        if use_small:
            # example smaller multilingual model (modify if you prefer another)
            small = "Helsinki-NLP/opus-mt-en-ROMANCE"
            return pipeline("translation", model=small, device=device)
        else:
            return pipeline("translation", model=model_name, device=device)
    except Exception as e:
        return f"PIPELINE_ERROR: {e}"

pipeline_or_err = create_pipeline(MODEL_NAME, device, use_small_model)

def translate_text(text, dest_code):
    if not text or text.strip() == "":
        return "Please enter text to translate."

    if isinstance(pipeline_or_err, str) and pipeline_or_err.startswith("PIPELINE_ERROR"):
        return f"Pipeline creation failed: {pipeline_or_err}"

    try:
        # some pipelines accept src_lang/tgt_lang — adjust if the model expects different kwargs
        out = pipeline_or_err(text, src_lang="eng_Latn", tgt_lang=dest_code)
        # pipeline returns list of dicts
        return out[0].get("translation_text", str(out))
    except Exception as e:
        return f"Error during translation: {e}"

if do_translate:
    with st.spinner("Translating..."):
        code = language_map.get(dest_language)
        if code is None:
            st.error("Destination language code not found.")
        else:
            result = translate_text(input_text, code)
            st.subheader("Translated text")
            st.text_area("Result", value=result, height=150)
