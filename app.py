import streamlit as st
import PyPDF2
import google.generativeai as genai
import os

# --- CONFIGURAZIONE CHIAVE API SICURA ---
# Leggiamo la chiave direttamente dai Secrets di Streamlit
API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    # Usiamo la libreria ufficiale che gestisce da sola l'endpoint corretto
    genai.configure(api_key=API_KEY)
else:
    st.error("⚠️ Chiave API non trovata! Inseriscila nei Secrets di Streamlit Cloud.")

st.set_page_config(page_title="Guardiano Contratti", page_icon="🛡️")

st.title("🛡️ Guardiano del Contratto Globale AI")
st.info("Analisi professionale attiva con configurazione ufficiale.")

file_pdf = st.file_uploader("Carica il tuo contratto (PDF)", type="pdf")

if file_pdf and API_KEY:
    st.success("Documento pronto per l'analisi.")
    
    if st.button("🚀 AVVIA ANALISI"):
        with st.spinner('L’AI sta esaminando le clausole...'):
            try:
                # 1. Lettura testo dal PDF
                reader = PyPDF2.PdfReader(file_pdf)
                testo_completo = ""
                for page in reader.pages:
                    testo_completo += page.extract_text() or ""
                
                if not testo_completo.strip():
                    st.error("Il file sembra vuoto o non leggibile.")
                else:
                    # 2. Inizializzazione del modello corretto
                    model = genai.GenerativeModel('models/gemini-1.5-flash')
                    
                    # 3. Costruzione del prompt professionale
                    prompt = (
                        "Agisci come un avvocato esperto. Analizza questo contratto in italiano:\n"
                        "1. Identifica i 3 rischi più gravi.\n"
                        "2. Segnala eventuali clausole vessatorie.\n"
                        "3. Esprimi un voto di equità da 1 a 10.\n\n"
                        f"Testo contratto:\n{testo_completo[:15000]}"
                    )
                    
                    # 4. Generazione del contenuto tramite libreria ufficiale
                    response = model.generate_content(prompt)
                    
                    # 5. Mostra il risultato
                    st.markdown("---")
                    st.markdown("### 📋 Analisi del Contratto:")
                    st.write(response.text)

            except Exception as e:
                st.error(f"Errore tecnico durante la generazione: {e}")

st.caption("Nota: Analisi basata su intelligenza artificiale. Non sostituisce un legale.")
