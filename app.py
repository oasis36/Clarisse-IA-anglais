import streamlit as st
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓", layout="wide")

# Style CSS pour les couleurs spécifiques (Bleu, Orange, Vert)
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
    /* Page Démarrer : Bouton Gris/Bleu neutre par défaut ou spécifique */
    /* Page Présentation : Couleurs demandées */
    div.stButton:nth-of-type(1) button { background-color: #007bff !important; } /* BLEU */
    div.stButton:nth-of-type(2) button { background-color: #ff8c00 !important; } /* ORANGE */
    div.stButton:nth-of-type(3) button { background-color: #28a745 !important; } /* VERT */
    
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

# --- 2. INITIALISATION ---
if 'etape' not in st.session_state: st.session_state.etape = "start_page"
if 'niveau' not in st.session_state: st.session_state.niveau = "Débutant"
if 'leçon_index' not in st.session_state: st.session_state.leçon_index = 0
if 'vies' not in st.session_state: st.session_state.vies = 5
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'erreurs' not in st.session_state: st.session_state.erreurs = []
if 'last_audio_key' not in st.session_state: st.session_state.last_audio_key = ""

# --- 3. PROGRAMME PÉDAGOGIQUE ---
PROGRAMME = {
    "Débutant": [
        {"titre": "Se Présenter", "regle": "Utilisez 'My name is' pour le nom.", "ex": "My name is Clarisse.", "test": "Traduisez : 'Mon nom est Marc'", "rep": "my name is marc", "aide": "Structure : My name + IS + Prénom."},
        {"titre": "Le Verbe ÊTRE", "regle": "I am, You are, He/She/It is.", "ex": "She is a teacher.", "test": "Traduisez : 'Elle est professeur'", "rep": "she is a teacher", "aide": "Pour 'elle', on utilise 'She is'."},
        {"titre": "Les Articles A/AN", "regle": "'A' (consonne), 'AN' (voyelle).", "ex": "A dog, An apple.", "test": "Comment dit-on 'Une pomme' ?", "rep": "an apple", "aide": "Apple commence par une voyelle."}
    ],
    "Intermédiaire": [
        {"titre": "Le Présent Continu", "regle": "BE + Verbe-ING.", "ex": "I am eating.", "test": "Traduisez : 'Je suis en train de manger'", "rep": "i am eating", "aide": "Utilisez am/is/are + verbe-ing."}
    ],
    "Avancé": [
        {"titre": "Le Present Perfect", "regle": "HAVE + Participe passé.", "ex": "I have lost my keys.", "test": "Traduisez : 'J'ai perdu mes clés'", "rep": "i have lost my keys", "aide": "Utilisez l'auxiliaire HAVE."}
    ]
}

# --- 4. FONCTION AUDIO ---
def parler(txt):
    js = f"<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{txt.replace("'", "\\'")}'); m.lang = 'fr-FR'; window.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 5. INTERFACE ---

# ÉTAPE 0 : PAGE DE DÉMARRAGE
if st.session_state.etape == "start_page":
    st.title("🎓 Clarisse English Academy")
    st.write("### Bienvenue dans votre espace d'apprentissage.")
    if st.button("DÉMARRER"):
        st.session_state.etape = "presentation"
        st.rerun()

# ÉTAPE 1 : PRÉSENTATION & CHOIX DU NIVEAU
elif st.session_state.etape == "presentation":
    st.title("🎓 Clarisse English Academy")
    msg = "Bonjour, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage. Quel est ton niveau actuel ?"
    st.write(f"### {msg}")
    
    if st.session_state.last_audio_key != "intro":
        parler(msg)
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

# ÉTAPE 2 : COURS
elif st.session_state.etape == "cours":
    # Barre de score
    c1, c2 = st.columns(2)
    c1.markdown(f"<div class='score-box'>❤️ Vies : {st.session_state.vies}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='score-box'>⭐ XP : {st.session_state.xp}</div>", unsafe_allow_html=True)
    st.divider()

    cours = PROGRAMME[st.session_state.niveau]
    idx = st.session_state.leçon_index
    
    if idx < len(cours):
        leçon = cours[idx]
        st.header(f"Leçon {idx + 1} : {leçon['titre']}")
        st.info(f"*Règle :* {leçon['regle']}\n\n**Exemple :** {leçon['ex']}")
        
        reponse = st.text_input(f"EXERCICE : {leçon['test']}", key=f"q_{idx}").lower().strip()
        
        if st.button("Valider"):
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
        st.success("Bravo ! Niveau terminé. Même Shakespeare n'aurait pas fait mieux ! 😉")
        if st.button("Retour au menu"):
            st.session_state.update({"etape": "presentation", "leçon_index": 0})
            st.rerun()

# ÉTAPE 3 : GAME OVER
elif st.session_state.etape == "game_over":
    st.error("Jeu terminé ! Vous n'avez plus de vies.")
    if st.button("Recommencer"):
        st.session_state.update({"etape": "start_page", "vies": 5, "xp": 0})
        st.rerun()
