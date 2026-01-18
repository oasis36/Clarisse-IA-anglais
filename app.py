import streamlit as st

# --- CONFIGURATION INITIALE ---
if 'etape' not in st.session_state:
    st.session_state.etape = "presentation"
if 'leçon_index' not in st.session_state:
    st.session_state.leçon_index = 0
if 'niveau' not in st.session_state:
    st.session_state.niveau = "Débutant"

# --- BASE DE DONNÉES (Échantillon du Programme de 60 leçons) ---
PROGRAMME = {
    "Débutant": [
        {"titre": "L'Alphabet & Phonétique", "regle": "A [eɪ], E [iː], G [dʒ], J [dʒeɪ].", "ex": "Apple, Book, Cat", "test": "Épelle 'CAT' (minuscules) :", "rep": "cat"},
        {"titre": "L'auxiliaire BE", "regle": "I am, You are, He/She/It is...", "ex": "I am happy, She is a doctor", "test": "Complète : 'They _ students.'", "rep": "are"},
        {"titre": "HAVE GOT", "regle": "I have got, He has got...", "ex": "I have got a car", "test": "He _ got a dog.", "rep": "has"}
    ],
    "Intermédiaire": [
        {"titre": "Present Perfect", "regle": "Have + Participe Passé.", "ex": "I have seen this movie", "test": "She _ (finish) her work", "rep": "has finished"}
    ],
    "Avancé": [
        {"titre": "Conditionnel Type 3", "regle": "If + Past Perfect -> Would have + PP.", "ex": "If I had known...", "test": "If he _ (be) there, he would have helped.", "rep": "had been"}
    ]
}

# --- FONCTION DE SYNTHÈSE VOCALE ---
def parler(texte):
    js = f"const msg = new SpeechSynthesisUtterance('{texte}'); msg.lang = 'en-US'; window.speechSynthesis.speak(msg);"
    st.components.v1.html(f"<script>{js}</script>", height=0)

# --- LOGIQUE D'AFFICHAGE ---

# 1. Présentation de Clarisse (selon tes consignes)
if st.session_state.etape == "presentation":
    st.title("🤖 Rencontre avec Clarisse")
    st.write("Bonjour, je me présente, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage. Pour commencer notre programme, quel est ton niveau actuel ?")
    
    col1, col2, col3 = st.columns(3)
    if col1.button("Débutant"):
        st.session_state.niveau = "Débutant"
        st.session_state.etape = "cours"
        st.rerun()
    if col2.button("Intermédiaire"):
        st.session_state.niveau = "Intermédiaire"
        st.session_state.etape = "cours"
        st.rerun()
    if col3.button("Avancé"):
        st.session_state.niveau = "Avancé"
        st.session_state.etape = "cours"
        st.rerun()

# 2. Interface de Cours
elif st.session_state.etape == "cours":
    leçons_du_niveau = PROGRAMME[st.session_state.niveau]
    leçon = leçons_du_niveau[st.session_state.leçon_index]

    st.sidebar.title("📌 Progression")
    st.sidebar.write(f"Niveau : {st.session_state.niveau}")
    st.sidebar.write(f"Leçon : {st.session_state.leçon_index + 1} / {len(leçons_du_niveau)}")
    
    if st.sidebar.button("🔄 Changer de niveau"):
        st.session_state.etape = "presentation"
        st.session_state.leçon_index = 0
        st.rerun()

    st.title(f"Leçon {st.session_state.leçon_index + 1} : {leçon['titre']}")
    
    with st.expander("📖 Voir la règle de grammaire", expanded=True):
        st.info(leçon['regle'])
    
    st.subheader("🔊 Écoute et Prononciation")
    st.write(f"Exemple : *{leçon['ex']}*")
    if st.button("Écouter Clarisse"):
        parler(leçon['ex'])

    st.divider()

    st.subheader("✍️ Exercice Écrit")
    st.write(leçon['test'])
    reponse_u = st.text_input("Ta réponse :", key=f"input_{st.session_state.leçon_index}").lower().strip()

    if st.button("Valider la leçon"):
        if reponse_u == leçon['rep']:
            st.success("C'est bien.")
            if st.session_state.leçon_index < len(leçons_du_niveau) - 1:
                st.session_state.leçon_index += 1
                st.rerun()
            else:
                st.balloons()
                st.success("Félicitations ! Tu as terminé ce niveau. Un peu d'humour : Pourquoi les oiseaux volent-ils vers le sud ? Parce que c'est trop loin pour y aller à pied !")
        else:
            st.error(f"Non, la réponse était : {leçon['rep']}. Réessaie !")

    # Bouton retour
    if st.session_state.leçon_index > 0:
        if st.button("⬅️ Leçon précédente"):
            st.session_state.leçon_index -= 1
            st.rerun()
