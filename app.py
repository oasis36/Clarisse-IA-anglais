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

# --- 2. INITIALISATION ---
if 'etape' not in st.session_state: st.session_state.etape = "presentation"
if 'niveau' not in st.session_state: st.session_state.niveau = "Débutant"
if 'leçon_index' not in st.session_state: st.session_state.leçon_index = 0
if 'last_audio_key' not in st.session_state: st.session_state.last_audio_key = ""

# --- 3. PROGRAMME PÉDAGOGIQUE COMPLET ---
PROGRAMME = {
    "Débutant": [
        {"titre": "Se Présenter", "regle": "Utilisez 'My name is' pour le nom et 'I am' pour l'âge ou l'état.", "ex": "My name is Clarisse. I am happy to meet you.", "test": "Traduisez : 'Mon nom est Marc'", "rep": "my name is marc"},
        {"titre": "Le Verbe ÊTRE (To Be)", "regle": "I am, You are, He/She/It is. Utile pour décrire une personne.", "ex": "She is a teacher. They are students.", "test": "Traduisez : 'Elle est professeur' (teacher)", "rep": "she is a teacher"},
        {"titre": "Les Articles A/AN", "regle": "'A' devant une consonne, 'AN' devant une voyelle.", "ex": "A dog, An orange, An apple.", "test": "Comment dit-on 'Une pomme' ? (apple)", "rep": "an apple"},
        {"titre": "Le Verbe AVOIR (Have Got)", "regle": "I have got, You have got, He/She has got.", "ex": "I have got a blue car. He has got a big house.", "test": "Traduisez : 'J'ai une voiture' (a car)", "rep": "i have got a car"},
        {"titre": "Le Présent Simple", "regle": "Exprime une habitude. Attention au 'S' à la 3ème personne.", "ex": "I work in Paris. He works in London.", "test": "Traduisez : 'Il travaille' (work)", "rep": "he works"}
    ],
    "Intermédiaire": [
        {"titre": "Le Présent Continu", "regle": "Action en cours : BE + Verbe-ING.", "ex": "I am eating a pizza. Look! It is raining.", "test": "Traduisez : 'Je suis en train de manger'", "rep": "i am eating"},
        {"titre": "Le Passé Simple (ED)", "regle": "Pour une action terminée. Verbes réguliers + ED.", "ex": "Yesterday, I played tennis. She visited London.", "test": "Traduisez : 'J'ai joué au tennis' (played tennis)", "rep": "i played tennis"},
        {"titre": "Le Comparatif", "regle": "Adjectif court + ER + THAN.", "ex": "The cat is smaller than the dog.", "test": "Traduisez : 'Plus petit que' (smaller than)", "rep": "smaller than"},
        {"titre": "Le Futur avec WILL", "regle": "Pour une décision ou prédiction. WILL + Verbe.", "ex": "I think it will rain tomorrow.", "test": "Traduisez : 'Il pleuvra' (rain)", "rep": "it will rain"},
        {"titre": "Les Adverbes de Fréquence", "regle": "S'installent avant le verbe (Always, Never, Often).", "ex": "I always drink coffee. She never smokes.", "test": "Traduisez : 'Je bois toujours' (always drink)", "rep": "i always drink"}
    ],
    "Avancé": [
        {"titre": "Le Present Perfect", "regle": "Lien entre passé et présent. HAVE + Participe passé.", "ex": "I have lost my keys. She has lived here for ten years.", "test": "Traduisez : 'J'ai perdu mes clés' (lost my keys)", "rep": "i have lost my keys"},
        {"titre": "Le Conditionnel Type 2", "regle": "Hypothèse imaginaire : IF + Prétérit, WOULD + Verbe.", "ex": "If I were rich, I would buy a boat.", "test": "Traduisez : 'Si j'étais riche' (If I were rich)", "rep": "if i were rich"},
        {"titre": "La Voix Passive", "regle": "Mise en avant de l'objet. BE + Participe passé.", "ex": "The book was written in 1920.", "test": "Traduisez : 'Le livre a été écrit' (The book was written)", "rep": "the book was written"},
        {"titre": "Le Discours Indirect", "regle": "Rapporter des paroles. Le présent devient passé.", "ex": "She said: 'I am tired' devient She said she was tired.", "test": "Traduisez : 'Elle a dit qu'elle était fatiguée'", "rep": "she said she was tired"},
        {"titre": "Les Modaux de Déduction", "regle": "Must (certitude), Might (possibilité).", "ex": "It must be true. He might come later.", "test": "Traduisez : 'Cela doit être vrai' (must be true)", "rep": "it must be true"}
    ]
}

# --- 4. FONCTIONS AUDIO ---
def parler_sequence(annonce_fr, exemple_en, question_fr):
    ex_en = re.sub(r'\(.*?\)', '', exemple_en).replace("'", "\\'")
    ann_fr = annonce_fr.replace("'", "\\'")
    que_fr = question_fr.replace("'", "\\'")
    js = f"""<script>
    window.speechSynthesis.cancel();
    var m1 = new SpeechSynthesisUtterance('{ann_fr}'); m1.lang = 'fr-FR'; m1.rate = 0.9;
    var m2 = new SpeechSynthesisUtterance('{ex_en}'); m2.lang = 'en-US'; m2.rate = 0.8;
    var m3 = new SpeechSynthesisUtterance('{que_fr}'); m3.lang = 'fr-FR'; m3.rate = 0.9;
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
        annonce = f"Leçon numéro {st.session_state.leçon_index + 1}. {leçon['titre']}."
        
        # Gestion Audio
        key = f"{st.session_state.niveau}_{st.session_state.leçon_index}"
        if st.session_state.last_audio_key != key:
            parler_sequence(annonce, leçon['ex'], leçon['test'])
            st.session_state.last_audio_key = key

        st.title(f"Leçon {st.session_state.leçon_index + 1} : {leçon['titre']}")
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
        st.success(f"Bravo ! Niveau {st.session_state.niveau} terminé.")
        if st.button("Retour à l'accueil"):
            st.session_state.leçon_index = 0
            st.session_state.etape = "presentation"
            st.rerun()
