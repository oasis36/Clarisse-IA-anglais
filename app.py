import streamlit as st
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓", layout="wide")

# Style CSS pour les boutons de couleur et l'interface
st.markdown("""
    <style>
    .stButton > button {
        height: 70px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        color: white !important;
        border-radius: 10px !important;
        margin-bottom: 15px !important;
        width: 100% !important;
    }
    /* Couleurs forcées pour la page de présentation */
    div.stButton:nth-of-type(1) button { background-color: #007bff !important; }
    div.stButton:nth-of-type(2) button { background-color: #ff8c00 !important; }
    div.stButton:nth-of-type(3) button { background-color: #28a745 !important; }
    
    .stButton > button:hover { opacity: 0.8; color: white !important; }
    
    .score-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALISATION DU SESSION STATE ---
if 'etape' not in st.session_state: st.session_state.etape = "presentation"
if 'niveau' not in st.session_state: st.session_state.niveau = "Débutant"
if 'leçon_index' not in st.session_state: st.session_state.leçon_index = 0
if 'vies' not in st.session_state: st.session_state.vies = 5
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'last_audio_key' not in st.session_state: st.session_state.last_audio_key = ""

# --- 3. LE COURS INTÉGRÉ (PROGRAMME) ---
PROGRAMME = {
    "Débutant": [
        {"titre": "Se Présenter", "regle": "Utilisez 'My name is' pour le nom.", "ex": "My name is Clarisse.", "test": "Traduisez : 'Mon nom est Marc'", "rep": "my name is marc", "aide": "Structure : My name + IS + Prénom."},
        {"titre": "Le Verbe ÊTRE", "regle": "I am, You are, He/She/It is.", "ex": "She is a teacher.", "test": "Traduisez : 'Elle est professeur' (teacher)", "rep": "she is a teacher", "aide": "Pour 'elle', on utilise 'She is'."},
        {"titre": "Les Articles A/AN", "regle": "'A' devant consonne, 'AN' devant voyelle.", "ex": "A dog, An apple.", "test": "Comment dit-on 'Une pomme' ? (apple)", "rep": "an apple", "aide": "Apple commence par 'A', donc utilisez 'an'."}
    ],
    "Intermédiaire": [
        {"titre": "Le Présent Continu", "regle": "Utilisé pour une action en cours : BE + Verbe-ING.", "ex": "I am eating.", "test": "Traduisez : 'Je suis en train de manger'", "rep": "i am eating", "aide": "Utilisez am/is/are + eating."}
    ],
    "Avancé": [
        {"titre": "Le Present Perfect", "regle": "Action passée avec conséquence présente : HAVE + Participe passé.", "ex": "I have lost my keys.", "test": "Traduisez : 'J'ai perdu mes clés' (lost my keys)", "rep": "i have lost my keys", "aide": "L'auxiliaire est HAVE."}
    ]
}

# --- 4. FONCTION AUDIO ---
def parler(txt, lang='fr-FR'):
    js = f"<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{txt.replace("'", "\\'")}'); m.lang = '{lang}'; window.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 5. LOGIQUE D'INTERFACE ---

# Barre de progression Vies et XP (visible pendant le cours)
if st.session_state.etape == "cours":
    c1, c2 = st.columns(2)
    c1.markdown(f"<div class='score-box'>❤️ Vies : {st.session_state.vies}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='score-box'>⭐ XP : {st.session_state.xp}</div>", unsafe_allow_html=True)
    st.divider()

# PAGE 1 : PRÉSENTATION & CHOIX DU NIVEAU
if st.session_state.etape == "presentation":
    st.title("🎓 Clarisse English Academy")
    st.write("### Bonjour, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage. Quel est ton niveau actuel ?")
    
    if st.session_state.last_audio_key != "intro":
        parler("Bonjour, je m'appelle Clarisse. Quel est ton niveau actuel ?")
        st.session_state.last_audio_key = "intro"
    
    if st.button("DÉBUTANT"):
        st.session_state.update({"niveau": "Débutant", "etape": "cours", "leçon_index": 0, "vies": 5})
        st.rerun()
    if st.button("INTERMÉDIAIRE"):
        st.session_state.update({"niveau": "Intermédiaire", "etape": "cours", "leçon_index": 0, "vies": 5})
        st.rerun()
    if st.button("AVANCÉ"):
        st.session_state.update({"niveau": "Avancé", "etape": "cours", "leçon_index": 0, "vies": 5})
        st.rerun()

# PAGE 2 : SESSION DE COURS
elif st.session_state.etape == "cours":
    cours_actuel = PROGRAMME[st.session_state.niveau]
    idx = st.session_state.leçon_index
    
    if idx < len(cours_actuel):
        leçon = cours_actuel[idx]
        st.header(f"Niveau {st.session_state.niveau} - Leçon {idx + 1}")
        
        # Affichage du cours
        with st.expander("📖 Voir la règle de grammaire", expanded=True):
            st.info(leçon['regle'])
            st.write(f"*Exemple :* {leçon['ex']}")
        
        st.write(f"### 🎯 Exercice : {leçon['test']}")
        
        # Formulaire de réponse
        reponse = st.text_input("Tape ta réponse ici :", key=f"input_{idx}").lower().strip()
        
        if st.button("Valider ma réponse"):
            if reponse == leçon['rep']:
                st.success("C'est bien !")
                st.session_state.xp += 10
                st.session_state.leçon_index += 1
                st.rerun()
            else:
                st.error(f"Félicitations pour l'essai, mais ce n'est pas tout à fait ça. Aide : {leçon['aide']}")
                st.session_state.vies -= 1
                if st.session_state.vies <= 0:
                    st.session_state.etape = "game_over"
                st.rerun()
    else:
        # VICTOIRE DU NIVEAU
        st.balloons()
        st.success("### 🎉 Niveau Complété !")
        st.write("Même Shakespeare n'aurait pas fait mieux (enfin, peut-être, mais on ne lui dira pas) ! 😉")
        if st.button("Revenir à l'accueil"):
            st.session_state.update({"etape": "presentation", "leçon_index": 0})
            st.rerun()

# PAGE 3 : GAME OVER
elif st.session_state.etape == "game_over":
    st.title("❌ Game Over")
    st.write("Tu as épuisé tes 5 vies. L'anglais, c'est comme le vélo, il faut juste remonter en selle !")
    if st.button("Réessayer"):
        st.session_state.update({"etape": "presentation", "vies": 5, "xp": 0})
        st.rerun()
