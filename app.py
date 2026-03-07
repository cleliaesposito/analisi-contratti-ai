import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- CONFIGURAZIONE CHIAVE API ---
# Prendi la chiave dalla tua Foto 2 e incollala qui tra le virgolette
API_KEY = "AIzaSyAMb8tZrMuEWxBxNVX_GX_0sjMaIaHq30s" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Guardiano Contratti", page_icon="🛡️")

st.title("🛡️ Guardiano del Contratto Globale AI")
st.write("Analisi professionale dei rischi contrattuali in pochi secondi.")

uploaded_file = st.file_uploader("Carica il tuo contratto (PDF)", type="pdf")

if uploaded_file:
    # Lettura del PDF
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    if st.button("🚀 AVVIA ANALISI"):
        with st.spinner('L\'intelligenza artificiale sta analizzando...'):
            prompt = f"Analizza questo contratto in italiano. Trova i 3 rischi principali e dai un voto di equità da 1 a 10. Testo: {text[:10000]}"
            try:
                response = model.generate_content(prompt)
                st.markdown("### Risultato dell'analisi:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Errore: {e}")
