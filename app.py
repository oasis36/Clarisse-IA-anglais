import streamlit as st

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", layout="wide")

# --- 2. LE STYLE INVASIF (FORÇAGE BRUTAL) ---
st.markdown("""
    <style>
    /* Centrage de la colonne de boutons */
    [data-testid="stVerticalBlock"] {
        align-items: center !important;
    }

    /* Style commun forcé */
    button {
        height: 80px !important;
        width: 500px !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        color: white !important;
        border-radius: 20px !important;
        border: 4px solid rgba(255,255,255,0.2) !important;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4) !important;
        text-transform: uppercase !important;
    }

    /* CIBLAGE PAR TOOLTIP (MÉTHODE LA PLUS STABLE POUR LES COULEURS) */
    /* DÉBUTANT : VERT FLASH */
    button[aria-label="DEB"] { background-color: #00C851 !important; }
    
    /* INTERMÉDIAIRE : ORANGE ÉLECTRIQUE */
    button[aria-label="INT"] { background-color: #FF8800 !important; }
    
    /* AVANCÉ : VIOLET PROFOND */
    button[aria-label="AVA"] { background-color: #AA66CC !important; }
    
    /* DÉMARRER : NOIR/GRIS */
    button[aria-label="STA"] { background-color: #2E2E2E !important; }

    button:hover {
        transform: scale(1.05) !important;
        filter: brightness(1.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INITIALISATION ---
if 'etape' not in st.session_state: st.session_state.etape = "start_page"
if 'vies' not in st.session_state: st.session_state.vies = 5
if 'xp' not in st.session_state: st.session_state.xp = 0

# --- 4. LOGIQUE AUDIO ---
def parler(txt):
    js = f"<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{txt.replace("'", "\\'")}'); m.lang = 'fr-FR'; window.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 5. INTERFACE ---

if st.session_state.etape == "start_page":
    st.markdown("<h1 style='text-align: center;'>🎓 Clarisse English Academy</h1>", unsafe_allow_html=True)
    if st.button("DÉMARRER", help="STA"):
        st.session_state.etape = "presentation"
        st.rerun()

elif st.session_state.etape == "presentation":
    st.markdown("<h1 style='text-align: center;'>🎓 Clarisse English Academy</h1>", unsafe_allow_html=True)
    msg = "Bonjour, je m'appelle Clarisse. Quel est ton niveau actuel ?"
    st.markdown(f"<h2 style='text-align: center;'>{msg}</h2>", unsafe_allow_html=True)
    
    parler(msg)
    
    # Boutons avec identifiants forcés via le paramètre 'help'
    if st.button("DÉBUTANT", help="DEB"):
        st.session_state.update({"niveau": "Débutant", "etape": "cours", "index": 0})
        st.rerun()
        
    if st.button("INTERMÉDIAIRE", help="INT"):
        st.session_state.update({"niveau": "Intermédiaire", "etape": "cours", "index": 0})
        st.rerun()
        
    if st.button("AVANCÉ", help="AVA"):
        st.session_state.update({"niveau": "Avancé", "etape": "cours", "index": 0})
        st.rerun()

elif st.session_state.etape == "cours":
    st.write(f"❤️ {st.session_state.vies} | ⭐ {st.session_state.xp}")
    st.write(f"Niveau sélectionné : {st.session_state.niveau}")
    if st.button("Retour", help="STA"):
        st.session_state.etape = "presentation"
        st.rerun()
