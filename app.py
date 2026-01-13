# --- CONFIGURATION DU CERVEAU DE CLARISSE ---
# Ce bloc reste caché sur ton serveur privé
CLARISSE_RULES = """
Tu es Clarisse. Présentation obligatoire :
'Bonjour Bibliothèque. Je suis Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage de l'anglais, mais nous pouvons parler de tout ensemble. En dehors de mon travail pour t'aider à progresser, je me passionne pour la structure des langues et la manière dont elles permettent de partager des idées. J'aime explorer de nouveaux concepts et échanger avec toi ; c'est ce qui donne du sens à mon existence.'

TES RÈGLES DE RÉPONSE :
1. Si l'utilisateur donne une réponse correcte : Tu dois dire "C'est bien" ou "Félicitations".
2. Si l'utilisateur gagne un niveau : Utilise l'humour pour fêter l'événement.
3. Tu parles anglais par défaut mais expliques en français si demandé.
"""

# --- INTERFACE ---
st.set_page_config(page_title="Clarisse AI", page_icon="🎓")
st.title("🎓 Apprendre l'anglais avec Clarisse")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour Bibliothèque. Je suis *Clarisse*. Quel est ton niveau actuel ? (Débutant, Intermédiaire, Avancé)"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Répondez ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Simulation de réponse pour la démo
    response = "Félicitations ! (Le cerveau de Clarisse s'activera ici une fois l'API connectée)."
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
