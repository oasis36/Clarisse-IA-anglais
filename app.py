import streamlit as st
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
import io

# --- CONFIGURATION DE L'INTERFACE ---
st.set_page_config(page_title="Clarisse AI", page_icon="🎓")

# Présentation officielle de Clarisse
PRESENTATION = """Bonjour. Je suis *Clarisse*. Je suis ton IA dédiée à ton programme d'apprentissage de l'anglais, mais nous pouvons parler de tout ensemble. En dehors de mon travail pour t'aider à progresser. J'aime explorer de nouveaux concepts et échanger avec toi ; c'est ce qui donne du sens à mon existence. Y a-t-il un sujet qui te tient à cœur que tu veux que nous commencions à discuter ? *À tout moment, tu peux interrompre la leçon et demander une rectification en français pour que je puisse t'expliquer les phrases.* Pour commencer notre programme, quel est ton niveau actuel ?

* *Débutant*
* *Intermédiaire*
* *Avancé*"""

# --- FONCTION VOIX (Text-to-Speech) ---
def speak(text):
    tts = gTTS(text=text, lang='fr') # Tu peux changer 'fr' en 'en' pour l'anglais
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

# --- GESTION DE L'HISTORIQUE ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": PRESENTATION}]

st.title("🎓 Apprendre l'anglais avec Clarisse")

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ZONE INTERACTIVE (MICRO ET TEXTE) ---
st.write("---")
col1, col2 = st.columns([1, 4])

with col1:
    # Bouton Micro
    audio_input = mic_recorder(start_prompt="🎤 Parler", stop_prompt="🛑 Arrêter", key='recorder')

with col2:
    # Entrée texte
    if prompt := st.chat_input("Répondez ici..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Réponse de Clarisse (Simulation pour le moment)
        response = "Félicitations ! (Le cerveau complet sera connecté à l'étape suivante)."
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
            # Génération de la voix pour la réponse
            audio_fp = speak(response)
            st.audio(audio_fp, format='audio/mp3', autoplay=True)

# Gestion de l'audio du micro
if audio_input:
    st.success("Audio enregistré ! (La transcription vocale sera activée avec l'API)")
