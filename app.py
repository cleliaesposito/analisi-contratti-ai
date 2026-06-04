import streamlit as st
import pypdf
import google.generativeai as genai
import os

st.set_page_config(
    page_title="Guardiano Contratti",
    page_icon="🛡️",
    menu_items={
        "About": (
            "**Guardiano del Contratto Globale AI** — Strumento di analisi automatizzata. "
            "Non fornisce consulenza legale ai sensi del D.Lgs. 247/2012. "
            "Dati elaborati tramite Google Gemini API."
        ),
    },
)

API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# --- Sidebar: riferimenti normativi e privacy ---
with st.sidebar:
    st.markdown("### ⚖️ Nota Legale")
    st.markdown(
        "Le analisi prodotte da questo strumento sono generate automaticamente da un modello AI "
        "e **non costituiscono consulenza legale** ai sensi del D.Lgs. 247/2012. "
        "Non sostituiscono il parere di un avvocato iscritto all'Albo."
    )
    st.markdown("---")
    st.markdown("### 🔒 Trattamento Dati")
    st.markdown(
        "Il testo estratto dal documento viene trasmesso a **Google Gemini API** "
        "unicamente per generare la risposta. "
        "Questa applicazione non archivia né registra alcun dato.\n\n"
        "Titolare del trattamento lato Google: "
        "[Google AI Terms of Service](https://ai.google.dev/gemini-api/terms)\n\n"
        "Per esercitare i diritti GDPR (Art. 15-22) contatta il titolare dell'applicazione."
    )
    st.markdown("---")
    st.caption("v1.1 · MIT License · © 2024 Clelia Esposito")

st.title("🛡️ Guardiano del Contratto Globale AI")

# --- Consenso informato (GDPR Art. 6 + Art. 13) ---
if "consent_given" not in st.session_state:
    st.session_state.consent_given = False

with st.expander(
    "📋 Informativa sul trattamento dei dati e condizioni d'uso — **da leggere prima di procedere**",
    expanded=not st.session_state.consent_given,
):
    st.markdown(
        """
**AVVERTENZA LEGALE (D.Lgs. 247/2012 — Ordinamento Forense Italiano)**

Questo strumento produce osservazioni automatizzate su documenti contrattuali tramite intelligenza artificiale.
L'output generato:
- **non costituisce consulenza legale** né parere professionale vincolante;
- **può contenere errori**, omissioni o imprecisioni tipiche dei modelli linguistici (c.d. allucinazioni);
- **non può essere citato** in procedimenti legali come fonte autorevole.

Per valutazioni legalmente rilevanti rivolgiti esclusivamente a un avvocato abilitato.

---

**INFORMATIVA PRIVACY (Reg. UE 2016/679 — GDPR, Art. 13)**

*Titolare del trattamento:* il gestore di questa applicazione.

*Finalità e base giuridica:* elaborazione del documento caricato per generare un'analisi AI,
sulla base del consenso espresso dall'utente (Art. 6.1.a GDPR).

*Destinatari dei dati:* il testo estratto dal PDF viene trasmesso a **Google LLC** tramite le API
Google Gemini esclusivamente per la generazione della risposta. Google agisce come responsabile
del trattamento (Art. 28 GDPR). L'applicazione non archivia né trasmette i dati a terze parti ulteriori.

*Conservazione:* i dati non vengono memorizzati da questa applicazione; la sessione è volatile.

*Diritti dell'interessato (Artt. 15-22 GDPR):* accesso, rettifica, cancellazione, opposizione,
portabilità. Per esercitarli contatta il titolare dell'applicazione.

*Nota:* i contratti spesso contengono dati personali di terzi. Assicurati di essere autorizzato
al trattamento di tali dati prima di caricare il documento.

---

**Caricando un documento e procedendo dichiari di:**
1. aver letto e compreso questa informativa;
2. prestare il consenso al trattamento dei dati come sopra descritto;
3. essere autorizzato a trattare i dati contenuti nel documento;
4. non fare affidamento esclusivo su questo output per decisioni legali o commerciali.
        """
    )
    if st.checkbox("Ho letto l'informativa e presto il consenso al trattamento dei dati"):
        st.session_state.consent_given = True
        st.success("Consenso registrato per questa sessione. Puoi procedere.")

if not st.session_state.consent_given:
    st.stop()

# --- Verifica chiave API ---
if not API_KEY:
    st.error(
        "⚠️ Chiave API non configurata. "
        "Aggiungila nei **Secrets** di Streamlit Cloud con la chiave `GEMINI_API_KEY`."
    )
    st.stop()

# --- Caricamento documento ---
file_pdf = st.file_uploader(
    "Carica il tuo contratto (PDF testuale — non scansioni)",
    type="pdf",
    help="Sono supportati solo PDF con testo selezionabile. I PDF basati su immagini/scansioni non verranno letti correttamente.",
)

if file_pdf:
    st.success("Documento pronto per l'analisi.")

    if st.button("🚀 AVVIA ANALISI"):
        with st.spinner("L'AI sta esaminando le clausole..."):
            try:
                reader = pypdf.PdfReader(file_pdf)
                testo_completo = ""
                for page in reader.pages:
                    testo_completo += page.extract_text() or ""

                if not testo_completo.strip():
                    st.error(
                        "Il file non contiene testo selezionabile. "
                        "I PDF generati da scansioni o immagini non sono supportati: "
                        "utilizza un PDF testuale o converto prima con OCR."
                    )
                else:
                    MAX_CHARS = 15000
                    troncato = len(testo_completo) > MAX_CHARS
                    testo_da_analizzare = testo_completo[:MAX_CHARS]

                    model = genai.GenerativeModel("models/gemini-1.5-flash")
                    prompt = (
                        "Agisci come un avvocato esperto. Analizza questo contratto in italiano:\n"
                        "1. Identifica i 3 rischi più gravi.\n"
                        "2. Segnala eventuali clausole vessatorie.\n"
                        "3. Esprimi un voto di equità da 1 a 10.\n\n"
                        f"Testo contratto:\n{testo_da_analizzare}"
                    )

                    response = model.generate_content(prompt)

                    if troncato:
                        st.warning(
                            f"Il contratto supera {MAX_CHARS:,} caratteri: "
                            f"analizzati solo i primi {MAX_CHARS:,}. "
                            "Le clausole finali potrebbero non essere valutate."
                        )

                    st.markdown("---")
                    st.markdown("### 📋 Analisi del Contratto:")
                    st.write(response.text)

                    st.warning(
                        "**Disclaimer post-analisi:** questo output è generato da un modello AI e non costituisce "
                        "consulenza legale (D.Lgs. 247/2012). Prima di firmare qualsiasi contratto "
                        "rivolgiti a un avvocato abilitato per una valutazione professionale."
                    )

            except Exception as e:
                st.error(f"Errore tecnico durante la generazione: {e}")

st.caption(
    "Guardiano del Contratto Globale AI · "
    "Non fornisce consulenza legale · "
    "Dati elaborati via Google Gemini API · "
    "MIT License"
)
