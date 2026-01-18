import streamlit as st
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓", layout="wide")

# --- 2. INITIALISATION DES ÉTATS ---
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
        {"titre": "Se Présenter", "regle": "Utilisez 'My name is' pour le nom.", "ex": "My name is Clarisse.", "test": "Traduisez : 'Mon nom est Marc'", "rep": "my name is marc", "aide": "En anglais, on dit 'My name IS'."},
        {"titre": "Le Verbe ÊTRE", "regle": "I am, You are, He/She/It is.", "ex": "She is a teacher.", "test": "Traduisez : 'Elle est professeur' (teacher)", "rep": "she is a teacher", "aide": "Pour 'Elle est', on utilise 'She is'."},
        {"titre": "Les Articles A/AN", "regle": "'A' (consonne), 'AN' (voyelle).", "ex": "A dog, An apple.", "test": "Comment dit-on 'Une pomme' ? (apple)", "rep": "an apple", "aide": "Utilisez 'an' car 'apple' commence par une voyelle."},
        {"titre": "Le Verbe AVOIR", "regle": "Possession : I have got.", "ex": "I have got a cat.", "test": "Traduisez : 'J'ai un chat' (a cat)", "rep": "i have got a cat", "aide": "La structure est 'I have got'."},
        {"titre": "Le Présent Simple", "regle": "Ajoutez 's' à la 3ème personne.", "ex": "He works in London.", "test": "Traduisez : 'Il travaille' (work)", "rep": "he works", "aide": "N'oubliez pas le 's' avec 'He'."}
    ],
    "Intermédiaire": [
        {"titre": "Le Présent Continu", "regle": "BE + Verbe-ING.", "ex": "I am eating.", "test": "Traduisez : 'Je suis en train de manger'", "rep": "i am eating", "aide": "Utilisez 'am' + 'verbe-ing'."}
    ],
    "Avancé": [
        {"titre": "Le Present Perfect", "regle": "HAVE + Participe passé.", "ex": "I have lost my keys.", "test": "Traduisez : 'J'ai perdu mes clés' (lost my keys)", "rep": "i have lost my keys", "aide": "Utilisez l'auxiliaire 'have'."}
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

# ÉTAPE 0 : PAGE DÉMARRER
if st.session_state.etape == "start_page":
    st.title("🎓 Clarisse English Academy")
    st.write("### Bienvenue dans votre nouvel espace d'apprentissage.")
    if st.button("DÉMARRER", use_container_width=True):
        st.session_state.etape = "presentation"
        st.rerun()

# ÉTAPE 1 : PRÉSENTATION CLARISSE
elif st.session_state.etape == "presentation":
    st.title("🎓 Clarisse English Academy")
    intro = "Bonjour, je me présente, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage. Pour commencer notre programme, quel est ton niveau actuel ?"
    st.write(intro)
    
    if st.session_state.last_audio_key != "intro":
        parler_simple(intro)
        st.session_state.last_audio_key = "intro"
    
    c1, c2, c3 = st.columns(3)
    if c1.button("Débutant"): 
        st.session_state.update({"niveau": "Débutant", "etape": "cours", "leçon_index": 0, "erreurs": [], "vies": 5, "xp": 0})
        st.rerun()
    if c2.button("Intermédiaire"): 
        st.session_state.update({"niveau": "Intermédiaire", "etape": "cours", "leçon_index": 0, "erreurs": [], "vies": 5, "xp": 0})
        st.rerun()
    if c3.button("Avancé"): 
        st.session_state.update({"niveau": "Avancé", "etape": "cours", "leçon_index": 0, "erreurs": [], "vies": 5, "xp": 0})
        st.rerun()

# ÉTAPE 2 : LE COURS (STYLE DUOLINGO)
elif st.session_state.etape == "cours":
    liste = PROGRAMME[st.session_state.niveau]
    
    with st.sidebar:
        st.write(f"### 👤 Profil")
        st.write(f"❤️ Vies : {'❤️' * st.session_state.vies}")
        st.write(f"⭐ XP : {st.session_state.xp}")
        if st.button("Quitter la session"):
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
        st.error(f"Correction : *{leçon['rep']}*")
        st.info(f"💡 {st.session_state.feedback_erreur}")
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
                    st.success("Correct !")
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
                    if st.session_state.vies <= 0:
                        st.error("Plus de vies ! Recommence le niveau.")
                        st.session_state.update({"leçon_index": 0, "vies": 5, "erreurs": []})
                    st.rerun()

# ÉTAPE 3 : FIN DE NIVEAU
elif st.session_state.etape == "fin":
    st.balloons()
    st.success(f"Niveau {st.session_state.niveau} terminé !")
    st.write(f"Score total : {st.session_state.xp} XP")
    if st.button("Menu principal"):
        st.session_state.update({"etape": "presentation", "leçon_index": 0, "erreurs": [], "mode_revision": False})
        st.rerun()
