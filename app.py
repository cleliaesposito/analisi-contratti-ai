import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- CONFIGURAZIONE ---
# La chiave deve essere sempre tra virgolette per essere letta come testo
API_KEY = "AIzaSyAMb8tZrMuEWxBxNVX_GX_0sjMaIaHq30s"
genai.configure(api_key=API_KEY)

# Usiamo il modello 1.5-pro, ottimo per l'analisi legale
model = genai.GenerativeModel('gemini-1.5-pro')

st.set_page_config(page_title="Guardiano del Contratto", page_icon="🛡️")

st.title("🛡️ Guardiano del Contratto Globale AI")
st.info("Analisi professionale dei rischi contrattuali in pochi secondi.")

file_pdf = st.file_uploader("Carica il tuo contratto (PDF)", type="pdf")

if file_pdf:
    st.success("File caricato correttamente!")
    
    if st.button("🚀 AVVIA ANALISI"):
        with st.spinner('L’AI sta analizzando il documento...'):
            try:
                # Estrazione del testo dal PDF
                reader = PyPDF2.PdfReader(file_pdf)
                testo = ""
                for page in reader.pages:
                    testo += page.extract_text()
                
                if not testo.strip():
                    st.error("Il PDF non contiene testo leggibile.")
                else:
                    # Prompt ottimizzato per l'analisi
                    prompt = (
                        "Agisci come un avvocato esperto. Analizza il seguente contratto in italiano:\n"
                        "1. Identifica i 3 rischi principali per l'utente.\n"
                        "2. Segnala eventuali clausole poco chiare o vessatorie.\n"
                        "3. Esprimi un voto di equità da 1 a 10.\n\n"
                        f"Testo del contratto:\n{testo[:15000]}"
                    )
                    
                    risposta = model.generate_content(prompt)
                    
                    st.markdown("---")
                    st.markdown("### 📋 Risultato dell'Analisi:")
                    st.write(risposta.text)
                    
            except Exception as e:
                st.error(f"Si è verificato un errore: {e}")

st.caption("Nota: Questa analisi è a scopo informativo e non sostituisce un parere legale professionale.")
