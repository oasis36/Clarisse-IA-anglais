import streamlit as st
import streamlit.components.v1 as components

# Configuration de la page
st.set_page_config(page_title="Clarisse - English Learning", layout="centered")

st.write("### Interface d'Apprentissage avec Clarisse")

clarisse_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        .main-container {
            font-family: sans-serif;
            text-align: center;
            padding: 30px;
            background-color: #f9f9f9;
            border-radius: 15px;
            border: 1px solid #ddd;
        }
        .btn-start {
            padding: 15px 30px;
            font-size: 18px;
            cursor: pointer;
            border-radius: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            box-shadow: 0 4px #2e6b31;
        }
        .input-field { padding: 10px; font-size: 16px; margin: 15px; border-radius: 5px; border: 1px solid #ccc; width: 80%; }
        .hidden { display: none; }
        #display-text { margin-top: 20px; font-size: 1.2rem; color: #333; font-weight: 500; line-height: 1.4; }
        .level-btn { padding: 10px 20px; margin: 10px; cursor: pointer; background-color: #008CBA; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="main-container">
        <button id="launch-btn" class="btn-start">Lancer la conversation</button>

        <div id="step-1" class="hidden">
            <input type="text" id="user-name" class="input-field" placeholder="Entrez votre prénom...">
            <br>
            <button id="submit-name" class="btn-start" style="font-size: 14px;">Valider</button>
        </div>

        <div id="step-2" class="hidden">
            <div id="levels-container">
                <button class="level-btn" onclick="alert('Niveau Débutant sélectionné')">Débutant</button>
                <button class="level-btn" onclick="alert('Niveau Intermédiaire sélectionné')">Intermédiaire</button>
                <button class="level-btn" onclick="alert('Niveau Avancé sélectionné')">Avancé</button>
            </div>
        </div>

        <div id="display-text"></div>
    </div>

    <script>
        const launchBtn = document.getElementById('launch-btn');
        const step1 = document.getElementById('step-1');
        const step2 = document.getElementById('step-2');
        const displayText = document.getElementById('display-text');
        const nameInput = document.getElementById('user-name');
        
        let voices = [];

        // Charger les voix et essayer de trouver une voix française de haute qualité
        function loadVoices() {
            voices = window.speechSynthesis.getVoices();
        }
        window.speechSynthesis.onvoiceschanged = loadVoices;
        loadVoices();

        function speak(text) {
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(text);
            
            // Cherche une voix française plus naturelle (ex: Google ou Premium)
            const frenchVoice = voices.find(v => v.lang.includes('fr') && v.name.includes('Google')) || 
                               voices.find(v => v.lang.includes('fr'));
            
            if (frenchVoice) utter.voice = frenchVoice;
            
            utter.lang = 'fr-FR';
            utter.rate = 0.9;  // Légèrement plus lent pour être moins robotique
            utter.pitch = 1.1; // Un ton légèrement plus haut pour plus de clarté
            
            window.speechSynthesis.speak(utter);
        }

        launchBtn.addEventListener('click', function() {
            launchBtn.style.display = 'none';
            step1.classList.remove('hidden');
            const intro = "Bonjour ! Je suis Clarisse, ton IA dédiée à l'apprentissage de l'anglais. Et toi, comment t'appelles-tu ?";
            displayText.innerText = intro;
            speak(intro);
        });

        document.getElementById('submit-name').addEventListener('click', function() {
            const name = nameInput.value;
            if(name.trim() !== "") {
                step1.classList.add('hidden');
                step2.classList.remove('hidden');
                const welcome = "C'est un plaisir de faire ta connaissance, " + name + " ! Sache que nous pouvons parler de tout ensemble. Mon but est de t'aider à progresser. À tout moment, tu peux m'interrompre en français pour me demander une explication sur une phrase. Pour commencer notre programme, quel est ton niveau actuel ?";
                displayText.innerText = welcome;
                speak(welcome);
            }
        });
    </script>
</body>
</html>
"""

components.html(clarisse_html, height=600)
