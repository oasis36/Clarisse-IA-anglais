import streamlit as st
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓", layout="wide")

# --- 2. INITIALISATION DES ÉTATS ---
if 'etape' not in st.session_state: st.session_state.etape = "presentation"
if 'niveau' not in st.session_state: st.session_state.niveau = "Débutant"
if 'leçon_index' not in st.session_state: st.session_state.leçon_index = 0
if 'erreurs' not in st.session_state: st.session_state.erreurs = []
if 'mode_revision' not in st.session_state: st.session_state.mode_revision = False
if 'last_audio_key' not in st.session_state: st.session_state.last_audio_key = ""
if 'feedback_erreur' not in st.session_state: st.session_state.feedback_erreur = None

# --- 3. PROGRAMME PÉDAGOGIQUE ---
PROGRAMME = {
    "Débutant": [
        {"titre": "Se Présenter", "regle": "Utilisez 'My name is' pour le nom.", "ex": "My name is Clarisse.", "test": "Traduisez : 'Mon nom est Marc'", "rep": "my name is marc", "aide": "En anglais, on dit 'My name IS' (Mon nom EST)."},
        {"titre": "Le Verbe ÊTRE", "regle": "I am, You are, He/She/It is.", "ex": "She is a teacher.", "test": "Traduisez : 'Elle est professeur' (teacher)", "rep": "she is a teacher", "aide": "Pour 'Elle est', on utilise 'She is'."},
        {"titre": "Les Articles A/AN", "regle": "'A' (consonne), 'AN' (voyelle).", "ex": "A dog, An apple.", "test": "Comment dit-on 'Une pomme' ? (apple)", "rep": "an apple", "aide": "Utilisez 'an' car 'apple' commence par la voyelle 'a'."},
        {"titre": "Le Verbe AVOIR", "regle": "Possession : I have got, He/She has got.", "ex": "I have got a cat.", "test": "Traduisez : 'J'ai un chat' (a cat)", "rep": "i have got a cat", "aide": "La structure complète est 'I have got'."},
        {"titre": "Le Présent Simple", "regle": "Action habituelle. Ajoutez 's' au singulier.", "ex": "He works in London.", "test": "Traduisez : 'Il travaille' (work)", "rep": "he works", "aide": "N'oubliez pas le 's' à la fin de 'work' car le sujet est 'He'."}
    ],
    "Intermédiaire": [
        {"titre": "Le Présent Continu", "regle": "BE + Verbe-ING.", "ex": "I am eating.", "test": "Traduisez : 'Je suis en train de manger'", "rep": "i am eating", "aide": "Utilisez l'auxiliaire 'am' + le verbe avec 'ing'."}
    ],
    "Avancé": [
        {"titre": "Le Present Perfect", "regle": "HAVE + Participe passé.", "ex": "I have lost my keys.", "test": "Traduisez : 'J'ai perdu mes clés' (lost my keys)", "rep": "i have lost my keys", "aide": "L'auxiliaire 'have' est obligatoire ici."}
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
if st.session_state.etape == "presentation":
    st.title("🎓 Clarisse - English Academy")
    intro = "Bonjour, je me présente, je m'appelle Clarisse. Choisissez votre niveau :"
    st.write(intro)
    if st.session_state.last_audio_key != "intro":
        parler_simple(intro)
        st.session_state.last_audio_key = "intro"
    
    c1, c2, c3 = st.columns(3)
    if c1.button("Débutant"):
