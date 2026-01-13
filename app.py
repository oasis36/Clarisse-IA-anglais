import streamlit as st
import streamlit.components.v1 as components

# Configuration de la page
st.set_page_config(page_title="Clarisse - English Learning", layout="centered")

# On définit le code HTML/JS à l'intérieur d'une variable Python
clarisse_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        .main-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 15px;
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
        .btn-start:active { box-shadow: 0 0; transform: translateY(4px); }
        .input-field { padding: 10px; font-size: 16px; margin: 10px; border-radius: 5px; border: 1px solid #ddd; width: 250px; }
        .hidden { display: none; }
        #text-area { margin-top: 25px; font-size: 1.2rem; color: #333; min-height: 50px; }
        .level-btn { padding: 10px 20px; margin: 5px; cursor: pointer; background-color: #008CBA; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="main-container">
        <button id="launch-btn" class="btn-start">Lancer la conversation</button>

        <div id="step-1" class="hidden">
            <p id="intro-text"></p>
            <input type="text" id="user-name" class="input-field" placeholder="Écris ton nom ici...">
            <br>
            <button id="submit-name" class="btn-start" style="font-size: 14px; padding: 10px 20px;">Valider mon nom</button>
        </div>

        <div id="step-2" class="hidden">
            <p id="welcome-text"></p>
            <div id="levels">
                <button class="level-btn" onclick="setLevel('Débutant')">Débutant</button>
                <button class="level-btn" onclick="setLevel('Intermédiaire')">Intermédiaire</button>
                <button class="level-btn" onclick="setLevel('Avancé')">Avancé</button>
            </div>
        </div>

        <div id="text-area"></div>
    </div>

    <script>
        const launchBtn = document.getElementById('launch-btn');
        const step1 = document.getElementById('step-1');
        const step2 = document.getElementById('step-2');
        const textArea = document.getElementById('text-area');
        const nameInput = document.getElementById('user-name');
        
        function speak(text) {
            const synth = window.speechSynthesis;
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = 'fr-FR';
            synth.speak(utter);
        }

        // Action : Lancer la conversation
        launchBtn.onclick = () => {
            launchBtn.classList.add('hidden');
            step1.classList.remove('hidden');
            const msg = "Bonjour ! Je suis Clarisse, ton IA dédiée à l'apprentissage de l'anglais. Et toi, comment t'appelles-tu ?";
            textArea.innerText = msg;
            speak(msg);
        };

        // Action : Valider le nom (Deuxième temps)
        document.getElementById('submit-name').onclick = () => {
            const name = nameInput.value;
            if(name) {
                step1.classList.add('hidden');
                step2.classList.remove('hidden');
                const welcome = C'est un plaisir de faire ta connaissance, ${name} ! Sache que nous pouvons parler de tout ensemble. Mon but est de t'aider à progresser. À tout moment, tu peux m'interrompre en français pour me demander une explication sur une phrase. Pour commencer notre programme, quel est ton niveau actuel ?;
                textArea.innerText = welcome;
                speak(welcome);
            }
        };

        function setLevel(lvl) {
            alert("Niveau choisi : " + lvl + ". Clarisse prépare votre première leçon !");
        }
    </script>
</body>
</html>
"""

# Injection du code dans l'application Streamlit
components.html(clarisse_html, height=600)
