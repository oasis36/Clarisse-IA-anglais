import streamlit as st

# --- 1. CONFIGURATION ET STYLE ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓", layout="wide")

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

# --- 3. PROGRAMME RESTRUCTURÉ (60 LEÇONS) ---
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
        {"titre": "Present Perfect", "regle": "Have + Participe Passé.", "ex": "I have seen (J'ai vu)", "test": "Traduis 'J'ai vu' :", "rep": "i have seen"}
    ],
    "Avancé": [
        {"titre": "Conditionnel 3", "regle": "If + Past Perfect -> Would have + PP.", "ex": "If I had known (Si j'avais su)", "test": "If I _ (be) there.", "rep": "had been"}
    ]
}

# --- 4. FONCTIONS AUDIO ---
def parler(texte):
    # On extrait l'anglais avant la parenthèse
    anglais = texte.split('(')[0].strip()
    js = f"const synth = window.speechSynthesis; const utter = new SpeechSynthesisUtterance('{anglais}'); utter.lang = 'en-US'; synth.speak(utter);"
    st.components.v1.html(f"<script>{js}</script>", height=0)

# --- 5. INTERFACE ---
if st.session_state.etape == "presentation":
    st.title("🎓 Clarisse - English Academy")
    st.write("Bonjour, je me présente, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage. Quel est ton niveau actuel ?")
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
    liste = PROGRAMME[st.session_state.niveau]
    leçon = liste[st.session_state.leçon_index]
    
    st.sidebar.title("💎 Espace Clarisse")
    st.sidebar.write(f"Niveau : *{st.session_state.niveau}*")
    st.sidebar.progress((st.session_state.leçon_index + 1) / len(liste))
    
    if st.sidebar.button("⏮️ Menu"):
        st.session_state.etape, st.session_state.leçon_index = "presentation", 0
        st.rerun()

    st.title(f"Leçon {st.session_state.leçon_index + 1} : {leçon['titre']}")
    st.info(f"*Règle :* {leçon['regle']}")
    st.write(f"*Exemple :* {leçon['ex']}")
    if st.button("Prononciation 🔊"): 
        parler(leçon['ex'])
    
    st.divider()
    st.subheader("📝 Exercice")
    st.write(leçon['test'])
    reponse = st.text_input("Ta réponse :", key=f"ans_{st.session_state.leçon_index}").lower().strip()
    
    if st.button("Valider"):
        if reponse == leçon['rep']:
            st.success("✨ C'est bien !")
            if st.session_state.leçon_index < len(liste) - 1:
                st.session_state.leçon_index += 1
                st.rerun()
            else:
                st.balloons()
                st.success("Félicitations ! Niveau terminé.")
        else:
            st.error("Réessaie !")
Envoyé
Écrire à
