import streamlit as st
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓", layout="wide")

# Style CSS pour des barres de boutons entièrement colorées
st.markdown("""
    <style>
    /* Style de base pour les boutons de niveau */
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
    /* Couleur Débutant : Bleu */
    div.stButton > button:nth-child(1) { background-color: #007bff !important; }
    /* Couleur Intermédiaire : Orange */
    div.stButton > button:nth-child(2) { background-color: #ff8c00 !important; }
    /* Couleur Avancé : Vert */
    div.stButton > button:nth-child(3) { background-color: #28a745 !important; }
    
    .stButton > button:hover { opacity: 0.8; }
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
if 'feedback_erreur' not in st.session_state: st.session_state.feedback_erreur = None

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
def parler_sequence(ann, ex, que):
    ex_clean = re.sub(r'\(.*?\)', '', ex).replace("'", "\\'")
    js = f"""<script>
    window.speechSynthesis.cancel();
    var m1 = new SpeechSynthesisUtterance('{ann.replace("'", "\\'")}'); m1.lang = 'fr-FR';
    var m2 = new SpeechSynthesisUtterance('{ex_clean}'); m2.lang = 'en-US';
    var m3 = new SpeechSynthesisUtterance('{que.replace("'", "\\'")}'); m3.lang = 'fr-FR';
    m1.onend = function() {{ window.speechSynthesis.speak(m2); }};
    m2.onend = function() {{ window.speechSynthesis.speak(m3); }};
    window.speechSynthesis.speak(m1);
    </script>"""
    st.components.v1.html(js, height=0)

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
    
    # Boutons verticaux avec couleurs pleines
    if st.button("DÉBUTANT", use_container_width=True):
        st.session_state.update({"niveau": "Débutant", "etape": "cours", "leçon_index": 0, "erreurs": [], "vies": 5})
        st.rerun()
    if st.button("INTERMÉDIAIRE", use_container_width=True):
        st.session_state.update({"niveau": "Intermédiaire", "etape": "cours", "leçon_index": 0, "erreurs": [], "vies": 5})
        st.rerun()
    if st.button("AVANCÉ", use_container_width=True):
        st.session_state.update({"niveau": "Avancé", "etape": "cours", "leçon_index": 0, "erreurs": [], "vies": 5})
        st.rerun()

elif st.session_state.etape == "cours":
    liste = PROGRAMME[st.session_state.niveau]
    
    with st.sidebar:
        st.write(f"### ❤️ Vies : {'❤️' * st.session_state.vies}")
        st.write(f"⭐ XP : {st.session_state.xp}")
        if st.button("Quitter"):
            st.session_state.etape = "presentation"
            st.rerun()

    if not st.session_state.mode_revision:
        if st.session_state.leçon_index < len(liste):
            leçon = liste[st.session_state.leçon_index]
            st.progress(st.session_state.leçon_index / len(liste))
            titre = f"Leçon {st.session_state.leçon_index + 1}"
        else:
            if st.session_state.erreurs:
                st.session_state.mode_revision = True
                st.rerun()
            else:
                st.session_state.etape = "fin"
                st.rerun()
    else:
        if st.session_state.erreurs:
            leçon = st.session_state.erreurs[0]
            st.warning("🔄 SESSION DE RÉVISION")
            titre = "Rattrapage"
        else:
            st.session_state.etape = "fin"
            st.rerun()

    key = f"{st.session_state.niveau}_{st.session_state.leçon_index}_{st.session_state.mode_revision}"
    if st.session_state.last_audio_key != key:
        parler_sequence(f"{titre}. {leçon['titre']}", leçon['ex'], leçon['test'])
        st.session_state.last_audio_key = key

    st.title(f"{leçon['titre']}")
    st.info(f"*Règle :* {leçon['regle']}")
    
    if st.session_state.feedback_erreur:
        st.error(f"❌ La correction était : *{leçon['rep']}*")
        st.warning(f"💡 {st.session_state.feedback_erreur}")
        if st.button("Continuer"):
            st.session_state.feedback_erreur = None
            if st.session_state.mode_revision:
                st.session_state.erreurs.append(st.session_state.erreurs.pop(0))
            else:
                st.session_state.leçon_index += 1
            st.rerun()
    else:
        with st.form(key='form', clear_on_submit=True):
            st.subheader(leçon['test'])
            rep = st.text_input("Réponse :").lower().strip()
            if st.form_submit_button("Vérifier"):
                if rep == leçon['rep']:
                    st.success("✨ Correct !")
                    st.session_state.xp += 10
                    if st.session_state.mode_revision:
                        st.session_state.erreurs.pop(0)
                    else:
                        st.session_state.leçon_index += 1
                    st.rerun()
                else:
                    st.session_state.vies -= 1
                    st.session_state.feedback_erreur = leçon['aide']
                    if leçon not in st.session_state.erreurs:
                        st.session_state.erreurs.append(leçon)
                    st.rerun()

elif st.session_state.etape == "fin":
    st.balloons()
    st.success("Niveau terminé !")
    if st.button("Retour au menu"):
        st.session_state.update({"etape": "presentation", "leçon_index": 0, "erreurs": [], "mode_revision": False})
        st.rerun()
