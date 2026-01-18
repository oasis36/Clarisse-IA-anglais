import streamlit as st
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓", layout="wide")

# Style CSS Corrigé pour des couleurs distinctes
st.markdown("""
    <style>
    /* Style de base commun */
    .stButton > button {
        height: 70px;
        font-size: 22px !important;
        font-weight: bold;
        color: white !important;
        border-radius: 10px;
        border: none;
        margin-bottom: 10px;
        transition: 0.3s;
    }

    /* Ciblage spécifique par bloc pour garantir les couleurs */
    /* Débutant (Bleu) */
    [data-testid="stVerticalBlock"] > div:nth-child(1) button {
        background-color: #007bff !important;
    }
    /* Intermédiaire (Orange) */
    [data-testid="stVerticalBlock"] > div:nth-child(2) button {
        background-color: #ff8c00 !important;
    }
    /* Avancé (Vert) */
    [data-testid="stVerticalBlock"] > div:nth-child(3) button {
        background-color: #28a745 !important;
    }
    
    .stButton > button:hover { 
        opacity: 0.8; 
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALISATION ---
if 'etape' not in st.session_state: st.session_state.etape = "start_page"
if 'niveau' not in st.session_state: st.session_state.niveau = "Débutant"
if 'leçon_index' not in st.session_state: st.session_state.leçon_index = 0
if 'vies' not in st.session_state: st.session_state.vies = 5
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'erreurs' not in st.session_state: st.session_state.erreurs = []
if 'mode_revision' not in st.session_state: st.session_state.mode_revision = False
if 'last_audio_key' not in st.session_state: st.session_state.last_audio_key = ""

# --- 3. PROGRAMME PÉDAGOGIQUE ---
PROGRAMME = {
    "Débutant": [
        {"titre": "Se Présenter", "regle": "Utilisez 'My name is' pour le nom.", "ex": "My name is Clarisse.", "test": "Traduisez : 'Mon nom est Marc'", "rep": "my name is marc", "aide": "Structure : My name + IS + Prénom."},
        {"titre": "Le Verbe ÊTRE", "regle": "I am, You are, He/She/It is.", "ex": "She is a teacher.", "test": "Traduisez : 'Elle est professeur' (teacher)", "rep": "she is a teacher", "aide": "Pour elle, on utilise 'She is'."},
        {"titre": "Les Articles A/AN", "regle": "'A' (consonne), 'AN' (voyelle).", "ex": "A dog, An apple.", "test": "Comment dit-on 'Une pomme' ? (apple)", "rep": "an apple", "aide": "Apple commence par une voyelle, utilisez 'an'."}
    ],
    "Intermédiaire": [
        {"titre": "Le Présent Continu", "regle": "BE + Verbe-ING.", "ex": "I am eating.", "test": "Traduisez : 'Je suis en train de manger'", "rep": "i am eating", "aide": "Utilisez am/is/are + verbe-ing."}
    ],
    "Avancé": [
        {"titre": "Le Present Perfect", "regle": "HAVE + Participe passé.", "ex": "I have lost my keys.", "test": "Traduisez : 'J'ai perdu mes clés' (lost my keys)", "rep": "i have lost my keys", "aide": "Utilisez l'auxiliaire HAVE."}
    ]
}

# --- 4. FONCTIONS AUDIO ---
def parler_simple(txt):
    js = f"<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{txt.replace("'", "\\'")}'); m.lang = 'fr-FR'; window.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 5. INTERFACE ---
if st.session_state.etape == "start_page":
    st.title("🎓 Clarisse English Academy")
    if st.button("DÉMARRER", use_container_width=True):
        st.session_state.etape = "presentation"
        st.rerun()

elif st.session_state.etape == "presentation":
    st.title("🎓 Clarisse English Academy")
    st.write("Bonjour, je m'appelle Clarisse. Choisissez votre niveau :")
    
    if st.session_state.last_audio_key != "intro":
        parler_simple("Bonjour, je m'appelle Clarisse. Choisissez votre niveau.")
        st.session_state.last_audio_key = "intro"
    
    # Boutons avec couleurs distinctes
    if st.button("DÉBUTANT", use_container_width=True):
        st.session_state.update({"niveau": "Débutant", "etape": "cours", "leçon_index": 0, "erreurs": [], "vies": 5})
        st.rerun()
        
    if st.button("INTERMÉDIAIRE", use_container_width=True):
        st.session_state.update({"niveau": "Intermédiaire", "etape": "cours", "leçon_index": 0, "erreurs": [], "vies": 5})
        st.rerun()
        
    if st.button("AVANCÉ", use_container_width=True):
        st.session_state.update({"niveau": "Avancé", "etape": "cours", "leçon_index": 0, "erreurs": [], "vies": 5})
        st.rerun()
