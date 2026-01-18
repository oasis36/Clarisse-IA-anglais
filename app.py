import streamlit as st

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓", layout="wide")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #004a99;
        color: white;
        font-weight: bold;
    }
    h1 { color: #004a99; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALISATION ---
if 'etape' not in st.session_state:
    st.session_state.etape = "presentation"
if 'leçon_index' not in st.session_state:
    st.session_state.leçon_index = 0
if 'niveau' not in st.session_state:
    st.session_state.niveau = "Débutant"
if 'last_leçon' not in st.session_state:
    st.session_state.last_leçon = -1

# --- 3. PROGRAMME COMPLET ---
PROGRAMME = {
    "Débutant": [
        {
            "titre": "Le Verbe ÊTRE (To BE)", 
            "regle": "I am (Je suis), You are (Tu es), He/She is (Il/Elle est).", 
            "ex": "I am Clarisse (Je suis Clarisse), She is happy (Elle est heureuse)", 
            "test": "Traduis 'Je suis' :", 
            "rep": "i am"
        },
        {
            "titre": "Le Verbe AVOIR (Have Got)", 
            "regle": "I have got (J'ai), You have got (Tu as), He/She has got (Il/Elle a).", 
            "ex": "I have got a book (J'ai un livre), He has got a car (Il a une voiture)", 
            "test": "Traduis 'J'ai' :", 
            "rep": "i have got"
        },
        {
            "titre": "Les Nombres (1 à 20)", 
            "regle": "1: One, 2: Two, 3: Three, 10: Ten, 11: Eleven, 12: Twelve, 20: Twenty.", 
            "ex": "Three cats (Trois chats), Ten apples (Dix pommes)", 
            "test": "Comment dit-on 'Huit' ?", 
            "rep": "eight"
        },
        {
            "titre": "Les Nombres (20 à 100)", 
            "regle": "30: Thirty, 40: Forty, 50: Fifty, 100: One hundred.", 
            "ex": "Forty-two (Quarante-deux), One hundred euros (Cent euros)", 
            "test": "Traduis 'Cinquante' :", 
            "rep": "fifty"
        }
    ],
    "Intermédiaire": [
        {"titre": "Present Perfect", "regle": "Have + Participe Passé.", "ex": "I have seen (J'ai vu), She has worked (Elle a travaillé)", "test": "Traduis 'J'ai vu' :", "rep": "i have seen"}
    ],
    "Avancé": [
        {"titre": "Conditionnel 3", "regle": "If + Past Perfect -> Would have + PP.", "ex": "If I had known (Si j'avais su), I would have stayed (Je serais resté)", "test": "If I _ (be) there.", "rep": "had been"}
    ]
}

# --- 4. FONCTION AUDIO AUTOMATIQUE ---
def parler_automatique(texte):
    # Nettoyage pour extraire tout l'anglais de la phrase (avant chaque parenthèse)
    import re
    phrase_anglaise = re.sub(r'\(.*?\)', '', texte).replace(',', '.')
    
    js = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{phrase_anglaise}');
    msg.lang = 'en-US';
    msg.rate = 0.9;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js, height=0)

# --- 5. INTERFACE ---
if st.session_state.etape == "presentation":
    st.title("🎓 Clarisse - English Academy")
    st.write("Bonjour, je me présente, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage. Quel est ton niveau actuel ?")
    c1, c2, c3 = st.columns(3)
    if c1.button("Débutant"): 
        st.session_state.niveau = "Débutant"
        st.session_state.etape = "cours"
        st.rerun()
    if c2.button("Intermédiaire"): 
        st.session_state.niveau = "Intermédiaire"
        st.session_state.etape = "cours"
        st.rerun()
    if c3.button("Avancé"): 
        st.session_state.niveau = "Avancé"
        st.session_state.etape = "cours"
        st.rerun()

elif st.session_state.etape == "cours":
    liste = PROGRAMME[st.session_state.niveau]
    leçon = liste[st.session_state.leçon_index]
    
    # Déclenchement automatique de la voix au chargement de la leçon
    if st.session_state.last_leçon != st.session_state.leçon_index:
        parler_automatique(leçon['ex'])
        st.session_state.last_leçon = st.session_state.leçon_index

    st.sidebar.title("💎 Espace Clarisse")
    st.sidebar.write(f"Niveau : *{st.session_state.niveau}*")
    st.sidebar.progress((st.session_state.leçon_index + 1) / len(liste))
    
    if st.sidebar.button("⏮️ Menu"):
        st.session_state.etape = "presentation"
        st.session_state.leçon_index = 0
        st.session_state.last_leçon = -1
        st.rerun()

    st.title(f"Leçon {st.session_state.leçon_index + 1} : {leçon['titre']}")
    st.info(f"*Règle :* {leçon['regle']}")
    st.write(f"*Exemples :* {leçon['ex']}")
    
    st.divider()
    st.subheader("📝 Exercice")
    st.write(leçon['test'])
    
    # Utilisation du formulaire pour que ENTER valide tout d'un coup
    with st.form(key='exercice_form', clear_on_submit=True):
        reponse = st.text_input("Ta réponse (Appuie sur ENTER pour valider) :").lower().strip()
        submit = st.form_submit_button("Valider")
        
        if submit:
            if reponse == leçon['rep']:
                st.success("✨ C'est bien !")
                if st.session_state.leçon_index < len(liste) - 1:
                    st.session_state.leçon_index += 1
                    st.rerun()
                else:
                    st.balloons()
                    st.success("Félicitations ! Niveau terminé.")
            else:
                st.error("Réessaie ! Clarisse va répéter l'exemple.")
                parler_automatique(leçon['ex'])
