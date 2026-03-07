import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- CONFIGURAZIONE ---
API_KEY = "AIzaSyAMb8tZrMuEWxBxNVX_GX_0sjMaIaHq30s"
genai.configure(api_key=API_KEY)

# Usiamo 1.5-flash: è velocissimo e ottimo per leggere documenti
model = genai.GenerativeModel('gemini-1.5-pro')

st.set_page_config(page_title="Guardiano del Contratto", page_icon="🛡️", layout="centered")

st.title("🛡️ Guardiano del Contratto Globale AI")
st.info("Analisi professionale dei rischi contrattuali in pochi secondi.")

file_pdf = st.file_uploader("Carica il tuo contratto (PDF)", type="pdf")

if file_pdf:
    # Mostra un'anteprima del caricamento
    st.success("File caricato correttamente!")
    
    if st.button("🚀 AVVIA ANALISI"):
        with st.spinner('L’AI sta leggendo le clausole...'):
            try:
                # Estrazione testo migliorata
                reader = PyPDF2.PdfReader(file_pdf)
                testo = ""
                for page in reader.pages:
                    testo += page.extract_text()
                
                if not testo.strip():
                    st.error("Il PDF sembra non contenere testo leggibile (forse è un'immagine?).")
                else:
                    # Prompt più strutturato per risultati migliori
                    prompt = (
                        "Agisci come un esperto legale. Analizza il seguente contratto in italiano. "
                        "1. Elenca i 3 rischi principali per chi firma. "
                        "2. Indica eventuali clausole vessatorie o squilibrate. "
                        "3. Dai un voto di equità da 1 a 10 con una breve spiegazione. "
                        f"\n\nTesto del contratto:\n{testo[:15000]}" # Limite aumentato a 15k caratteri
                    )
                    
                    risposta = model.generate_content(prompt)
                    
                    st.markdown("---")
                    st.markdown("### 📋 Risultato dell'Analisi Professionale")
                    st.write(risposta.text)
                    
            except Exception as e:
                # Questo cattura l'errore 404 e spiega cosa fare
                if "404" in str(e):
                    st.error("Errore di configurazione: Il modello specificato non è disponibile. Prova a cambiare 'gemini-1.5-flash' con 'gemini-1.5-pro' nel codice.")
                else:
                    st.error(f"Si è verificato un errore: {e}")

# --- FOOTER ---
st.caption("Nota: Questa analisi è generata da un'IA e non sostituisce il parere di un avvocato.")
