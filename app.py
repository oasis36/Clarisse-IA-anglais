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
        {"titre": "Questions WH-", "regle": "Who, What, Where, When, Why.", "ex": "Where is it?
