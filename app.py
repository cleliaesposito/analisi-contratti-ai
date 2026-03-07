import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- CONFIGURAZIONE ---
API_KEY = "AIzaSyAMb8tZrMuEWxBxNVX_GX_0sjMaIaHq30s" 
genai.configure(api_key=API_KEY)

# Cambiato in 'gemini-1.5-flash' che è il più compatibile con le API attuali
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Guardiano del Contratto", page_icon="🛡️")

st.title("🛡️ Guardiano del Contratto Globale AI")
st.info("Analisi professionale dei rischi contrattuali in pochi secondi.")

file_pdf = st.file_uploader("Carica il tuo contratto (PDF)", type="pdf")

if file_pdf:
    st.success("File caricato correttamente!")
    
    if st.button("🚀 AVVIA ANALISI"):
        with st.spinner('L’AI sta analizzando le clausole...'):
            try:
                reader = PyPDF2.PdfReader(file_pdf)
                testo = ""
                for page in reader.pages:
                    testo += page.extract_text()
                
                if not testo.strip():
                    st.error("Il PDF non contiene testo leggibile.")
                else:
                    prompt = (
                        "Agisci come un esperto legale. Analizza il seguente contratto in italiano: "
                        "\n1. Elenca i 3 rischi principali per chi firma."
                        "\n2. Indica eventuali clausole squilibrate."
                        "\n3. Dai un voto di equità da 1 a 10."
                        f"\n\nTesto:\n{testo[:15000]}"
                    )
                    
                    # Generazione contenuto
                    risposta = model.generate_content(prompt)
                    
                    st.markdown("---")
                    st.markdown("### 📋 Risultato dell'Analisi:")
                    st.write(risposta.text)
                    
            except Exception as e:
                st.error(f"Si è verificato un errore: {e}")

st.caption("Nota: Questa analisi è a scopo informativo e non sostituisce un parere legale.")
