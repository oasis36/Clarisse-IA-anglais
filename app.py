import streamlit as st
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #004a99; color: white; font-weight: bold; }
    h1 { color: #004a99; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALISATION DES ÉTATS ---
if 'etape' not in st.session_state: st.session_state.etape = "presentation"
if 'niveau' not in st.session_state: st.session_state.niveau = "Débutant"
if 'leçon_index' not in st.session_state: st.session_state.leçon_index = 0
if 'erreurs' not in st.session_state: st.session_state.erreurs = []
if 'last_audio_key' not in st.session_state: st.session_state.last_audio_key = ""

# --- 3. PROGRAMME PÉDAGOGIQUE COMPLET ---
PROGRAMME = {
    "Débutant": [
        {"titre": "Le Verbe ÊTRE", "regle": "I am, You are, He/She/It is, We are, You are, They are.", "ex": "I am happy (Je suis heureux). You are a student (Tu es étudiant).", "test": "Traduis : 'Elle est heureuse'", "rep": "she is happy"},
        {"titre": "Le Verbe AVOIR", "regle": "Possession : I have got, You have got, He/She has got.", "ex": "I have got a car (J'ai une voiture). He has got a cat (Il a un chat).", "test": "Traduis : 'J'ai un chien'", "rep": "i have got a dog"},
        {"titre": "Le Présent Simple", "regle": "Ajoutez un 's' à la 3ème personne (He, She, It).", "ex": "I play tennis. He plays football.", "test": "Traduis : 'Il travaille'", "rep": "he works"},
        {"titre": "Les Articles", "regle": "'A' (consonne), 'An' (voyelle), 'The' (défini).", "ex": "A book, An apple, The sun.", "test": "Comment dit-on 'Une orange' ?", "rep": "an orange"},
        {"titre": "Les Pluriels", "regle": "En général, on ajoute un 's'.", "ex": "One dog, two dogs. One car, three cars.", "test": "Pluriel de 'Book' ?", "rep": "books"}
    ],
    "Intermédiaire": [
        {"titre": "Le Present Continuous", "regle": "Action en cours : BE + Verbe-ING.", "ex": "I am eating (Je suis en train de manger).", "test": "Traduis : 'Il est en train de dormir' (sleep)", "rep": "he is sleeping"},
        {"titre": "Le Past Simple", "regle": "Actions terminées. Verbes réguliers en -ED.", "ex": "I watched a movie (J'ai regardé un film).", "test": "Traduis : 'J'ai travaillé'", "rep": "i worked"},
        {"titre": "Le Present Perfect", "regle": "Lien passé/présent : HAVE + Participe Passé.", "ex": "I have lost my keys (J'ai perdu mes clés).", "test": "Traduis : 'J'ai vu' (seen)", "rep": "i have seen"},
        {"titre": "Les Comparatifs", "regle": "Adjectif court + ER + THAN.", "ex": "The car is faster than the bike.", "test": "Traduis : 'Plus grand que' (Tall)", "rep": "taller than"},
        {"titre": "Le Futur (Will)", "regle": "Décision ou prédiction : WILL + Verbe.", "ex": "It will rain tomorrow.", "test": "Traduis : 'Je viendrai' (come)", "rep": "i will come"}
    ],
    "Avancé": [
        {"titre": "Le Conditionnel", "regle": "Hypothèse : IF + Past Simple -> WOULD + Verbe.", "ex": "If I won, I would travel.", "test": "Complète : If I were rich, I _ (buy) a boat.", "rep": "would buy"},
        {"titre": "Le Past Perfect", "regle": "Action avant une autre dans le passé : HAD + Participe Passé.", "ex": "I had already eaten when he arrived.", "test": "Traduis : 'J'avais fini' (finished)", "rep": "i had finished"},
        {"titre": "La Voix Passive", "regle": "BE + Participe Passé.", "ex": "The cake was eaten by the dog.", "test": "Traduis : 'La lettre a été écrite' (written)", "rep": "the letter was written"},
        {"titre": "Gerund vs Infinitive", "regle": "Certains verbes sont suivis de -ING (ex: enjoy, stop).", "ex": "I enjoy swimming. I want to go.", "test": "Complète : I stop _ (smoke).", "rep": "smoking"},
        {"titre": "Les Modaux (Deduction)", "regle": "Must (certitude), Might (possibilité).", "ex": "It must be true. It might rain.", "test": "Traduis : 'Cela doit être lui'", "rep": "it must be him"}
    ]
}

# --- 4. FONCTIONS AUDIO ---
def parler_sequence(annonce_fr, exemple_en, question_fr):
    ex_en = re.sub(r'\(.*?\)', '', exemple_en).replace("'", "\\'")
    ann_fr = annonce_fr.replace("'", "\\'")
    que_fr = question_fr.replace("'", "\\'")
    
    js = f"""
    <script>
    window.speechSynthesis.cancel();
    var m1 = new SpeechSynthesisUtterance('{ann_fr}'); m1.lang = 'fr-FR'; m1.rate = 0.9;
    var m2 = new SpeechSynthesisUtterance('{ex_en}'); m2.lang = 'en-US'; m2.rate = 0.8;
    var m3 = new SpeechSynthesisUtterance('{que_fr}'); m3.lang = 'fr-FR'; m3.rate = 0.9;
    m1.onend = function() {{ window.speechSynthesis.speak(m2); }};
    m2.onend = function() {{ window.speechSynthesis.speak(m3); }};
    window.speechSynthesis.speak(m1);
    </script>
    """
    st.components.v1.html(js, height=0)

def parler_simple(txt):
    js = f"<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{txt.replace("'", "\\'")}'); m.lang = 'fr-FR'; window.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 5. INTERFACE ---
if st.session_state.etape == "presentation":
    st.title("🎓 Clarisse - English Academy")
    intro = "Bonjour, je me présente, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage. Pour commencer notre programme, quel est ton niveau actuel ?"
    st.write(intro)
    if st.session_state.last_audio_key != "intro":
        parler_simple(intro)
        st.session_state.last_audio_key = "intro"
    
    c1, c2, c3 = st.columns(3)
    if c1.button("Débutant"): 
        st.session_state.niveau, st.session_state.etape = "Débutant", "cours"
        st.rerun()
    if c2.button("Intermédiaire"): 
        st.session_state.niveau, st.session_state.etape = "Intermédiaire", "cours"
        st.rerun()
    if c3.button("Avancé"): 
        st.session_state.niveau, st.session_state.etape = "Avancé", "cours"
        st.rerun()

elif st.session_state.etape == "cours":
    cours_actuel = PROGRAMME[st.session_state.niveau]
    
    if st.session_state.leçon_index < len(cours_actuel):
        leçon = cours_actuel[st.session_state.leçon_index]
        titre = f"Leçon {st.session_state.leçon_index + 1} : {leçon['titre']}"
        annonce = f"Leçon numéro {st.session_state.leçon_index + 1}. {leçon['titre']}."
        
        # Audio
        key = f"{st.session_state.niveau}_{st.session_state.leçon_index}"
        if st.session_state.last_audio_key != key:
            parler_sequence(annonce, leçon['ex'], leçon['test'])
            st.session_state.last_audio_key = key

        st.title(titre)
        st.info(f"*Grammaire :* {leçon['regle']}")
        st.write(f"*Exemples :* {leçon['ex']}")
        st.divider()
        
        with st.form(key='ex_form', clear_on_submit=True):
            st.subheader(leçon['test'])
            rep_user = st.text_input("Votre réponse :").lower().strip()
            if st.form_submit_button("Valider"):
                if rep_user == leçon['rep']:
                    st.success("C'est bien ! Félicitations.")
                    st.session_state.leçon_index += 1
                    st.rerun()
                else:
                    st.error(f"Mauvaise réponse. La correction est : {leçon['rep']}")
    else:
        st.balloons()
        st.success(f"Bravo ! Vous avez terminé le niveau {st.session_state.niveau}.")
        if st.button("Retour à l'accueil"):
            st.session_state.leçon_index = 0
            st.session_state.etape = "presentation"
            st.rerun()
