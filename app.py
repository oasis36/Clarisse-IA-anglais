import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Clarisse - English School", layout="centered")

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
        .grammar-box { background: #fff3e0; padding: 15px; border-radius: 10px; margin: 15px 0; font-family: 'Courier New', Courier, monospace; font-weight: bold; color: #e65100; font-size: 1.2rem; white-space: pre-wrap; }
        .step-indicator { color: #888; font-size: 0.9rem; margin-bottom: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="main-container">
        <div id="intro-screen">
            <button id="launch-btn" class="btn-start">Lancer la conversation</button>
        </div>

        <div id="step-name" class="hidden">
            <input type="text" id="user-name" style="padding:10px; width:70%; border-radius:5px; border:1px solid #ccc;" placeholder="Ton prénom...">
            <br>
            <button id="submit-name" class="btn-start">Valider mon prénom</button>
        </div>

        <div id="step-level" class="hidden">
            <p>Bonjour ! Quel est ton niveau actuel ?</p>
            <button class="btn-start" onclick="startLesson('Débutant')">Débutant (Bases & Phrases)</button>
            <button class="btn-start" onclick="startLesson('Intermédiaire')">Intermédiaire</button>
            <button class="btn-start" onclick="startLesson('Avancé')">Avancé</button>
        </div>

        <div id="course-screen" class="hidden">
            <div class="step-indicator" id="progression">Module : Les Piliers de l'Anglais</div>
            <div id="display-text"></div>
            <div id="grammar-zone" class="grammar-box"></div>
            <button id="next-btn" class="btn-start btn-next">Étape Suivante</button>
        </div>
    </div>

    <script>
        let currentStep = 0;
        let userName = "";
        const displayText = document.getElementById('display-text');
        const grammarZone = document.getElementById('grammar-zone');

        function speak(text) {
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = 'fr-FR';
            utter.rate = 1.25;
            window.speechSynthesis.speak(utter);
        }

        // --- PROGRAMME : ÊTRE, AVOIR ET DÉBUTS DE PHRASES ---
        const lessonPlan = [
            { 
                text: "Étape 1 : Le verbe ÊTRE (To Be). Il sert à décrire un état ou une identité. Répète après moi : I am, You are.", 
                rule: "I am (Je suis)\\nYou are (Tu es)\\nHe/She/It is (Il/Elle est)\\nWe are (Nous sommes)\\nThey are (Ils sont)" 
            },
            { 
                text: "Étape 2 : Le verbe AVOIR (To Have). Indispensable pour la possession. Attention à la 3ème personne : He HAS.", 
                rule: "I have (J'ai)\\nYou have (Tu as)\\nHe/She/It HAS (Il/Elle a)\\nWe have (Nous avons)\\nThey have (Ils ont)" 
            },
            { 
                text: "C'est bien ! Maintenant, passons aux débuts de phrases utiles. Pour se présenter ou dire ce qu'on aime.", 
                rule: "I am from... (Je viens de...)\\nI have a... (J'ai un/une...)\\nI like to... (J'aime...)" 
            },
            { 
                text: "Pratiquons ! Voici comment poser une question simple avec le verbe avoir.", 
                rule: "Do you have? (Est-ce que tu as ?)\\nEx: Do you have a dog? (As-tu un chien ?)" 
            },
            { 
                text: "Et voici comment utiliser le verbe être pour décrire une émotion.", 
                rule: "I am happy (Je suis heureux)\\nI am tired (Je suis fatigué)\\nI am hungry (J'ai faim - littéralement: Je suis affamé)" 
            }
        ];

        function startLesson(level) {
            document.getElementById('step-level').classList.add('hidden');
            document.getElementById('course-screen').classList.remove('hidden');
            showStep();
        }

        function showStep() {
            if (currentStep < lessonPlan.length) {
                const data = lessonPlan[currentStep];
                displayText.innerText = data.text;
                grammarZone.innerText = data.rule.replace(/\\\\n/g, '\\n');
                document.getElementById('progression').innerText = "Module Débutant - Étape " + (currentStep + 1) + " / " + lessonPlan.length;
                speak(data.text);
            } else {
                const fin = "C'est bien " + userName + " ! Tu maîtrises maintenant les bases des verbes Être et Avoir, et tu sais former tes premières phrases. Félicitations !";
                displayText.innerText = fin;
                grammarZone.innerText = "Niveau Fondamental Validé ! ✅\\n\\nProchaine leçon : Le Présent Continu !";
                document.getElementById('next-btn').style.display = 'none';
                speak(fin);
            }
        }

        document.getElementById('next-btn').onclick = () => {
            currentStep++;
            showStep();
        };

        document.getElementById('launch-btn').onclick = function() {
            this.parentElement.classList.add('hidden');
            document.getElementById('step-name').classList.remove('hidden');
            const intro = "Bonjour ! Je me présente, je m'appelle Clarisse, ton IA dédiée à l'apprentissage de l'anglais. Et toi, comment t'appelles-tu ?";
            speak(intro);
        };

        document.getElementById('submit-name').onclick = function() {
            userName = document.getElementById('user-name').value;
            if(userName.trim() !== "") {
                document.getElementById('step-name').classList.add('hidden');
                document.getElementById('step-level').classList.remove('hidden');
                const welcome = "C'est un plaisir de faire ta connaissance, " + userName + " ! Quel est ton niveau actuel ?";
                speak(welcome);
            }
        };
    </script>
</body>
</html>
"""

components.html(clarisse_html, height=750)
