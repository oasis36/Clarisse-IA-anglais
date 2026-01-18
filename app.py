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
if 'erreurs' not in st.session_state: st.session_state.erreurs = []
if 'mode_revision' not in st.session_state: st.session_state.mode_revision = False
if 'last_audio_key' not in st.session_state: st.session_state.last_audio_key = ""

# --- 3. PROGRAMME COMPLET ---
PROGRAMME = {
    "Débutant": [
        {
            "titre": "Le Verbe ÊTRE (To BE)", 
            "regle": "I am (Je suis), You are (Tu es), He/She is (Il/Elle est).", 
            "ex": "I am Clarisse (Je suis Clarisse), She is happy (Elle est heureuse)", 
            "test": "Comment dit-on 'Je suis' en anglais ?", 
            "rep": "i am"
        },
        {
            "titre": "Le Verbe AVOIR (Have Got)", 
            "regle": "I have got (J'ai), You have got (Tu as), He/She has got (Il/Elle a).", 
            "ex": "I have got a book (J'ai un livre), He has got a car (Il a une voiture)", 
            "test": "Comment dit-on 'J'ai' en anglais ?", 
            "rep": "i have got"
        },
        {
            "titre": "Les Nombres (1 à 20)", 
            "regle": "One (1), Two (2), Three (3), Eight (😎, Ten (10).", 
            "ex": "Three cats (Trois chats), Eight apples (Huit pommes)", 
            "test": "Comment dit-on 'Huit' en anglais ?", 
            "rep": "eight"
        }
    ],
    "Intermédiaire": [
        {"titre": "Present Perfect", "regle": "Have + Participe Passé.", "ex": "I have seen (J'ai vu)", "test": "Traduis 'J'ai vu' :", "rep": "i have seen"}
    ],
    "Avancé": [
        {"titre": "Conditionnel 3", "regle": "If + Past Perfect.", "ex": "If I had known (Si j'avais su)", "test": "Complète : If I _ (be) there.", "rep": "had been"}
    ]
}

# --- 4. FONCTION AUDIO ---
def parler(texte):
    # Nettoie le texte pour ne lire que l'anglais (enlève ce qui est entre parenthèses)
    phrase = re.sub(r'\(.*?\)', '', texte).replace(',', '.')
    js = f"""
    <script>
    window.speechSynthesis.cancel();
    var m = new SpeechSynthesisUtterance('{phrase}');
    m.lang = 'en-US';
    m.rate = 0.9;
    window.speechSynthesis.speak(m);
    </script>
    """
    st.components.v1.html(js, height=0)

# --- 5. INTERFACE ---
if st.session_state.etape == "presentation":
    st.title("🎓 Clarisse - English Academy")
    st.write("Bonjour, je me présente, je m'appelle Clarisse. Choisissez votre niveau :")
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
    liste_base = PROGRAMME[st.session_state.niveau]
    
    if not st.session_state.mode_revision:
        leçon = liste_base[st.session_state.leçon_index]
        titre_page = f"Leçon {st.session_state.leçon_index + 1} : {leçon['titre']}"
    else:
        leçon = st.session_state.erreurs[0]
        titre_page = f"Révision : {leçon['titre']}"

    # Audio Automatique
    audio_key = f"{st.session_state.niveau}_{st.session_state.leçon_index}_{st.session_state.mode_revision}"
    if st.session_state.last_audio_key != audio_key:
        parler(leçon['ex'])
        st.session_state.last_audio_key = audio_key

    st.title(titre_page)
    st.info(f"*Règle :* {leçon['regle']}")
    st.write(f"*Exemples :* {leçon['ex']}")
    
    st.divider()
    st.subheader("📝 Exercice")
    st.write(f"👉 *Question :* {leçon['test']}")
    
    with st.form(key='exercice_form', clear_on_submit=True):
        reponse = st.text_input("Ta réponse (ENTER pour valider) :").lower().strip()
        submit = st.form_submit_button("Valider")
        
        if submit:
            if reponse == leçon['rep']:
                st.success("✨ C'est bien !")
                if st.session_state.mode_revision:
                    st.session_state.erreurs.pop(0)
                else:
                    st.session_state.leçon_index += 1
            else:
                st.error(f"❌ Mauvaise réponse. La bonne était : '{leçon['rep']}'")
                parler(f"The correct answer is {leçon['rep']}")
                if leçon not in st.session_state.erreurs:
                    st.session_state.erreurs.append(leçon)
                if not st.session_state.mode_revision:
                    st.session_state.leçon_index += 1

            # Fin de cycle
            if not st.session_state.mode_revision and st.session_state.leçon_index >= len(liste_base):
                if st.session_state.erreurs:
                    st.session_state.mode_revision = True
                else:
                    st.balloons()
                    st.session_state.etape = "presentation"
            
            if st.session_state.mode_revision and not st.session_state.erreurs:
                st.balloons()
                st.session_state.etape = "presentation"
                st.session_state.mode_revision = False
                st.session_state.leçon_index = 0
            
            st.rerun()

    if st.button("⏮️ Menu"):
        st.session_state.etape = "presentation"
        st.session_state.leçon_index = 0
        st.rerun()
