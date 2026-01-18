import streamlit as st

# --- CONFIGURATION INITIALE ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓")

if 'etape' not in st.session_state:
    st.session_state.etape = "presentation"
if 'leçon_index' not in st.session_state:
    st.session_state.leçon_index = 0
if 'niveau' not in st.session_state:
    st.session_state.niveau = "Débutant"

# --- PROGRAMME INTÉGRAL (60 LEÇONS) ---
PROGRAMME = {
    "Débutant": [
        {"titre": "L'Alphabet", "regle": "A [eɪ], E [iː], G [dʒ], J [dʒeɪ].", "ex": "Apple (Pomme), Book (Livre)", "test": "Épelle 'cat' :", "rep": "cat"},
        {"titre": "BE au Présent", "regle": "I am, You are, He/She/It is...", "ex": "I am happy (Je suis heureux)", "test": "He _ (be) a doctor.", "rep": "is"},
        {"titre": "HAVE GOT", "regle": "Possession : I have got, He has got.", "ex": "I have got a car (J'ai une voiture)", "test": "He _ got a dog.", "rep": "has"},
        {"titre": "Articles A/AN/THE", "regle": "A (consonne), AN (voyelle), THE (précis).", "ex": "An apple (Une pomme)", "test": "_ banana.", "rep": "a"},
        {"titre": "Le Pluriel", "regle": "Ajoutez 's'. Irrégulier: Men, Children.", "ex": "Two cars (Deux voitures)", "test": "Pluriel de 'boy' :", "rep": "boys"},
        {"titre": "Adj. Possessifs", "regle": "My, Your, His, Her...", "ex": "My book (Mon livre)", "test": "Traduis 'Son chat' (femme) :", "rep": "her cat"},
        {"titre": "Présent Simple (+)", "regle": "Base + 's' à la 3ème pers.", "ex": "He works (Il travaille)", "test": "I _ (play) tennis.", "rep": "play"},
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
        {"titre": "Present Perfect", "regle": "Have + Part. Passé.", "ex": "I have seen (J'ai vu)", "test": "She _ (work) here.", "rep": "has worked"},
        {"titre": "For / Since", "regle": "For (durée), Since (début).", "ex": "For 2 days (Pendant 2 jours)", "test": "_ 1990.", "rep": "since"},
        {"titre": "Superlatif", "regle": "The + Short-est / The most + Long.", "ex": "The biggest (Le plus grand)", "test": "The _ (fast).", "rep": "fastest"},
        {"titre": "Modal Should", "regle": "Should (conseil).", "ex": "You should go (Tu devrais y aller)", "test": "He _ (not) smoke.", "rep": "shouldn't"},
        {"titre": "Will (Futur)", "regle": "Will + verbe (décision).", "ex": "It will rain (Il pleuvra)", "test": "I _ (help) you.", "rep": "will help"},
        {"titre": "Prétérit Continu", "regle": "Was/Were + V-ing.", "ex": "I was sleeping (Je dormais)", "test": "They _ playing.", "rep": "were"},
        {"titre": "Passif", "regle": "BE + Part. Passé.", "ex": "It is made (C'est fait)", "test": "The car _ (steal).", "rep": "was stolen"},
        {"titre": "Used to", "regle": "Habitude passée.", "ex": "I used to smoke (Je fumais avant)", "test": "I _ to live here.", "rep": "used"},
        {"titre": "Relative Pronouns", "regle": "Who (person), Which (thing).", "ex": "The man who... (L'homme qui...)", "test": "The book _ I read.", "rep": "which"},
        {"titre": "Conditionnel 1", "regle": "If + Présent -> Will.", "ex": "If it rains, I'll stay (S'il pleut, je reste)", "test": "If I win, I _ (buy) it.", "rep": "will buy"},
        {"titre": "Conditionnel 2", "regle": "If + Prétérit -> Would.", "ex": "If I were rich... (Si j'étais riche...)", "test": "If I _ (be) you.", "rep": "were"},
        {"titre": "Gerund vs Inf", "regle": "Enjoy + ing / Want + to.", "ex": "I enjoy swimming (J'aime nager)", "test": "I want _ (eat).", "rep": "to eat"},
        {"titre": "Past Perfect", "regle": "Had + Part. Passé.", "ex": "I had left (J'étais parti)", "test": "They _ (finish).", "rep": "had finished"},
        {"titre": "Passive Voice", "regle": "Mise en valeur de l'objet.", "ex": "It was built (Ce fut construit)", "test": "The cake _ eaten.", "rep": "was"},
        {"titre": "Modaux Probabilité", "regle": "May / Might / Must.", "ex": "It must be him (Ce doit être lui)", "test": "It _ rain (possible).", "rep": "might"},
        {"titre": "Discours Rapporté", "regle": "He said that...", "ex": "She said she was tired.", "test": "He _ (say) hello.", "rep": "said"},
        {"titre": "Phrasal Verbs 1", "regle": "Verbe + préposition.", "ex": "Give up (Abandonner)", "test": "Wake _ (Se réveiller).", "rep": "up"},
        {"titre": "Question Tags", "regle": "..., isn't it? / ..., don't you?", "ex": "You are French, aren't you?", "test": "He is tall, _ he?", "rep": "isn't"},
        {"titre": "Adverbes", "regle": "Adj + LY.", "ex": "Slowly (Doucement)", "test": "Quick -> _.", "rep": "quickly"},
        {"titre": "Révision B2", "regle": "Validation.", "ex": "Good luck (Bonne chance)", "test": "Traduis 'Hier' :", "rep": "yesterday"}
    ],
    "Avancé": [
        {"titre": "Conditionnel 3", "regle": "If + Past Perfect -> Would have + PP.", "ex": "If I had known... (Si j'avais su...)", "test": "If he _ (be) there.", "rep": "had been"},
        {"titre": "Wish / If Only", "regle": "Regret.", "ex": "I wish I were... (Je voudrais être...)", "test": "I wish I _ (know).", "rep": "knew"},
        {"titre": "Have something done", "regle": "Faire faire.", "ex": "I had my hair cut (Je me suis fait couper les cheveux)", "test": "I had it _ (repair).", "rep": "repaired"},
        {"titre": "Inversion Emphase", "regle": "Never have I...", "ex": "Never have I seen such (Jamais je n'ai vu tel)", "test": "Seldom _ he go.", "rep": "does"},
        {"titre": "Modaux Passé", "regle": "Should have + PP.", "ex": "You should have told me.", "test": "I _ (must) have lost it.", "rep": "must"},
        {"titre": "Pres Perf Cont.", "regle": "Have been + V-ing.", "ex": "I have been waiting for hours.", "test": "She _ been crying.", "rep": "has"},
        {"titre": "Phrasal Verbs 2", "regle": "Get along, Carry on...", "ex": "Keep on (Continuer)", "test": "Look _ (Chercher).", "rep": "for"},
        {"titre": "Connecteurs", "regle": "However, Despite, Although.", "ex": "Despite the rain (Malgré la pluie)", "test": "_ (Bien que) it's late.", "rep": "although"},
        {"titre": "Subjonctif", "regle": "I suggest that he be...", "ex": "It is vital that she stay.", "test": "I insist he _ (go).", "rep": "go"},
        {"titre": "Nominalisation", "regle": "Verbe en nom.", "ex": "Decision (Décision)", "test": "Noun of 'Apply' :", "rep": "application"},
        {"titre": "Cleft Sentences", "regle": "What I need is...", "ex": "It is you that I love.", "test": "_ I want is water.", "rep": "what"},
        {"titre": "Double Comp.", "regle": "The more... the more...", "ex": "The more I study, the more I learn.", "test": "The _ the better.", "rep": "sooner"},
        {"titre": "Participe début", "regle": "Having finished, I left.", "ex": "Being tired, he went home.", "test": "_ (see) the car, I ran.", "rep": "seeing"},
        {"titre": "Future Perfect", "regle": "Will have + Part. Passé.", "ex": "I will have finished by 5.", "test": "She _ have arrived.", "rep": "will"},
        {"titre": "Idiomes", "regle": "Expressions.", "ex": "Piece of cake (C'est facile)", "test": "Under the _ (Malade).", "rep": "weather"},
        {"titre": "Business English", "regle": "Vocabulaire pro.", "ex": "A meeting (Une réunion)", "test": "Traduis 'Rendez-vous' :", "rep": "appointment"},
        {"titre": "Rédaction", "regle": "Structure d'essai.", "ex": "Firstly, Secondly...", "test": "_ (Pour conclure).", "rep": "to conclude"},
        {"titre": "Accents", "regle": "UK vs US English.", "ex": "Flat (UK) / Apartment (US)", "test": "US for 'Lift' :", "rep": "elevator"},
        {"titre": "Argot / Slang", "regle": "Familier.", "ex": "Gonna (Going to)", "test": "Wanna -> Want _.", "rep": "to"},
        {"titre": "Examen Final", "regle": "Maîtrise C1.", "ex": "Well done (Bien joué)", "test": "Traduis 'Maîtrise' :", "rep": "mastery"}
    ]
}

# --- FONCTIONS ---
def parler(texte):
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
    liste = PROGRAMME[st.session_state.niveau]
    leçon = liste[st.session_state.leçon_index]
    
    st.sidebar.title("Menu Clarisse")
    st.sidebar.write(f"Niveau : *{st.session_state.niveau}*")
    st.sidebar.progress((st.session_state.leçon_index + 1) / len(liste))
    
    if st.sidebar.button("🔄 Changer de niveau"):
        st.session_state.etape, st.session_state.leçon_index = "presentation", 0
        st.rerun()

    st.title(f"Leçon {st.session_state.leçon_index + 1} : {leçon['titre']}")
    st.info(f"*Règle :* {leçon['regle']}")
    st.write(f"*Exemple :* {leçon['ex']}")
    if st.button("Prononciation 🔊"): parler(leçon['ex'])
    
    st.divider()
    st.subheader("Exercice")
    st.write(leçon['test'])
    ans = st.text_input("Réponse :", key=f"ans_{st.session_state.leçon_index}_{st.session_state.niveau}").lower().strip()
    
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
