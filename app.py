import streamlit as st
import PyPDF2
import requests
import json
import os  # <--- AGGIUNTO: Necessario per leggere i Secrets in sicurezza

# --- NUOVA CONFIGURAZIONE CHIAVE SICURA ---
# Legge la chiave direttamente dai Secrets di Streamlit o dall'ambiente locale
API_KEY = os.environ.get("GEMINI_API_KEY")

# Configura l'URL solo se la chiave esiste, per evitare errori di link malformati
if API_KEY:
    API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
else:
    API_URL = ""

st.set_page_config(page_title="Guardiano Contratti", page_icon="🛡️")

st.title("🛡️ Guardiano del Contratto Globale AI")
st.info("Analisi professionale attiva con nuova chiave API sicura.")

# Controllo iniziale se la chiave è configurata
if not API_KEY:
    st.error("⚠️ Chiave API non trovata! Ricordati di inserirla nei Secrets di Streamlit Cloud usando il nome GEMINI_API_KEY.")

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
                    testo_completo += page.extract_text()
                
                if not testo_completo.strip():
                    st.error("Il file sembra vuoto o non leggibile.")
                else:
                    # 2. Costruzione della richiesta
                    prompt = (
                        "Agisci come un avvocato esperto. Analizza questo contratto in italiano: "
                        "1. Identifica i 3 rischi più gravi. "
                        "2. Segnala eventuali clausole vessatorie. "
                        "3. Esprimi un voto di equità da 1 a 10. "
                        f"\n\nTesto contratto:\n{testo_completo[:15000]}"
                    )
                    
                    payload = {
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }]
                    }
                    
                    # 3. Invio a Google
                    response = requests.post(
                        API_URL,
                        headers={'Content-Type': 'application/json'},
                        data=json.dumps(payload)
                    )
                    
                    # 4. Gestione Risposta
                    risultato = response.json()
                    
                    if response.status_code == 200:
                        analisi = risultato['candidates'][0]['content']['parts'][0]['text']
                        st.markdown("---")
                        st.markdown("### 📋 Analisi del Contratto:")
                        st.write(analisi)
                    else:
                        errore_msg = risultato.get('error', {}).get('message', 'Errore sconosciuto')
                        st.error(f"Errore API: {errore_msg}")

            except Exception as e:
                st.error(f"Errore tecnico: {e}")

st.caption("Nota: Analisi basata su intelligenza artificiale. Non sostituisce un legale.")
