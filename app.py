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
        .btn-start { padding: 12px 25px; font-size: 16px; cursor: pointer; border-radius: 10px; background-color: #4CAF50; color: white; border: none; font-weight: bold; margin: 5px; }
        .input-field { padding: 12px; font-size: 16px; margin: 15px; border-radius: 5px; border: 1px solid #ccc; width: 80%; }
        .hidden { display: none; }
        #display-text { margin-top: 20px; font-size: 1.2rem; color: #333; line-height: 1.4; text-align: left; background: white; padding: 15px; border-radius: 10px; }
        .lesson-card { background: #e3f2fd; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left; border-left: 5px solid #2196F3; }
    </style>
</head>
<body>
    <div class="main-container">
        <button id="launch-btn" class="btn-start">Lancer la conversation</button>

        <div id="step-1" class="hidden">
            <input type="text" id="user-name" class="input-field" placeholder="Entrez votre prénom...">
            <br>
            <button id="submit-name" class="btn-start" style="background-color: #008CBA;">Valider mon prénom</button>
        </div>

        <div id="step-2" class="hidden">
            <p>Choisissez votre niveau pour commencer :</p>
            <button class="btn-start" onclick="demarrerCours('Débutant')">Débutant</button>
            <button class="btn-start" onclick="demarrerCours('Intermédiaire')">Intermédiaire</button>
            <button class="btn-start" onclick="demarrerCours('Avancé')">Avancé</button>
        </div>

        <div id="display-text"></div>
        
        <div id="lesson-area" class="hidden">
            <div class="lesson-card">
                <h4 id="lesson-title"></h4>
                <p id="lesson-content"></p>
                <button class="btn-start" style="background-color: #f44336;" onclick="location.reload()">Quitter la leçon</button>
            </div>
        </div>
    </div>

    <script>
        const displayText = document.getElementById('display-text');
        let voices = [];
        
        function loadVoices() { voices = window.speechSynthesis.getVoices(); }
        window.speechSynthesis.onvoiceschanged = loadVoices;
        loadVoices();

        function speak(text) {
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(text);
            const frenchVoice = voices.find(v => v.lang.includes('fr') && (v.name.includes('Google') || v.name.includes('Premium'))) || voices.find(v => v.lang.includes('fr'));
            if (frenchVoice) utter.voice = frenchVoice;
            utter.lang = 'fr-FR';
            utter.rate = 1.3;
            window.speechSynthesis.speak(utter);
        }

        // --- GESTION DES COURS ---
        function demarrerCours(niveau) {
            document.getElementById('step-2').classList.add('hidden');
            document.getElementById('lesson-area').classList.remove('hidden');
            
            let message = "";
            let titre = "";
            let contenu = "";

            if(niveau === 'Débutant') {
                titre = "Lesson 1: Greetings (Les Salutations)";
                contenu = "En anglais, pour dire bonjour le matin, on dit : *Good morning*. Répétez après moi.";
                message = "C'est parti pour le niveau Débutant. Félicitations pour ce premier pas ! Nous allons commencer par les bases. Lesson one : Greetings. Good morning.";
            } else if(niveau === 'Intermédiaire') {
                titre = "Lesson 1: Common Expressions";
                contenu = "How is it going? (Comment ça va ?). C'est une façon courante et fluide de demander des nouvelles.";
                message = "Niveau Intermédiaire activé. Félicitations ! Travaillons ta fluidité. On ne dit pas juste How are you, mais souvent : How is it going ?";
            } else {
                titre = "Lesson 1: Subtle Nuances";
                contenu = "The difference between 'Sometime' and 'Sometimes'. Let's dive into the details.";
                message = "Niveau Avancé. Félicitations, tu as déjà un excellent niveau ! Concentrons-nous sur les nuances qui feront de toi un expert.";
            }

            document.getElementById('lesson-title').innerText = titre;
            document.getElementById('lesson-content').innerText = contenu;
            displayText.innerText = message;
            speak(message);
        }

        // --- ETAPES INITIALES ---
        document.getElementById('launch-btn').onclick = function() {
            this.style.display = 'none';
            document.getElementById('step-1').classList.remove('hidden');
            const intro = "Bonjour ! Je me présente, je m'appelle Clarisse, ton IA dédiée à l'apprentissage de l'anglais. Et toi, comment t'appelles-tu ?";
            displayText.innerText = intro;
            speak(intro);
        };

        document.getElementById('submit-name').onclick = function() {
            const name = document.getElementById('user-name').value;
            if(name.trim() !== "") {
                document.getElementById('step-1').classList.add('hidden');
                document.getElementById('step-2').classList.remove('hidden');
                const welcome = "C'est un plaisir de faire ta connaissance, " + name + " ! Sache que nous pouvons parler de tout ensemble. Mon but est de t'aider à progresser. Pour commencer notre programme, quel est ton niveau actuel ?";
                displayText.innerText = welcome;
                speak(welcome);
            }
        };
    </script>
</body>
</html>
"""

components.html(clarisse_html, height=700)
