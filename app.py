import streamlit as st

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", layout="wide")

# --- 2. INITIALISATION ---
if 'etape' not in st.session_state: st.session_state.etape = "start_page"
if 'vies' not in st.session_state: st.session_state.vies = 5
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'niveau' not in st.session_state: st.session_state.niveau = None

# --- 3. FONCTION AUDIO ---
def parler(txt):
    js = f"<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{txt.replace("'", "\\'")}'); m.lang = 'fr-FR'; window.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 4. LOGIQUE DE NAVIGATION VIA URL PARAMS (POUR LES BOUTONS HTML) ---
# On utilise les paramètres d'URL pour détecter le clic sur les boutons HTML
params = st.query_params

if "action" in params:
    action = params["action"]
    if action == "demarrer":
        st.session_state.etape = "presentation"
    elif action in ["Débutant", "Intermédiaire", "Avancé"]:
        st.session_state.niveau = action
        st.session_state.etape = "cours"
    # On nettoie l'URL pour éviter les boucles
    st.query_params.clear()
    st.rerun()

# --- 5. INTERFACE ---

# ÉTAPE 0 : DÉMARRAGE
if st.session_state.etape == "start_page":
    st.markdown("<h1 style='text-align: center;'>🎓 Clarisse English Academy</h1>", unsafe_allow_html=True)
    
    # Bouton HTML Centré
    st.markdown("""
        <div style="display: flex; justify-content: center;">
            <a href="/?action=demarrer" target="_self" style="
                background-color: #343a40; color: white; padding: 20px 100px; 
                text-decoration: none; font-size: 24px; font-weight: bold; 
                border-radius: 15px; text-transform: uppercase;">
                DÉMARRER
            </a>
        </div>
    """, unsafe_allow_html=True)

# ÉTAPE 1 : PRÉSENTATION & CHOIX DU NIVEAU
elif st.session_state.etape == "presentation":
    st.markdown("<h1 style='text-align: center;'>🎓 Clarisse English Academy</h1>", unsafe_allow_html=True)
    msg = "Bonjour, je m'appelle Clarisse. Quel est ton niveau actuel ?"
    st.markdown(f"<h2 style='text-align: center;'>{msg}</h2>", unsafe_allow_html=True)
    
    parler(msg)
    
    # Boutons HTML Centrés avec 3 Couleurs différentes
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; gap: 20px;">
            <a href="/?action=Débutant" target="_self" style="
                background-color: #28a745; color: white; width: 400px; padding: 20px; 
                text-align: center; text-decoration: none; font-size: 22px; font-weight: bold; 
                border-radius: 15px; text-transform: uppercase;">
                DÉBUTANT
            </a>
            <a href="/?action=Intermédiaire" target="_self" style="
                background-color: #ff8c00; color: white; width: 400px; padding: 20px; 
                text-align: center; text-decoration: none; font-size: 22px; font-weight: bold; 
                border-radius: 15px; text-transform: uppercase;">
                INTERMÉDIAIRE
            </a>
            <a href="/?action=Avancé" target="_self" style="
                background-color: #6f42c1; color: white; width: 400px; padding: 20px; 
                text-align: center; text-decoration: none; font-size: 22px; font-weight: bold; 
                border-radius: 15px; text-transform: uppercase;">
                AVANCÉ
            </a>
        </div>
    """, unsafe_allow_html=True)

# ÉTAPE 2 : COURS (STRUCTURE DE BASE)
elif st.session_state.etape == "cours":
    st.markdown(f"<h3 style='text-align: center;'>❤️ Vies : {st.session_state.vies} | ⭐ XP : {st.session_state.xp}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Niveau : {st.session_state.niveau}</h2>", unsafe_allow_html=True)
    
    if st.button("RETOUR AU MENU"):
        st.session_state.etape = "presentation"
        st.rerun()
