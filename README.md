# 🛡️ Guardiano del Contratto Globale AI

Strumento di analisi automatizzata di contratti PDF basato su **Anthropic Claude**. Carica un contratto, ottieni in pochi secondi un'analisi strutturata dei rischi, delle clausole vessatorie e un voto di equità — direttamente nel browser.

> ⚠️ **Disclaimer legale:** questo strumento genera analisi automatizzate a scopo informativo. Non costituisce consulenza legale ai sensi del D.Lgs. 247/2012. Rivolgiti sempre a un avvocato abilitato per valutazioni vincolanti.

---

## ✨ Funzionalità

- **Analisi dei rischi** — identifica i 3 rischi contrattuali più gravi con descrizione delle conseguenze
- **Rilevamento clausole vessatorie** — segnala clausole squilibrate o abusive
- **Voto di equità** — punteggio da 1 a 10 con motivazione
- **Consenso GDPR** — gate di consenso informato conforme al Reg. UE 2016/679, Art. 13
- **Privacy by design** — nessun dato archiviato; il testo viene trasmesso ad Anthropic solo per la generazione della risposta

---

## 🛠️ Stack tecnologico

| Componente | Tecnologia |
|---|---|
| Frontend | [Streamlit](https://streamlit.io) |
| LLM | [Anthropic Claude](https://www.anthropic.com) — `claude-sonnet-4-6` |
| Lettura PDF | [pypdf](https://pypdf.readthedocs.io) |
| Variabili d'ambiente | [python-dotenv](https://pypi.org/project/python-dotenv/) |

---

## 📋 Prerequisiti

- Python 3.9+
- Una chiave API Anthropic → [console.anthropic.com](https://console.anthropic.com/settings/keys)

---

## 🚀 Avvio locale

### 1. Clona il repository

```bash
git clone https://github.com/cleliaesposito/global-contract-guardian.git
cd global-contract-guardian
```

### 2. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 3. Configura la chiave API

Copia il file di esempio e inserisci la tua chiave:

```bash
cp .env.example .env
```

Apri `.env` e sostituisci il placeholder:

```env
ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Avvia l'app

```bash
streamlit run app.py
```

L'app sarà disponibile su [http://localhost:8501](http://localhost:8501).

---

## ☁️ Deploy su Streamlit Cloud

1. Fai il fork del repository su GitHub
2. Vai su [share.streamlit.io](https://share.streamlit.io) e collega il repo
3. In **Settings → Secrets**, aggiungi:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

4. Clicca **Deploy**

---

## 📁 Struttura del progetto

```
global-contract-guardian/
├── app.py              # Applicazione principale
├── requirements.txt    # Dipendenze Python
├── .env.example        # Template variabili d'ambiente
├── .env                # Chiave API locale (escluso da git)
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Configurazione

| Variabile | Descrizione |
|---|---|
| `ANTHROPIC_API_KEY` | Chiave API Anthropic (obbligatoria) |

---

## 🔒 Privacy & GDPR

Il testo estratto dai PDF viene trasmesso ad **Anthropic, PBC** tramite le API Claude per la sola generazione della risposta, sulla base del consenso esplicito dell'utente (Art. 6.1.a GDPR). L'applicazione non archivia né registra alcun dato. Per i dettagli sul trattamento lato Anthropic: [Anthropic Privacy Policy](https://www.anthropic.com/privacy).

---

## 📄 Licenza

Distribuito sotto licenza **MIT**. Vedi [`LICENSE`](LICENSE) per i dettagli.

---

## ⚖️ Note legali

Le analisi prodotte da questo strumento sono generate automaticamente da un modello AI e **non costituiscono consulenza legale** ai sensi del D.Lgs. 247/2012 (Ordinamento Forense Italiano). L'utilizzo di questo software non crea un rapporto avvocato-cliente.

---

## 👤 Autrice

**Clelia Esposito** — [@cleliaesposito_ia](https://www.instagram.com/cleliaesposito_ia) su Instagram
