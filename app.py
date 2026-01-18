import streamlit as st

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", layout="wide")

# --- 2. INITIALISATION ---
if 'etape' not in st.session_state: st.session_state.etape = "start_page"
if 'vies' not in st.session_state: st.session_state.vies = 5
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'niveau' not in st.session_state: st.session_state.niveau = None
if 'leçon_index' not in st.session_state: st.session_state.leçon_index = 0

# --- 3. PROGRAMME PÉDAGOGIQUE ---
PROGRAMME = {
    "Débutant": [
        {"titre": "Se Présenter", "regle": "Utilisez 'My name is' pour le nom.", "ex": "My name is Clarisse.", "test": "Traduisez : 'Mon nom est Marc'", "rep": "my name is marc", "aide": "Structure : My name + IS + Prénom."},
        {"titre": "Le Verbe ÊTRE", "regle": "I am, You are, He/She/It is.", "ex": "She is a teacher.", "test": "Traduisez : 'Elle est professeur'", "rep": "she is a teacher", "aide": "Pour 'elle', on utilise 'She is'."}
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

# --- 5. STYLE CSS (CENTRAGE + COULEURS FORCÉES) ---
st.markdown("""
    <style>
    /* Centrage de tous les boutons */
    div.stButton {
        display: flex;
        justify-content: center;
    }

    /* Style de base des boutons */
    .stButton > button {
        height: 75px !important;
        width: 450px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        color: white !important;
        border-radius: 15px !important;
        text-transform: uppercase !important;
        border: none !important;
        margin-bottom: 10px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important;
    }

    /* Couleurs de la page de présentation par ordre d'apparition */
    /* 1. DÉBUTANT : VERT */
    div.stButton:nth-of-type(1) button { background-color: #2ED573 !important; }
    /* 2. INTERMÉDIAIRE : JAUNE/ORANGE */
    div.stButton:nth-of-type(2) button { background-color: #ECCC68 !important; }
    /* 3. AVANCÉ : VIOLET */
    div.stButton:nth-of-type(3) button { background-color: #A29BFE !important; }

    /* Bouton DÉMARRER (Gris anthracite) */
    .start-btn button { background-color: #2F3542 !important; }

    .stButton > button:hover {
        filter: brightness(1.1);
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 6. INTERFACE ---

# ÉTAPE 0 : DÉMARRAGE
if st.session_state.etape == "start_page":
    st.markdown("<h1 style='text-align: center;'>🎓 Clarisse English Academy</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="start-btn">', unsafe_allow_html=True)
        if st.button("DÉMARRER"):
            st.session_state.etape = "presentation"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ÉTAPE 1 : PRÉSENTATION & CHOIX DU NIVEAU
elif st.session_state.etape == "presentation":
    st.markdown("<h1 style='text-align: center;'>🎓 Clarisse English Academy</h1>", unsafe_allow_html=True)
    msg = "Bonjour, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage. Quel est ton niveau actuel ?"
    st.markdown(f"<h3 style='text-align: center; padding: 20px;'>{msg}</h3>", unsafe_allow_html=True)
    
    parler(msg)
    
    # Boutons avec couleurs distinctes et centrage
    if st.button("DÉBUTANT"):
        st.session_state.update({"niveau": "Débutant", "etape": "cours", "leçon_index": 0})
        st.rerun()
    if st.button("INTERMÉDIAIRE"):
        st.session_state.update({"niveau": "Intermédiaire", "etape": "cours", "leçon_index": 0})
        st.rerun()
    if st.button("AVANCÉ"):
        st.session_state.update({"niveau": "Avancé", "etape": "cours", "leçon_index": 0})
        st.rerun()

# ÉTAPE 2 : COURS
elif st.session_state.etape == "cours":
    st.markdown(f"<h3 style='text-align: center;'>❤️ Vies : {st.session_state.vies} | ⭐ XP : {st.session_state.xp}</h3>", unsafe_allow_html=True)
    
    leçons = PROGRAMME[st.session_state.niveau]
    idx = st.session_state.leçon_index
    
    if idx < len(leçons):
        courant = leçons[idx]
        st.header(f"Niveau {st.session_state.niveau} - Leçon {idx + 1}")
        st.info(f"*Règle :* {courant['regle']}\n\n**Exemple :** {courant['ex']}")
        
        reponse = st.text_input(f"EXERCICE : {courant['test']}", key=f"ex_{idx}").lower().strip()
        
        if st.button("VALIDER"):
            if reponse == courant['rep']:
                st.success("C'est bien !")
                st.session_state.xp += 10
                st.session_state.leçon_index += 1
                st.rerun()
            else:
                st.error(f"Félicitations pour l'essai, mais c'est faux. Aide : {courant['aide']}")
                st.session_state.vies -= 1
                if st.session_state.vies <= 0:
                    st.session_state.etape = "game_over"
                st.rerun()
    else:
        st.balloons()
        st.success("Bravo ! Niveau terminé. Même Shakespeare n'aurait pas fait mieux ! 😉")
        if st.button("RETOUR AU MENU"):
            st.session_state.etape = "presentation"
            st.rerun()

# ÉTAPE 3 : GAME OVER
elif st.session_state.etape == "game_over":
    st.markdown("<h1 style='text-align: center; color: red;'>❌ GAME OVER</h1>", unsafe_allow_html=True)
    if st.button("RECOMMENCER"):
        st.session_state.update({"etape": "start_page", "vies": 5, "xp": 0})
        st.rerun()
