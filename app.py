import streamlit as st
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓", layout="wide")

# --- 2. INITIALISATION ---
if 'etape' not in st.session_state: st.session_state.etape = "start_page"
if 'niveau' not in st.session_state: st.session_state.niveau = "Débutant"
if 'leçon_index' not in st.session_state: st.session_state.leçon_index = 0
if 'vies' not in st.session_state: st.session_state.vies = 5
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'last_audio_key' not in st.session_state: st.session_state.last_audio_key = ""

# --- 3. PROGRAMME ---
PROGRAMME = {
    "Débutant": [{"titre": "Se Présenter", "regle": "Utilisez 'My name is' pour le nom.", "ex": "My name is Clarisse.", "test": "Traduisez : 'Mon nom est Marc'", "rep": "my name is marc", "aide": "Structure : My name + IS + Prénom."}],
    "Intermédiaire": [{"titre": "Le Présent Continu", "regle": "BE + Verbe-ING.", "ex": "I am eating.", "test": "Traduisez : 'Je suis en train de manger'", "rep": "i am eating", "aide": "Utilisez am/is/are + verbe-ing."}],
    "Avancé": [{"titre": "Le Present Perfect", "regle": "HAVE + Participe passé.", "ex": "I have lost my keys.", "test": "Traduisez : 'J'ai perdu mes clés'", "rep": "i have lost my keys", "aide": "Utilisez l'auxiliaire HAVE."}]
}

def parler(txt):
    js = f"<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{txt.replace("'", "\\'")}'); m.lang = 'fr-FR'; window.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 4. STYLE CSS GLOBAL ---
st.markdown("""
    <style>
    div.stButton > button {
        display: block;
        margin: 0 auto;
        height: 70px !important;
        width: 100% !important;
        font-size: 22px !important;
        font-weight: bold !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        transition: 0.3s;
    }
    /* Ciblage par position pour forcer les couleurs */
    .stButton:nth-of-type(1) button { background-color: #28a745 !important; } /* Vert */
    .stButton:nth-of-type(2) button { background-color: #fd7e14 !important; } /* Orange */
    .stButton:nth-of-type(3) button { background-color: #6f42c1 !important; } /* Violet */
    
    .stButton > button:hover { filter: brightness(1.2); transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# --- 5. INTERFACE ---

if st.session_state.etape == "start_page":
    st.markdown("<h1 style='text-align: center;'>🎓 Clarisse English Academy</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("DÉMARRER"):
            st.session_state.etape = "presentation"
            st.rerun()

elif st.session_state.etape == "presentation":
    st.markdown("<h1 style='text-align: center;'>🎓 Clarisse English Academy</h1>", unsafe_allow_html=True)
    msg = "Bonjour, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage. Quel est ton niveau actuel ?"
    st.markdown(f"<h3 style='text-align: center;'>{msg}</h3>", unsafe_allow_html=True)
    
    if st.session_state.last_audio_key != "intro":
        parler(msg)
        st.session_state.last_audio_key = "intro"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("DÉBUTANT"):
            st.session_state.update({"niveau": "Débutant", "etape": "cours", "leçon_index": 0})
            st.rerun()
        if st.button("INTERMÉDIAIRE"):
            st.session_state.update({"niveau": "Intermédiaire", "etape": "cours", "leçon_index": 0})
            st.rerun()
        if st.button("AVANCÉ"):
            st.session_state.update({"niveau": "Avancé", "etape": "cours", "leçon_index": 0})
            st.rerun()

elif st.session_state.etape == "cours":
    st.markdown(f"<p style='text-align: center;'><b>❤️ Vies : {st.session_state.vies} | ⭐ XP : {st.session_state.xp}</b></p>", unsafe_allow_html=True)
    cours = PROGRAMME[st.session_state.niveau]
    idx = st.session_state.leçon_index
    
    if idx < len(cours):
        leçon = cours[idx]
        st.header(f"Leçon : {leçon['titre']}")
        st.info(leçon['regle'])
        reponse = st.text_input(leçon['test']).lower().strip()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Valider la réponse"):
                if reponse == leçon['rep']:
                    st.success("C'est bien !")
                    st.session_state.xp += 10
                    st.session_state.leçon_index += 1
                    st.rerun()
                else:
                    st.error(f"Félicitations pour l'essai, mais c'est faux. Aide : {leçon['aide']}")
                    st.session_state.vies -= 1
                    if st.session_state.vies <= 0:
                        st.session_state.etape = "game_over"
                    st.rerun()
    else:
        st.balloons()
        st.success("Bravo ! Niveau terminé ! 😉")
        if st.button("Retour au menu"):
            st.session_state.update({"etape": "presentation", "leçon_index": 0})
            st.rerun()

elif st.session_state.etape == "game_over":
    st.error("Jeu terminé ! Vous n'avez plus de vies.")
    if st.button("Recommencer"):
        st.session_state.update({"etape": "start_page", "vies": 5, "xp": 0})
        st.rerun()
