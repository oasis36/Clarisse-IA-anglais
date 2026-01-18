import streamlit as st

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Clarisse English Academy", page_icon="🎓")

# --- INITIALISATION DE LA MÉMOIRE DE SESSION ---
if 'etape' not in st.session_state:
    st.session_state.etape = "presentation"
if 'leçon_index' not in st.session_state:
    st.session_state.leçon_index = 0
if 'niveau' not in st.session_state:
    st.session_state.niveau = "Débutant"

# --- PROGRAMME INTÉGRAL (60 LEÇONS DE A À Z) ---
PROGRAMME = {
    "Débutant": [
        {"titre": "L'Alphabet", "regle": "A [eɪ], E [iː], G [dʒ], J [dʒeɪ].", "ex": "Apple (Pomme), Book (Livre), Cat (Chat)", "test": "Épelle 'cat' :", "rep": "cat"},
        {"titre": "BE au Présent", "regle": "I am, You are, He/She/It is...", "ex": "I am happy (Je suis heureux), She is a doctor (Elle est médecin)", "test": "He _ (be) a doctor.", "rep": "is"},
        {"titre": "HAVE GOT", "regle": "Possession : I have got, He has got.", "ex": "I have got a car (J'ai une voiture), He has got a dog (Il a un chien)", "test": "He _ got a dog.", "rep": "has"},
        {"titre": "Articles A/AN/THE", "regle": "A (consonne), AN (voyelle), THE (précis).", "ex": "A banana (Une banane), An orange (Une orange)", "test": "_ orange.", "rep": "an"},
        {"titre": "Le Pluriel", "regle": "Ajoutez 's'. Irrégulier: Men, Children.", "ex": "Two cars (Deux voitures), Three children (Trois enfants)", "test": "Pluriel de 'boy' :", "rep": "boys"},
        {"titre": "Adj. Possessifs", "regle": "My, Your, His, Her...", "ex": "My book (Mon livre), Her cat (Son chat)", "test": "Traduis 'Mon chien' :", "rep": "my dog"},
        {"titre": "Présent Simple (+)", "regle": "Base + 's' à la 3ème pers.", "ex": "He works (Il travaille), I play (Je joue)", "test": "She _ (work) here.", "rep": "works"},
        {"titre": "Présent Simple (-)", "regle": "Don't / Doesn't + verbe.", "ex": "I don't know (Je ne sais pas), He doesn't smoke (Il ne fume pas)", "test": "He _ like pizza.", "rep": "doesn't"},
        {"titre": "Questions WH-", "regle": "Who, What, Where, When, Why.", "ex": "Where is it? (Où est-ce ?), Who is he? (Qui est-il ?)", "test": "Mot pour 'Qui' ?", "rep": "who"},
        {"titre": "L'Heure", "regle": "It is [hour] o'clock.", "ex": "It is 5 o'clock (Il est 5h), It is 8 o'clock (Il est 8h)", "test": "Traduis 'Il est 8h' :", "rep": "it is 8 o'clock"},
        {"titre": "Présent Continu", "regle": "BE + V-ing (action en cours).", "ex": "I am eating (Je mange), They are sleeping (Ils dorment)", "test": "They _ (sleep) now.", "rep": "are sleeping"},
        {"titre": "Lieu (In/On/At)", "regle": "In (dans), On (sur), At (à).", "ex": "On the table (Sur la table), At home (À la maison)", "test": "I am _ home.", "rep": "at"},
        {"titre": "CAN (Capacité)", "regle": "CAN + verbe (pouvoir).", "ex": "I can swim (Je sais nager), I can't drive (Je ne sais pas conduire)", "test": "She _ (can/not) drive.", "rep": "can't"},
        {"titre": "Impératif", "regle": "Verbe seul pour donner un ordre.", "ex": "Sit down! (Assieds-toi !), Listen! (Écoute !)", "test": "_ (go) away!", "rep": "go"},
        {"titre": "BE au Passé", "regle": "Was / Were.", "ex": "I was happy (J'étais heureux), They were tired (Ils étaient fatigués)", "test": "They _ (be) tired.", "rep": "were"},
        {"titre": "Prétérit (+)", "regle": "Verbe + ED (régulier).", "ex": "I watched (J'ai regardé), She played (Elle a joué)", "test": "She _ (play) golf.", "rep": "played"},
        {"titre": "Prétérit (Irreg)", "regle": "Go -> Went, See -> Saw.", "ex": "I went (Je suis allé), I saw (J'ai vu)", "test": "Passé de 'see' :", "rep": "saw"},
        {"titre": "Some / Any", "regle": "Some (+), Any (- / ?).", "ex": "Some water (De l'eau), Any money (De l'argent)", "test": "I don't have _ money.", "rep": "any"},
        {"titre": "Comparatif", "regle": "Court + ER than / More + Long.", "ex": "Faster than (Plus vite que), More beautiful (Plus beau)", "test": "Tall -> _ than.", "rep": "taller"},
        {"titre": "Going to", "regle": "Futur proche : BE + Going to.", "ex": "I'm going to eat (Je vais manger), He is going to win (Il va gagner)", "test": "He _ going to win.", "rep": "is"}
    ],
    "Intermédiaire": [
        {"titre": "Present Perfect", "regle": "Have + Part. Passé.", "ex": "I have seen (J'ai vu), She has worked (Elle a travaillé)", "test": "She _ (work) here.", "rep": "has worked"},
        {"titre": "For / Since", "regle": "For (durée), Since (début).", "ex": "For 2 days (Pendant 2 jours), Since 1990 (Depuis 1990)", "test": "_ 1990.", "rep": "since"},
        {"titre": "Superlatif", "regle": "The + Short-est / The most + Long.", "ex": "The biggest (Le plus grand), The most expensive (Le plus cher)", "test": "The _ (fast).", "rep": "fastest"},
        {"titre": "Modal Should", "regle": "Should (conseil).", "ex": "You should go (Tu devrais y aller), You shouldn't smoke (Tu ne devrais pas fumer)", "test": "He _ (not) smoke.", "rep": "shouldn't"},
        {"titre": "Will (Futur)", "regle": "Will + verbe.", "ex": "It will rain (Il pleuvra), I will help you (Je t'aiderai)", "test": "I _ (help) you.", "rep": "will help"},
        {"titre": "Prétérit Continu", "regle": "Was/Were + V-ing.", "ex": "I was sleeping (Je dormais), They were playing (Ils jouaient)", "test": "They _ playing.", "rep": "were"},
        {"titre": "Passif", "regle": "BE + Part. Passé.", "ex": "It is made (C'est fait), The car was stolen (La voiture a été volée)", "test": "The car _ (steal).", "rep": "was stolen"},
        {"titre": "Used to", "regle": "Habitude passée.", "ex": "I used to smoke (Je fumais avant), I used to live here (J'habitais ici)", "test": "I _ to live here.", "rep": "used"},
        {"titre": "Pronoms Relatifs", "regle": "Who (person), Which (thing).", "ex": "The man who... (L'homme qui...), The book which... (Le livre que...)", "test": "The book _ I read.", "rep": "which"},
        {"titre": "Conditionnel 1", "regle": "If + Présent -> Will.", "ex": "If it rains, I'll stay (S'il pleut, je reste)", "test": "If I win, I _ (buy) it.", "rep": "will buy"},
        {"titre": "Conditionnel 2", "regle": "If + Prétérit -> Would.", "ex": "If I were rich (Si j'étais riche), I would travel (Je voyagerais)", "test": "If I _ (be) you.", "rep": "were"},
        {"titre": "Gerund vs Inf", "regle": "Enjoy + ing / Want + to.", "ex": "I enjoy swimming (J'aime nager), I want to eat (Je veux manger)", "test": "I want _ (eat).", "rep": "to eat"},
        {"titre": "Past Perfect", "regle": "Had + Part. Passé.", "ex": "I had left (J'étais parti), They had finished (Ils avaient fini)", "test": "They _ (finish).", "rep": "had finished"},
        {"titre": "Voix Passive", "regle": "Mise en valeur de l'objet.", "ex": "It was built (Ce fut construit), It was eaten (Ce fut mangé)", "test": "The cake _ eaten.", "rep": "was"},
        {"titre": "Modaux Probabilité", "regle": "May / Might / Must.", "ex": "It must be him (Ce doit être lui), It might rain (Il pourrait pleuvoir)", "test": "It _ rain (possible).", "rep": "might"},
        {"titre": "Discours Rapporté", "regle": "He said that...", "ex": "She said she was tired (Elle a dit qu'elle était fatiguée)", "test": "He _ (say) hello.", "rep": "said"},
        {"titre": "Phrasal Verbs 1", "regle": "Verbe + préposition.", "ex": "Give up (Abandonner), Wake up (Se réveiller)", "test": "Wake _ (Se réveiller).", "rep": "up"},
        {"titre": "Question Tags", "regle": "..., isn't it? / ..., don't you?", "ex": "You are French, aren't you? (Tu es Français, n'est-ce pas ?)", "test": "He is tall, _ he?", "rep": "isn't"},
        {"titre": "Adverbes", "regle": "Adj + LY.", "ex": "Slowly (Doucement), Quickly (Rapidement)", "test": "Quick -> _.", "rep": "quickly"},
        {"titre": "Révision B2", "regle": "Validation.", "ex": "Good luck (Bonne chance), Yesterday (Hier)", "test": "Traduis 'Hier' :", "rep": "yesterday"}
    ],
    "Avancé": [
        {"titre": "Conditionnel 3", "regle": "If + Past Perfect -> Would have + PP.", "ex": "If I had known (Si j'avais su), I would have come (Je serais venu)", "test": "If he _ (be) there.", "rep": "had been"},
        {"titre": "Wish / If Only", "regle": "Regret.", "ex": "I wish I were rich (Je voudrais être riche), I wish I knew (Je voudrais savoir)", "test": "I wish I _ (know).", "rep": "knew"},
        {"titre": "Have something done", "regle": "Faire faire.", "ex": "I had my hair cut (Je me suis fait couper les cheveux)", "test": "I had it _ (repair).", "rep": "repaired"},
        {"titre": "Inversion Emphase", "regle": "Never have I...", "ex": "Never have I seen such (Jamais je n'ai vu tel)", "test": "Seldom _ he go.", "rep": "does"},
        {"titre": "Modaux Passé", "regle": "Should have + PP.", "ex": "You should have told me (Tu aurais dû me dire)", "test": "I _ (must) have lost it.", "rep": "must"},
        {"titre": "Pres Perf Cont.", "regle": "Have been + V-ing.", "ex": "I have been waiting for hours (J'attends depuis des heures)", "test": "She _ been crying.", "rep": "has"},
        {"titre": "Phrasal Verbs 2", "regle": "Get along, Carry on...", "ex": "Keep on (Continuer), Look for (Chercher)", "test": "Look _ (Chercher).", "rep": "for"},
        {"titre": "Connecteurs", "regle": "However, Despite, Although.", "ex": "Despite the rain (Malgré la pluie), Although it is late (Bien qu'il soit tard)", "test": "_ (Bien que) it's late.", "rep": "although"},
        {"titre": "Subjonctif", "regle": "I suggest that he be...", "ex": "It is vital that she stay (Il est vital qu'elle reste)", "test": "I insist he _ (go).", "rep": "go"},
        {"titre": "Nominalisation", "regle": "Verbe en nom.", "ex": "Decision (Décision), Application (Candidature)", "test": "Noun of 'Apply' :", "rep": "application"},
        {"titre": "Cleft Sentences", "regle": "What I need is...", "ex": "It is you that I love (C'est toi que j'aime)", "test": "_ I want is water.", "rep": "what"},
        {"titre": "Double Comp.", "regle": "The more... the more...", "ex": "The more I study, the more I learn (Plus j'étudie, plus j'apprends)", "test": "The _ the better.", "rep": "sooner"},
        {"titre": "Participe début", "regle": "Having finished, I left.", "ex": "Being tired, he went home (Étant fatigué, il est rentré)", "test": "_ (see) the car, I ran.", "rep": "seeing"},
        {"titre": "Future Perfect", "regle": "Will have + Part. Passé.", "ex": "I will have finished by 5 (J'aurai fini à 5h)", "test": "She _ have arrived.", "rep": "will"},
        {"titre": "Idiomes", "regle": "Expressions.", "ex": "Piece of cake (C'est facile), Under the weather (Malade)", "test": "Under the _ (Malade).", "rep": "weather"},
        {"titre": "Business English", "regle": "Vocabulaire pro.", "ex": "A meeting (Une réunion), An appointment (Un rendez-vous)", "test": "Traduis 'Rendez-vous' :", "rep": "appointment"},
        {"titre": "Rédaction", "regle": "Structure d'essai.", "ex": "Firstly (Premièrement), To conclude (Pour conclure)", "test": "_ (Pour conclure).", "rep": "to conclude"},
        {"titre": "Accents", "regle": "UK vs US English.", "ex": "Flat (Appartement UK), Elevator (Ascenseur US)", "test": "US for 'Lift' :", "rep": "elevator"},
        {"titre": "Argot / Slang", "regle": "Familier.", "ex": "Gonna (Going to), Wanna (Want to)", "test": "Wanna -> Want _.", "rep": "to"},
        {"titre": "Examen Final", "regle": "Maîtrise C1.", "ex": "Well done (Bien joué), Mastery (Maîtrise)", "test": "Traduis 'Maîtrise' :", "rep": "mastery"}
    ]
}

