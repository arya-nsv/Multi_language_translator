# app.py
import torch
import gradio as gr
import json
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Choose device: 0 for GPU (if available), -1 for CPU
device = 0 if torch.cuda.is_available() else -1

# Use the HF model name (will be downloaded if not present)
HF_MODEL = "facebook/nllb-200-distilled-600M"

# create the pipeline without forcing bfloat16 (avoid CPU-only bfloat16 error)
try:
    text_translator = pipeline(
        "translation",
        model=HF_MODEL,
        device=device,
        # do not force torch_dtype unless you know the environment supports it
    )
except Exception as e:
    # Fallback to a user-friendly pipeline creation error (so UI doesn't crash silently)
    text_translator = None
    creation_error = str(e)

# Load the JSON data from the file
with open('language.json', 'r', encoding='utf-8') as file:
    language_data = json.load(file)

# prepare dropdown mapping (Language name -> FLORES code)
language_map = {entry['Language']: entry['FLORES-200 code'] for entry in language_data}

def get_FLORES_code_from_language(language):
    return language_map.get(language)

def translate_text(text, destination_language):
    if text is None or text.strip() == "":
        return "Please enter some input text."

    if text_translator is None:
        return f"Translation pipeline unavailable. Error creating pipeline: {creation_error}"

    dest_code = get_FLORES_code_from_language(destination_language)
    if dest_code is None:
        return f"Destination language code not found for '{destination_language}'."

    try:
        # Some translation pipelines expect src_lang/tgt_lang kwargs
        result = text_translator(text, src_lang="eng_Latn", tgt_lang=dest_code)
        # pipeline returns a list of dicts
        return result[0].get("translation_text", str(result))
    except Exception as e:
        return f"Error during translation: {e}"

gr.close_all()

demo = gr.Interface(
    fn=translate_text,
    inputs=[
        gr.Textbox(label="Input text to translate", lines=6),
        gr.Dropdown(sorted(list(language_map.keys())), label="Select Destination Language")
    ],
    outputs=[gr.Textbox(label="Translated text", lines=4)],
    title="@GenAILearniverse Project 4: Multi language translator",
    description="Translate English text to many languages (FLORES codes)."
)

if __name__ == "__main__":
    demo.launch()
