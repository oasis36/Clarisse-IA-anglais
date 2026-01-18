import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓")

if 'etape' not in st.session_state:
    st.session_state.etape = "presentation"
if 'leçon_index' not in st.session_state:
    st.session_state.leçon_index = 0
if 'niveau' not in st.session_state:
    st.session_state.niveau = "Débutant"

# --- PROGRAMME AVEC DÉFINITIONS DÉTAILLÉES ---
PROGRAMME = {
    "Débutant": [
        {
            "titre": "L'Alphabet et Vocabulaire de base",
            "regle": "A [eɪ], E [iː], G [dʒ], J [dʒeɪ]. Définitions : Boy = Garçon, Girl = Fille, Teacher = Professeur.",
            "ex": "A boy (Un garçon), A girl (Une fille), A teacher (Un professeur)",
            "test": "Traduis le mot 'Fille' en anglais :",
            "rep": "girl"
        },
        {"titre": "BE au Présent", "regle": "I am (Je suis), You are (Tu es), He/She is (Il/Elle est).", "ex": "I am a boy (Je suis un garçon), She is a girl (Elle est une fille)", "test": "Traduis 'Je suis' :", "rep": "i am"},
        {"titre": "HAVE GOT", "regle": "I have got (J'ai), You have got (Tu as).", "ex": "I have got a book (J'ai un livre)", "test": "Traduis 'J'ai' :", "rep": "i have got"},
        # ... (Le reste du programme de 60 leçons suit cette logique de définition claire)
    ],
    "Intermédiaire": [
        {"titre": "Present Perfect", "regle": "Lien passé/présent. Have + Participe Passé.", "ex": "I have seen (J'ai vu)", "test": "Traduis 'J'ai vu' :", "rep": "i have seen"}
    ],
    "Avancé": [
        {"titre": "Conditionnel 3", "regle": "Regrets. If + Past Perfect -> Would have + PP.", "ex": "If I had known (Si j'avais su)", "test": "Complète: If I _ known.", "rep": "had"}
    ]
}

# --- FONCTION AUDIO ---
def parler(texte_complet):
    segments = texte_complet.split(',')
    a_lire = ""
    for s in segments:
        anglais = s.split('(')[0].strip()
        a_lire += anglais + ". "
    js_code = f"const synth = window.speechSynthesis; const utter = new SpeechSynthesisUtterance('{a_lire}'); utter.lang = 'en-US'; synth.speak(utter);"
    st.components.v1.html(f"<script>{js_code}</script>", height=0)

# --- INTERFACE ---
if st.session_state.etape == "presentation":
    st.title("🤖 Clarisse - English Academy")
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
    
    st.sidebar.title("Menu Clarisse")
    st.sidebar.write(f"Niveau : *{st.session_state.niveau}*")
    
    if st.sidebar.button("🔄 Changer de niveau"):
        st.session_state.etape, st.session_state.leçon_index = "presentation", 0
        st.rerun()

    st.title(f"Leçon {st.session_state.leçon_index + 1} : {leçon['titre']}")
    st.info(f"*Règle et Définitions :* {leçon['regle']}")
    st.write(f"*Exemples :* {leçon['ex']}")
    if st.button("Prononciation 🔊"): parler(leçon['ex'])
    
    st.divider()
    st.subheader("Exercice")
    st.write(leçon['test'])
    ans = st.text_input("Réponse :", key=f"ans_{st.session_state.leçon_index}").lower().strip()
    
    if st.button("Valider"):
        if ans == leçon['rep']:
            st.success("C'est bien.")
            if st.session_state.leçon_index < len(liste) - 1:
                st.session_state.leçon_index += 1
                st.rerun()
            else:
                st.balloons()
                st.success("Niveau terminé !")
        else:
            st.error("Réessaie !")