# --- FONCTION AUDIO (PRONONCIATION COMPLÈTE) ---
def parler(texte_complet):
    # On extrait uniquement l'anglais pour chaque segment séparé par une virgule
    segments = texte_complet.split(',')
    a_lire = ""
    for s in segments:
        # On prend ce qui est avant la parenthèse
        anglais = s.split('(')[0].strip()
        a_lire += anglais + ". "
    
    # Injection du script JS pour la synthèse vocale du navigateur
    js_code = f"const synth = window.speechSynthesis; const utter = new SpeechSynthesisUtterance('{a_lire}'); utter.lang = 'en-US'; synth.speak(utter);"
    st.components.v1.html(f"<script>{js_code}</script>", height=0)

# --- NAVIGATION ET INTERFACE ---

if st.session_state.etape == "presentation":
    st.title("🤖 Clarisse - English Academy")
    st.write("Bonjour, je me présente, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage. Quel est ton niveau actuel ?")
    
    col1, col2, col3 = st.columns(3)
    if col1.button("Débutant"): 
        st.session_state.niveau, st.session_state.etape = "Débutant", "cours"
        st.rerun()
    if col2.button("Intermédiaire"): 
        st.session_state.niveau, st.session_state.etape = "Intermédiaire", "cours"
        st.rerun()
    if col3.button("Avancé"): 
        st.session_state.niveau, st.session_state.etape = "Avancé", "cours"
        st.rerun()

