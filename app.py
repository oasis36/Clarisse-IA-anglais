import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Clarisse - English Learning", layout="centered")

st.write("### Interface d'Apprentissage avec Clarisse")

clarisse_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        .main-container { font-family: 'Segoe UI', sans-serif; text-align: center; padding: 30px; background-color: #f9f9f9; border-radius: 15px; border: 1px solid #ddd; }
        .btn-start { padding: 15px 30px; font-size: 18px; cursor: pointer; border-radius: 10px; background-color: #4CAF50; color: white; border: none; font-weight: bold; }
        .input-field { padding: 12px; font-size: 16px; margin: 15px; border-radius: 5px; border: 1px solid #ccc; width: 80%; }
        .hidden { display: none; }
        #display-text { margin-top: 20px; font-size: 1.2rem; color: #333; line-height: 1.4; text-align: left; }
    </style>
</head>
<body>
    <div class="main-container">
        <button id="launch-btn" class="btn-start">Lancer la conversation</button>

        <div id="step-1" class="hidden">
            <input type="text" id="user-name" class="input-field" placeholder="Entrez votre prénom...">
            <br>
            <button id="submit-name" class="btn-start" style="font-size: 14px; background-color: #008CBA;">Valider mon prénom</button>
        </div>

        <div id="step-2" class="hidden">
            <div id="levels-container" style="margin-top:20px;">
                <button class="btn-start" style="font-size:14px; margin:5px;" onclick="alert('Niveau Débutant')">Débutant</button>
                <button class="btn-start" style="font-size:14px; margin:5px;" onclick="alert('Niveau Intermédiaire')">Intermédiaire</button>
                <button class="btn-start" style="font-size:14px; margin:5px;" onclick="alert('Niveau Avancé')">Avancé</button>
            </div>
        </div>

        <div id="display-text"></div>
    </div>

    <script>
        const displayText = document.getElementById('display-text');
        let voices = [];
        
        function loadVoices() { 
            voices = window.speechSynthesis.getVoices(); 
        }
        window.speechSynthesis.onvoiceschanged = loadVoices;
        loadVoices();

        function speakFluid(text) {
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(text);
            const frenchVoice = voices.find(v => v.lang.includes('fr') && (v.name.includes('Google') || v.name.includes('Premium'))) || voices.find(v => v.lang.includes('fr'));
            
            if (frenchVoice) utter.voice = frenchVoice;
            utter.lang = 'fr-FR';
            utter.rate = 1.35; // Garde la fluidité rapide
            utter.pitch = 1.0;

            window.speechSynthesis.speak(utter);
        }

        document.getElementById('launch-btn').onclick = function() {
            this.style.display = 'none';
            document.getElementById('step-1').classList.remove('hidden');
            // MISE À JOUR DE LA PHRASE D'INTRODUCTION
            const intro = "Bonjour ! Je me présente, je m'appelle Clarisse, ton IA dédiée à l'apprentissage de l'anglais. Et toi, comment t'appelles-tu ?";
            displayText.innerText = intro;
            speakFluid(intro);
        };

        document.getElementById('submit-name').onclick = function() {
            const name = document.getElementById('user-name').value;
            if(name.trim() !== "") {
                document.getElementById('step-1').classList.add('hidden');
                document.getElementById('step-2').classList.remove('hidden');
                const welcome = "C'est un plaisir de faire ta connaissance, " + name + " ! Sache que nous pouvons parler de tout ensemble. Mon but est de t'aider à progresser. À tout moment, tu peux m'interrompre en français pour me demander une explication sur une phrase. Pour commencer notre programme, quel est ton niveau actuel ?";
                displayText.innerText = welcome;
                speakFluid(welcome);
            }
        };
    </script>
</body>
</html>
"""

components.html(clarisse_html, height=600)
