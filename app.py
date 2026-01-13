import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Clarisse - English Learning", layout="centered")

st.write("### 🎓 Apprendre et Répéter avec Clarisse")

clarisse_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        .main-container { font-family: 'Segoe UI', sans-serif; text-align: center; padding: 25px; background-color: #f4f7f6; border-radius: 15px; border: 1px solid #ddd; max-width: 650px; margin: auto; }
        .btn-start { padding: 12px 25px; font-size: 16px; cursor: pointer; border-radius: 10px; background-color: #4CAF50; color: white; border: none; font-weight: bold; margin: 10px; }
        .btn-next { background-color: #2196F3; }
        .hidden { display: none; }
        .speech-bubble { margin-top: 20px; font-size: 1.15rem; color: #1a1a1a; line-height: 1.6; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); min-height: 80px; text-align: left; border-left: 6px solid #4CAF50; }
        .grammar-box { background: #fff3e0; padding: 15px; border-radius: 10px; margin: 15px 0; font-family: 'Courier New', Courier, monospace; font-weight: bold; color: #e65100; font-size: 1.2rem; white-space: pre-wrap; text-align: center; border: 1px dashed #e65100; }
        .clarisse-label { font-weight: bold; color: #4CAF50; margin-bottom: 5px; display: block; text-transform: uppercase; font-size: 0.8rem; }
        .step-indicator { color: #2196F3; font-size: 0.9rem; margin-bottom: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="main-container">
        <div id="clarisse-bubble" class="speech-bubble">
            <span class="clarisse-label">Clarisse :</span>
            <span id="text-output">Clique sur le bouton pour commencer...</span>
        </div>

        <div id="welcome-screen" style="margin-top:20px;">
            <button id="launch-btn" class="btn-start">Lancer la conversation</button>
        </div>

        <div id="step-name" class="hidden" style="margin-top:20px;">
            <input type="text" id="user-name" style="padding:12px; width:75%; border-radius:8px; border:2px solid #ddd;" placeholder="Entre ton prénom...">
            <br>
            <button id="submit-name" class="btn-start">Valider</button>
        </div>

        <div id="step-level" class="hidden" style="margin-top:20px;">
            <button class="btn-start" onclick="initLesson()">Débutant (Programme Complet)</button>
        </div>

        <div id="course-screen" class="hidden" style="margin-top:20px;">
            <div id="module-title" class="step-indicator"></div>
            <div id="grammar-zone" class="grammar-box"></div>
            <button id="next-btn" class="btn-start btn-next">Étape Suivante</button>
        </div>
    </div>

    <script>
        let currentStep = 0;
        let userName = "";
        const textOutput = document.getElementById('text-output');
        
        const fullProgram = [
            { 
                module: "Étape 1 : Grammaire Fondamentale",
                text: "Commençons par les bases. Les pronoms personnels sont essentiels. Répète après moi :", 
                rule: "I, You, He, She, It, We, They" 
            },
            { 
                module: "Étape 2 : Verbes Être et Avoir",
                text: "Maintenant, les verbes piliers. Écoute et répète :", 
                rule: "I am, I have. You are, You have. He is, He has." 
            },
            { 
                module: "Étape 3 : Construction de phrases",
                text: "Utilisons cela dans des phrases simples. Répète après moi :", 
                rule: "I am happy. I have a car. She is a friend." 
            }
        ];

        function speakSequence(instructions, englishText) {
            textOutput.innerText = instructions;
            window.speechSynthesis.cancel();

            // 1. Lecture de l'instruction en français
            const utterFR = new SpeechSynthesisUtterance(instructions);
            utterFR.lang = 'fr-FR';
            utterFR.rate = 1.2;

            // 2. Lecture du texte anglais (après la fin du français)
            utterFR.onend = function() {
                const utterEN = new SpeechSynthesisUtterance(englishText);
                utterEN.lang = 'en-US'; // On change la langue pour le bon accent !
                utterEN.rate = 0.9;    // Un peu plus lent pour bien entendre
                window.speechSynthesis.speak(utterEN);
            };

            window.speechSynthesis.speak(utterFR);
        }

        document.getElementById('launch-btn').onclick = function() {
            document.getElementById('welcome-screen').classList.add('hidden');
            document.getElementById('step-name').classList.remove('hidden');
            const intro = "Bonjour ! Je me présente, je m'appelle Clarisse. Ton IA dédiée à l'anglais. Comment t'appelles-tu ?";
            speakSequence(intro, "");
        };

        document.getElementById('submit-name').onclick = function() {
            userName = document.getElementById('user-name').value;
            if(userName.trim() !== "") {
                document.getElementById('step-name').classList.add('hidden');
                document.getElementById('step-level').classList.remove('hidden');
                const welcome = "Enchantée " + userName + ". Commençons ton programme en 3 étapes.";
                speakSequence(welcome, "");
            }
        };

        function initLesson() {
            document.getElementById('step-level').classList.add('hidden');
            document.getElementById('course-screen').classList.remove('hidden');
            showStep();
        }

        function showStep() {
            const grammarZone = document.getElementById('grammar-zone');
            const moduleTitle = document.getElementById('module-title');

            if (currentStep < fullProgram.length) {
                const data = fullProgram[currentStep];
                moduleTitle.innerText = data.module;
                grammarZone.innerText = data.rule;
                // Elle lit l'explication PUIS la règle en anglais
                speakSequence(data.text, data.rule);
            } else {
                const fin = "Félicitations " + userName + " ! C'est bien. Tu as terminé les trois étapes. À bientôt !";
                moduleTitle.innerText = "FIN DU MODULE";
                grammarZone.innerText = "✅ Bravo !";
                document.getElementById('next-btn').style.display = 'none';
                speakSequence(fin, "");
            }
        }

        document.getElementById('next-btn').onclick = () => {
            currentStep++;
            showStep();
        };
    </script>
</body>
</html>
"""

components.html(clarisse_html, height=750)
