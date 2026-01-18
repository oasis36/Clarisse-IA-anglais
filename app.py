import streamlit as st

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", layout="wide")

# --- 2. STYLE CSS SIMPLIFIÉ ET PUISSANT ---
st.markdown("""
    <style>
    /* Force la taille et le texte des boutons */
    .stButton > button {
        height: 80px !important;
        width: 100% !important;
        font-size: 24px !important;
        font-weight: bold !important;
        color: white !important;
        border-radius: 15px !important;
        text-transform: uppercase !important;
        border: None !important;
    }
    
    /* Couleurs par position dans la page */
    /* Bouton 1 (Vert) */
    div.stButton:nth-of-type(1) button { background-color: #28a745 !important; }
    /* Bouton 2 (Orange) */
    div.stButton:nth-of-type(2) button { background-color: #ff8c00 !important; }
    /* Bouton 3 (Violet) */
    div.stButton:nth-of-type(3) button { background-color: #6f42c1 !important; }
    
    /* Bouton DÉMARRER (Gris/Noir) */
    .start-btn button { background-color: #343a40 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INITIALISATION ---
if 'etape' not in st.session_state: st.session_state.etape = "start_page"
if 'vies' not in st.session_state: st.session_state.vies = 5
if 'xp' not in st.session_state: st.session_state.xp = 0

# --- 4. AUDIO ---
def parler(txt):
    js = f"<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{txt.replace("'", "\\'")}'); m.lang = 'fr-FR'; window.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 5. INTERFACE ---

# ÉTAPE 0 : DÉMARRAGE
if st.session_state.etape == "start_page":
    st.markdown("<h1 style='text-align: center;'>🎓 Clarisse English Academy</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Prêt à commencer ?</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="start-btn">', unsafe_allow_html=True)
        if st.button("DÉMARRER"):
            st.session_state.etape = "presentation"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ÉTAPE 1 : PRÉSENTATION
elif st.session_state.etape == "presentation":
    st.markdown("<h1 style='text-align: center;'>🎓 Clarisse English Academy</h1>", unsafe_allow_html=True)
    msg = "Bonjour, je m'appelle Clarisse. Quel est ton niveau actuel ?"
    st.markdown(f"<h2 style='text-align: center;'>{msg}</h2>", unsafe_allow_html=True)
    
    parler(msg)
    
    # Centrage des 3 boutons de niveau
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("DÉBUTANT"):
            st.session_state.update({"niveau": "Débutant", "etape": "cours"})
            st.rerun()
        if st.button("INTERMÉDIAIRE"):
            st.session_state.update({"niveau": "Intermédiaire", "etape": "cours"})
            st.rerun()
        if st.button("AVANCÉ"):
            st.session_state.update({"niveau": "Avancé", "etape": "cours"})
            st.rerun()

# ÉTAPE 2 : COURS (STRUCTURE VIDE POUR LE TEST)
elif st.session_state.etape == "cours":
    st.markdown(f"<h3 style='text-align: center;'>❤️ Vies : {st.session_state.vies} | ⭐ XP : {st.session_state.xp}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Niveau : {st.session_state.niveau}</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("RETOUR AU MENU"):
            st.session_state.etape = "presentation"
            st.rerun()
