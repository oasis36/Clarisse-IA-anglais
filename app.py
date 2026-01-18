import streamlit as st

# --- INITIALISATION DE LA SESSION ---
if 'etape' not in st.session_state:
    st.session_state.etape = "presentation"
if 'leçon_index' not in st.session_state:
    st.session_state.leçon_index = 0
if 'niveau' not in st.session_state:
    st.session_state.niveau = "Débutant"

# --- PROGRAMME COMPLET (Leçons 1 à 60) ---
PROGRAMME = {
    "Débutant": [
        {"titre": "L'Alphabet", "regle": "A [eɪ], E [iː], G [dʒ], J [dʒeɪ].", "ex": "Apple (Pomme), Book (Livre), Cat (Chat)", "test": "Épelle 'cat' :", "rep": "cat"},
        {"titre": "BE au Présent", "regle": "I am, You are, He/She/It is...", "ex": "I am happy (Je suis heureux), She is a doctor (Elle est médecin)", "test": "He _ (be) a doctor.", "rep": "is"},
        {"titre": "HAVE GOT", "regle": "Possession : I have got, He has got.", "ex": "I have got a car (J'ai une voiture), He has got a dog (Il a un chien)", "test": "He _ got a dog.", "rep": "has"},
        {"titre": "Articles A/AN/THE", "regle": "A (consonne), AN (voyelle), THE (précis).", "ex": "A banana (Une banane), An apple (Une pomme)", "test": "_ orange.", "rep": "an"},
        {"titre": "Le Pluriel", "regle": "Ajoutez 's'. Irrégulier: Men, Children.", "ex": "Two cars (Deux voitures), Three children (Trois enfants)", "test": "Pluriel de 'boy' :", "rep": "boys"},
        {"titre": "Adj. Possessifs", "regle": "My, Your, His, Her...", "ex": "My book (Mon livre), Her cat (Son chat)", "test": "Traduis 'Mon chien' :", "rep": "my dog"},
        {"titre": "Présent Simple (+)", "regle": "Base + 's' à la 3ème pers.", "ex": "He works (Il travaille), I play (Je joue)", "test": "She _ (work) here.", "rep": "works"},
        {"titre": "Présent Simple (-)", "regle": "Don't / Doesn't + verbe.", "ex": "I don't know (Je ne sais pas)", "test": "He _ like pizza.", "rep": "doesn't"},
        {"titre": "Questions WH-", "regle": "Who, What, Where, When, Why.", "ex": "Where is it? (Où est-ce ?)", "test": "Mot pour 'Qui' ?", "rep": "who"},
        {"titre": "L'Heure", "regle": "It is [hour] o'clock.", "ex": "It is 5 o'clock (Il est 5h)", "test": "Traduis 'Il est 8h' :", "rep": "it is 8 o'clock"},
        {"titre": "Présent Continu", "regle": "BE + V-ing (action en cours).", "ex": "I am eating (Je mange)", "test": "They _ (sleep) now.", "rep": "are sleeping"},
        {"titre": "Lieu (In/On/At)", "regle": "In (dans), On (sur), At (à).", "ex": "On the table (Sur la table)", "test": "I am _ home.", "rep": "at"},
        {"titre": "CAN (Capacité)", "regle": "CAN + verbe (pouvoir).", "ex": "I can swim (Je sais nager)", "test": "She _ (can/not) drive.", "rep": "can't"},
        {"titre": "Impératif", "regle": "Verbe seul pour donner un ordre.", "ex": "Sit down! (Assieds-toi !)", "test": "_ (go) away!", "rep": "go"},
        {"titre": "BE au Passé", "regle": "Was / Were.", "ex": "I was happy (J'étais heureux)", "test": "They _ (be) tired.", "rep": "were"},
        {"titre": "Prétérit (+)", "regle": "Verbe + ED (régulier).", "ex": "I watched (J'ai regardé)", "test": "She _ (play) golf.", "rep": "played"},
        {"titre": "Prétérit (Irreg)", "regle": "Go -> Went, See -> Saw.", "ex": "I went (Je suis allé)", "test": "Passé de 'see' :", "rep": "saw"},
        {"titre": "Some / Any", "regle": "Some (+), Any (- / ?).", "ex": "Some water (De l'eau)", "test": "I don't have _ money.", "rep": "any"},
        {"titre": "Comparatif", "regle": "Court + ER than / More + Long.", "ex": "Faster than (Plus vite que)", "test": "Tall -> _ than.", "rep": "taller"},
        {"titre": "Going to", "regle": "Futur proche : BE + Going to.", "ex": "I'm going to eat (Je vais manger)", "test": "He _ going to win.", "rep": "is"}
    ],
    "Intermédiaire": [
        {"titre": "Present Perfect", "regle": "Have + Part. Passé.", "ex": "I have seen (J'ai vu)", "test": "She _ (work) here.", "rep": "has worked"}
    ],
    "Avancé": [
        {"titre": "Conditionnel 3", "regle": "If + Past Perfect -> Would have + PP.", "ex": "If I had known... (Si j'avais su...)", "test": "If he _ (be) there.", "rep": "had been"}
    ]
}

# --- FONCTION AUDIO ---
def parler(texte):
    # On ne garde que la partie anglaise (avant la parenthèse)
    texte_en = texte.split('(')[0].strip()
    js = f"const msg = new SpeechSynthesisUtterance('{texte_en}'); msg.lang = 'en-US'; window.speechSynthesis.speak(msg);"
    st.components.v1.html(f"<script>{js}</script>", height=0)

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
    liste_leçons = PROGRAMME[st.session_state.niveau]
    leçon = liste_leçons[st.session_state.leçon_index]
    
    st.sidebar.title("Menu Clarisse")
    st.sidebar.write(f"Niveau : *{st.session_state.niveau}*")
    st.sidebar.write(f"Leçon : {st.session_state.leçon_index + 1} / {len(liste_leçons)}")
    
    if st.sidebar.button("⏮️ Retour"):
        if st.session_state.leçon_index > 0:
            st.session_state.leçon_index -= 1
            st.rerun()
            
    if st.sidebar.button("🔄 Changer de niveau"):
        st.session_state.etape, st.session_state.leçon_index = "presentation", 0
        st.rerun()

    st.title(f"Leçon {st.session_state.leçon_index + 1} : {leçon['titre']}")
    st.info(f"*Règle :* {leçon['regle']}")
    st.write(f"*Exemple :* {leçon['ex']}")
    if st.button("Écouter la prononciation 🔊"):
        parler(leçon['ex'])
        
    st.divider()
    st.subheader("Exercice")
    st.write(leçon['test'])
    ans = st.text_input("Réponse :", key=f"ans_{st.session_state.leçon_index}").lower().strip()
    
    if st.button("Valider"):
        if ans == leçon['rep']:
            st.success("C'est bien.")
            if st.session_state.leçon_index < len(liste_leçons) - 1:
                st.session_state.leçon_index += 1
                st.write("Cliquez à nouveau sur 'Valider' ou attendez la prochaine interaction.")
                st.rerun()
            else:
                st.balloons()
                st.success("Félicitations ! Tu as fini ce niveau.")
        else:
            st.error("Réessaie !")
Envoyé
Écrire à
