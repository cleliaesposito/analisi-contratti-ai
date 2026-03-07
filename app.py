import streamlit as st
import PyPDF2
import requests
import json

# --- NUOVA CONFIGURAZIONE ---
# Se questa chiave continua a dare 400 o 404, creane una NUOVA su AI Studio
API_KEY = "AIzaSyAMb8tZrMuEWxBxNVX_GX_0sjMaIaHq30s"
# URL aggiornato alla versione v1 (stabile) senza beta
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="Guardiano Contratti", page_icon="🛡️")

st.title("🛡️ Guardiano del Contratto Globale AI")

# Aggiungiamo un campo per inserire la chiave a mano se quella nel codice fallisce
user_key = st.sidebar.text_input("Inserisci API Key (opzionale)", type="password")
final_key = user_key if user_key else API_KEY

file_pdf = st.file_uploader("Carica contratto (PDF)", type="pdf")

if file_pdf:
    if st.button("🚀 AVVIA ANALISI"):
        with st.spinner('Analisi in corso...'):
            try:
                # Lettura PDF
                reader = PyPDF2.PdfReader(file_pdf)
                testo = "".join([p.extract_text() for p in reader.pages])
                
                # Chiamata di emergenza
                payload = {
                    "contents": [{"parts": [{"text": f"Analizza rischi e equità di questo contratto: {testo[:10000]}"}]}]
                }
                
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={final_key}"
                res = requests.post(url, json=payload)
                data = res.json()
                
                if res.status_code == 200:
                    st.write(data['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"Errore: {data.get('error', {}).get('message', 'Controlla la tua API Key')}")
            except Exception as e:
                st.error(f"Errore tecnico: {e}")
