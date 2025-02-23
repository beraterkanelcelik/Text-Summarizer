# app.py

import streamlit as st
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

@st.cache_resource
def load_model():
    # Replace with your actual model repository ID on Hugging Face Hub
    model_repo = "beraterkanelcelik/my-t5-summarizer-model"
    model = T5ForConditionalGeneration.from_pretrained(model_repo)
    tokenizer = T5Tokenizer.from_pretrained(model_repo)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    return model, tokenizer, device

model, tokenizer, device = load_model()

st.title("Text Summarization with Fine-Tuned T5")
st.markdown("Enter the text below and click **Summarize** to generate a summary:")

input_text = st.text_area("Input Text", height=200)

if st.button("Summarize"):
    if input_text:
        # Prepend the task prefix and encode the input text
        input_ids = tokenizer.encode(
            "summarize: " + input_text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(device)
        # Generate the summary using beam search
        summary_ids = model.generate(input_ids, max_length=150, num_beams=2, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        st.subheader("Summary")
        st.write(summary)
    else:
        st.error("Please enter some text to summarize.")
