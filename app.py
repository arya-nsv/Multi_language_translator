# ---------------------------------------------------------------
# app.py — Streamlit Multilingual Translator
# ---------------------------------------------------------------

import streamlit as st
import torch
import json
from transformers import pipeline

# ---------------------------------------------------------------
# Streamlit page configuration (title + layout)
# ---------------------------------------------------------------
st.set_page_config(page_title="Multilingual Translator", layout="centered")

# ---------------------------------------------------------------
# Select device for running ML model
# device = 0 → GPU available
# device = -1 → CPU only
# ---------------------------------------------------------------
device = 0 if torch.cuda.is_available() else -1

# ---------------------------------------------------------------
# NLLB model name (Meta AI's multilingual translation model)
# This model supports 200 languages using FLORES codes.
# ---------------------------------------------------------------
MODEL_NAME = "facebook/nllb-200-distilled-600M"

# ---------------------------------------------------------------
# Streamlit UI Heading and description
# ---------------------------------------------------------------
st.title("Multilingual Translator")
st.write("Translate English text to many languages using FLORES codes (model: facebook/nllb-200-distilled-600M).")

# ---------------------------------------------------------------
# Function to load FLORES language codes from language.json
# @st.cache_data → Caches file loading to avoid re-reading repeatedly
# Returns a dictionary: { "Language Name" : "flores_code" }
# ---------------------------------------------------------------
@st.cache_data
def load_languages(path="language.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert JSON structure → {Language: FLORES-200 code}
    lang_map = {entry["Language"]: entry["FLORES-200 code"] for entry in data}
    return lang_map

# Load language map into memory
language_map = load_languages()

# ---------------------------------------------------------------
# Streamlit UI Elements
# ---------------------------------------------------------------

# User text input
input_text = st.text_area("Input text (English)", height=150)

# Dropdown list of destination languages
dest_language = st.selectbox("Destination language", sorted(language_map.keys()))

# Two buttons side-by-side (Translate + Smaller model option)
col1, col2 = st.columns([1, 1])
with col1:
    do_translate = st.button("Translate")

with col2:
    # User can choose a smaller model for speed (CPU friendly)
    use_small_model = st.checkbox("Use smaller CPU-friendly model (if available)", value=False)

# ---------------------------------------------------------------
# Create translation pipeline (cached so it loads only once)
# @st.cache_resource → caching model is important (it is large)
# If user selects smaller model, we switch to another HuggingFace model.
# ---------------------------------------------------------------
@st.cache_resource
def create_pipeline(model_name, device, use_small=False):
    try:
        # If user selects smaller model option
        if use_small:
            small = "Helsinki-NLP/opus-mt-en-ROMANCE"  # Lightweight model
            return pipeline("translation", model=small, device=device)

        # Otherwise, load official Facebook NLLB model
        return pipeline("translation", model=model_name, device=device)

    except Exception as e:
        # Return error string instead of crashing
        return f"PIPELINE_ERROR: {e}"

# Load translation pipeline (or error message)
pipeline_or_err = create_pipeline(MODEL_NAME, device, use_small_model)

# ---------------------------------------------------------------
# Function: translate_text
# Runs the translation using FLORES codes
# ---------------------------------------------------------------
def translate_text(text, dest_code):

    # Check for empty text
    if not text or text.strip() == "":
        return "Please enter text to translate."

    # Check if pipeline failed
    if isinstance(pipeline_or_err, str) and pipeline_or_err.startswith("PIPELINE_ERROR"):
        return f"Pipeline creation failed: {pipeline_or_err}"

    try:
        # Run translation using FLORES source/target codes
        out = pipeline_or_err(
            text,
            src_lang="eng_Latn",   # FLORES code for English
            tgt_lang=dest_code     # User-selected language code
        )

        # HuggingFace pipeline returns: [{"translation_text": "..."}]
        return out[0].get("translation_text", str(out))

    except Exception as e:
        return f"Error during translation: {e}"

# ---------------------------------------------------------------
# Execute translation when user clicks Translate button
# ---------------------------------------------------------------
if do_translate:
    with st.spinner("Translating..."):   # Spinner animation
        code = language_map.get(dest_language)

        # If language code missing (should not happen)
        if code is None:
            st.error("Destination language code not found.")
        else:
            # Perform translation
            result = translate_text(input_text, code)

            # Display translated output
            st.subheader("Translated text")
            st.text_area("Result", value=result, height=150)
