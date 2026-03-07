import streamlit as st
import PyPDF2
import requests
import json

# --- CONFIGURAZIONE ---
API_KEY = "AIzaSyAMb8tZrMuEWxBxNVX_GX_0sjMaIaHq30s"
# Usiamo l'endpoint stabile v1 invece della v1beta
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="Guardiano del Contratto", page_icon="🛡️")

st.title("🛡️ Guardiano del Contratto Globale AI")
st.info("Analisi professionale dei rischi contrattuali via Direct API Access.")

file_pdf = st.file_uploader("Carica il tuo contratto (PDF)", type="pdf")

if file_pdf:
    st.success("File caricato correttamente!")
    
    if st.button("🚀 AVVIA ANALISI"):
        with st.spinner('L’AI sta analizzando il documento tramite connessione diretta...'):
            try:
                # 1. Estrazione testo dal PDF
                reader = PyPDF2.PdfReader(file_pdf)
                testo_contratto = ""
                for page in reader.pages:
                    testo_contratto += page.extract_text()
                
                if not testo_contratto.strip():
                    st.error("Il PDF non contiene testo leggibile.")
                else:
                    # 2. Preparazione del Payload per la chiamata diretta
                    prompt = (
                        "Agisci come un esperto legale esperto in diritto civile italiano. "
                        "Analizza questo contratto e fornisci: "
                        "1) I 3 rischi principali. 2) Eventuali clausole vessatorie. 3) Voto equità 1-10. "
                        f"\n\nTesto contratto:\n{testo_contratto[:15000]}"
                    )
                    
                    payload = {
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }]
                    }
                    
                    # 3. Chiamata HTTP post
                    response = requests.post(
                        API_URL,
                        headers={'Content-Type': 'application/json'},
                        data=json.dumps(payload)
                    )
                    
                    # 4. Elaborazione risposta
                    result = response.json()
                    
                    if response.status_code == 200:
                        testo_risposta = result['candidates'][0]['content']['parts'][0]['text']
                        st.markdown("---")
                        st.markdown("### 📋 Esito Analisi Professionale:")
                        st.write(testo_risposta)
                    else:
                        st.error(f"Errore API ({response.status_code}): {result.get('error', {}).get('message', 'Errore sconosciuto')}")

            except Exception as e:
                st.error(f"Errore di sistema: {e}")

st.caption("Nota: Metodo Direct-Access v1.0. Analisi automatizzata non vincolante.")