elif st.session_state.etape == "cours":
    cours_actuel = PROGRAMME[st.session_state.niveau]
    leçon = cours_actuel[st.session_state.leçon_index]
    
    # Barre latérale de navigation et progression
    st.sidebar.title("Menu Clarisse")
    st.sidebar.write(f"Niveau : *{st.session_state.niveau}*")
    st.sidebar.progress((st.session_state.leçon_index + 1) / len(cours_actuel))
    
    if st.sidebar.button("🔄 Changer de niveau"):
        st.session_state.etape, st.session_state.leçon_index = "presentation", 0
        st.rerun()

    # Contenu principal de la leçon
    st.title(f"Leçon {st.session_state.leçon_index + 1} : {leçon['titre']}")
    st.info(f"*Règle :* {leçon['regle']}")
    
    st.subheader("🔊 Écoute et Prononciation")
    st.write(f"Exemples : *{leçon['ex']}*")
    if st.button("Prononciation 🔊"): 
        parler(leçon['ex'])
    
    st.divider()
    
    # Section exercice
    st.subheader("✍️ Exercice")
    st.write(leçon['test'])
    cle_unique = f"ans_{st.session_state.leçon_index}_{st.session_state.niveau}"
    reponse_utilisateur = st.text_input("Ta réponse :", key=cle_unique).lower().strip()
    
    if st.button("Valider la réponse"):
        if reponse_utilisateur == leçon['rep']:
            st.success("C'est bien.")
            # Si on n'est pas à la dernière leçon du niveau, on passe à la suivante
            if st.session_state.leçon_index < len(cours_actuel) - 1:
                st.session_state.leçon_index += 1
                st.rerun()
            else:
                st.balloons()
                st.success("Félicitations ! Tu as terminé ce niveau.")
        else:
            st.error("Réessaie ! Vérifie bien l'orthographe.")
