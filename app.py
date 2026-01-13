import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Clarisse - English Learning", layout="centered")

st.write("### 🎓 Ton Programme d'Apprentissage avec Clarisse")

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
        #display-text { margin-top: 20px; font-size: 1.1rem; color: #333; line-height: 1.5; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); min-height: 100px; text-align: left; border-left: 5px solid #4CAF50; }
        .grammar-box { background: #fff3e0; padding: 15px; border-radius: 10px; margin: 15px 0; font-family: 'Courier New', Courier, monospace; font-weight: bold; color: #e65100; font-size: 1.2rem; white-space: pre-wrap; text-align: center; }
        .step-indicator { color: #2196F3; font-size: 0.9rem; margin-bottom: 5px; font-weight: bold; text-transform: uppercase; }
    </style>
</head>
<body>
    <div class="main-container">
        <div id="welcome-screen">
            <button id="launch-btn" class="btn-start">Lancer la conversation</button>
        </div>

        <div id="step-name" class="hidden">
            <input type="text" id="user-name" style="padding:10px; width:70%; border-radius:5px; border:1px solid #ccc;" placeholder="Ton prénom...">
            <br>
            <button id="submit-name" class="btn-start">Valider mon prénom</button>
        </div>

        <div id="step-level" class="hidden">
            <p>Bonjour ! Je suis Clarisse. Pour commencer notre programme, quel est ton niveau actuel ?</p>
            <button class="btn-start" onclick="initLesson()">Débutant (Programme Complet)</button>
        </div>

        <div id="course-screen" class="hidden">
            <div id="module-title" class="step-indicator"></div>
            <div id="display-text"></div>
            <div id="grammar-zone" class="grammar-box"></div>
            <button id="next-btn" class="btn-start btn-next">Passer à la suite</button>
        </div>
    </div>

    <script>
        let currentStep = 0;
        let userName = "";
        
        // --- LE PROGRAMME EN 3 ÉTAPES ---
        const fullProgram = [
            // ÉTAPE 1 : GRAMMAIRE DE BASE
            { 
                module: "Étape 1 : Grammaire Fondamentale",
                text: "Commençons par les bases. Les pronoms personnels sont essentiels pour désigner qui parle ou de qui on parle.", 
                rule: "I (Je), You (Tu), He (Il), She (Elle)\\nIt (Chose), We (Nous), They (Ils)" 
            },
            // ÉTAPE 2 : VERBES ÊTRE ET AVOIR
            { 
                module: "Étape 2 : Verbes Être et Avoir",
                text: "Maintenant, le verbe ÊTRE (To Be) pour l'identité et le verbe AVOIR (To Have) pour la possession.", 
                rule: "I am (Je suis) / I have (J'ai)\\nYou are (Tu es) / You have (Tu as)\\nHe/She is (Il/Elle est) / He/She HAS (Il/Elle a)" 
            },
            // ÉTAPE 3 : CONSTRUCTION DE PHRASES SIMPLES
            { 
                module: "Étape 3 : Construction de phrases",
                text: "Utilisons ce que nous avons appris pour créer tes premières phrases simples.", 
                rule: "I am happy. (Je suis heureux)\\nI have a car. (J'ai une voiture)\\nShe is a friend. (Elle est une amie)" 
            },
            { 
                module: "Étape 3 : Construction de phrases",
                text: "Voici comment exprimer un besoin ou une origine.", 
                rule: "I am hungry. (J'ai faim)\\nI have a question. (J'ai une question)\\nI am from France. (Je viens de France)" 
            }
        ];

        function speak(text) {
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = 'fr-FR';
            utter.rate = 1.3;
            window.speechSynthesis.speak(utter);
        }

        function initLesson() {
            document.getElementById('step-level').classList.add('hidden');
            document.getElementById('course-screen').classList.remove('hidden');
            currentStep = 0;
            showStep();
        }

        function showStep() {
            const displayText = document.getElementById('display-text');
            const grammarZone = document.getElementById('grammar-zone');
            const moduleTitle = document.getElementById('module-title');

            if (currentStep < fullProgram.length) {
                const data = fullProgram[currentStep];
                moduleTitle.innerText = data.module;
                displayText.innerText = data.text;
                grammarZone.innerText = data.rule.replace(/\\\\n/g, '\\n');
                speak(data.text);
            } else {
                const fin = "Félicitations " + userName + " ! C'est bien. Tu as validé les 3 étapes de base : Grammaire, Verbes et Phrases simples !";
                moduleTitle.innerText = "PROGRAMME TERMINÉ";
                displayText.innerText = fin;
                grammarZone.innerText = "✅ Félicitations ! Tu es prêt pour le niveau suivant.";
                document.getElementById('next-btn').style.display = 'none';
                speak(fin);
            }
        }

        document.getElementById('next-btn').onclick = () => {
            currentStep++;
            showStep();
        };

        document.getElementById('launch-btn').onclick = function() {
            document.getElementById('welcome-screen').classList.add('hidden');
            document.getElementById('step-name').classList.remove('hidden');
            const intro = "Bonjour ! Je me présente, je m'appelle Clarisse. Ton IA dédiée à l'apprentissage de l'anglais. Et toi, comment t'appelles-tu ?";
            speak(intro);
        };

        document.getElementById('submit-name').onclick = function() {
            userName = document.getElementById('user-name').value;
            if(userName.trim() !== "") {
                document.getElementById('step-name').classList.add('hidden');
                document.getElementById('step-level').classList.remove('hidden');
                const welcome = "Enchantée " + userName + ". Nous allons suivre un programme en 3 étapes. Es-tu prêt ?";
                speak(welcome);
            }
        };
    </script>
</body>
</html>
"""

components.html(clarisse_html, height=750)
