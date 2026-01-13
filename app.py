import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Clarisse - English Learning", layout="centered")

st.write("### 🎓 Programme d'Apprentissage avec Clarisse")

clarisse_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        .main-container { font-family: 'Segoe UI', sans-serif; text-align: center; padding: 20px; background-color: #f4f7f6; border-radius: 15px; border: 1px solid #ddd; max-width: 650px; margin: auto; }
        .btn-start { padding: 12px 25px; font-size: 15px; cursor: pointer; border-radius: 10px; background-color: #4CAF50; color: white; border: none; font-weight: bold; margin: 10px; display: inline-block; width: 85%; line-height: 1.2; }
        .btn-start small { font-weight: normal; font-size: 0.85rem; display: block; margin-top: 4px; opacity: 0.9; }
        
        .speech-bubble { margin-top: 15px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: left; border-left: 6px solid #4CAF50; }
        
        .content-wrapper { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
        .text-area { flex-grow: 1; font-size: 1.1rem; color: #1a1a1a; line-height: 1.4; padding: 0 5px; }
        
        .controls-left { display: flex; flex-direction: column; gap: 5px; }
        
        .btn-control { padding: 6px 10px; font-size: 0.65rem; border-radius: 8px; cursor: pointer; border: none; font-weight: bold; white-space: nowrap; transition: 0.2s; min-width: 90px; }
        .btn-pause { background-color: #ffc107; color: black; min-width: 80px; }
        .btn-back { background-color: #6c757d; color: white; }
        .btn-menu { background-color: #17a2b8; color: white; }
        .btn-control:hover { opacity: 0.8; }
        
        .hidden { display: none; }
        .grammar-box { background: #fff3e0; padding: 15px; border-radius: 10px; margin: 15px 0; font-family: 'Segoe UI', sans-serif; font-weight: bold; color: #e65100; font-size: 1.2rem; white-space: pre-wrap; text-align: center; border: 1px dashed #e65100; }
        .clarisse-label { font-weight: bold; color: #4CAF50; text-transform: uppercase; font-size: 0.8rem; display: block; margin-bottom: 8px; }
        
        .input-area { margin-top: 20px; display: flex; gap: 10px; justify-content: center; }
        .input-box { padding: 12px; width: 70%; border-radius: 8px; border: 1px solid #ccc; font-size: 1rem; }
    </style>
</head>
<body>
    <div class="main-container">
        <div id="clarisse-bubble" class="speech-bubble">
            <span class="clarisse-label">Clarisse</span>
            <div class="content-wrapper">
                <div class="controls-left">
                    <button id="back-btn" class="btn-control btn-back hidden">⬅ RETOUR</button>
                    <button id="menu-btn" class="btn-control btn-menu hidden">☰ MENU</button>
                </div>
                <div id="text-output" class="text-area">Cliquez pour lancer la présentation.</div>
                <button id="pause-btn" class="btn-control btn-pause hidden">⏸ PAUSE</button>
            </div>
        </div>

        <div id="chat-zone" class="hidden">
            <div class="input-area">
                <input type="text" id="user-input" class="input-box" placeholder="Lui dire quelque chose...">
                <button id="send-btn" class="btn-start" style="width:auto; margin:0;">Envoyer</button>
            </div>
        </div>

        <div id="welcome-screen" style="margin-top:20px;">
            <button id="launch-btn" class="btn-start" style="width:auto;">Lancer la conversation</button>
        </div>

        <div id="step-name" class="hidden" style="margin-top:20px;">
            <input type="text" id="user-name-input" class="input-box" placeholder="Ton prénom...">
            <br><br>
            <button id="submit-name" class="btn-start" style="width:auto;">Valider mon prénom</button>
        </div>

        <div id="step-level" class="hidden" style="margin-top:20px;">
            <button class="btn-start" onclick="initLesson('Débutant')">
                <b>Débutant</b>
                <small>(Accent sur la grammaire et les bases fondamentales)</small>
            </button>
            <button class="btn-start" style="background-color: #FF9800;" onclick="initLesson('Intermédiaire')">
                <b>Intermédiaire</b>
                <small>(Fluidité et expressions courantes)</small>
            </button>
            <button class="btn-start" style="background-color: #9C2774;" onclick="initLesson('Avancé')">
                <b>Avancé</b>
                <small>(Perfectionnement et nuances)</small>
            </button>
        </div>

        <div id="course-screen" class="hidden" style="margin-top:20px;">
            <div id="grammar-zone" class="grammar-box"></div>
            <button id="next-btn" class="btn-start" style="background-color: #2196F3; width:auto;">Continuer la leçon</button>
        </div>
    </div>

    <script>
        let history = []; 
        let userName = "";
        let isPaused = false;
        const textOutput = document.getElementById('text-output');
        const pauseBtn = document.getElementById('pause-btn');
        const backBtn = document.getElementById('back-btn');
        const menuBtn = document.getElementById('menu-btn');

        function speakText(msg, onEndCallback, skipHistory = false) {
            window.speechSynthesis.cancel();
            if (!skipHistory && msg !== textOutput.innerText) {
                history.push(textOutput.innerText);
                if (history.length > 1) backBtn.classList.remove('hidden');
            }
            
            textOutput.innerText = msg;
            const utter = new SpeechSynthesisUtterance(msg);
            utter.lang = 'fr-FR';
            utter.rate = 1.25; 
            if (onEndCallback) utter.onend = onEndCallback;
            window.speechSynthesis.speak(utter);
            
            pauseBtn.classList.remove('hidden');
            pauseBtn.innerText = "⏸ PAUSE";
            isPaused = false;
        }

        menuBtn.onclick = function() {
            window.speechSynthesis.cancel();
            document.getElementById('course-screen').classList.add('hidden');
            document.getElementById('step-level').classList.remove('hidden');
            menuBtn.classList.add('hidden');
            backBtn.classList.add('hidden');
            history = [];
            speakText("D'accord, revenons au choix du programme. Quel niveau préfères-tu ?", null, true);
        };

        backBtn.onclick = function() {
            if (history.length > 0) {
                const previousText = history.pop();
                speakText(previousText, null, true);
                if (history.length <= 1) backBtn.classList.add('hidden');
            }
        };

        pauseBtn.onclick = function() {
            if (!isPaused) {
                window.speechSynthesis.pause();
                pauseBtn.innerText = "▶ REPRENDRE";
                isPaused = true;
            } else {
                window.speechSynthesis.resume();
                pauseBtn.innerText = "⏸ PAUSE";
                isPaused = false;
            }
        };

        document.getElementById('send-btn').onclick = function() {
            const val = document.getElementById('user-input').value;
            if(val.trim() !== "") {
                speakText("D'accord " + userName + ", je t'écoute. Tu me dis : '" + val + "'. On en discute ou tu préfères continuer ?", null, true);
                document.getElementById('user-input').value = "";
            }
        };

        document.getElementById('launch-btn').onclick = function() {
            document.getElementById('welcome-screen').style.display = 'none';
            document.getElementById('step-name').classList.remove('hidden');
            speakText("Bonjour. Je me présente, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage de l'anglais, mais nous pouvons parler de tout ensemble. Pour commencer, comment t'appelles-tu ?", null, true);
        };

        document.getElementById('submit-name').onclick = function() {
            userName = document.getElementById('user-name-input').value;
            if(userName.trim() !== "") {
                document.getElementById('step-name').classList.add('hidden');
                document.getElementById('chat-zone').classList.remove('hidden');
                const phrase = "Enchantée " + userName + ". Y a-t-il un sujet qui te tient à cœur ? À tout moment, tu peux m'interrompre, revenir en arrière ou changer de niveau. Quel est ton niveau actuel ?";
                speakText(phrase, function() {
                    document.getElementById('step-level').classList.remove('hidden');
                }, true);
            }
        };

        function initLesson(level) {
            document.getElementById('step-level').classList.add('hidden');
            document.getElementById('course-screen').classList.remove('hidden');
            menuBtn.classList.remove('hidden');
            speakText("C'est noté. Commençons le niveau " + level + ".", function() { showStep(); }, true);
        }

        function showStep() {
            const grammarZone = document.getElementById('grammar-zone');
            grammarZone.innerText = "I = Je \\n You = Tu \\n He = Il \\n She = Elle";
            speakText("Voici les premiers pronoms personnels. Écoute bien la prononciation.");
        }
    </script>
</body>
</html>
"""

components.html(clarisse_html, height=800)
