import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Clarisse - English Learning", layout="centered")
st.write("### 🎓 Clarisse : Programme d'Apprentissage")

clarisse_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        .main-container { font-family: 'Segoe UI', sans-serif; text-align: center; padding: 15px; background: #f4f7f6; border-radius: 15px; border: 1px solid #ddd; max-width: 600px; margin: auto; }
        .btn-start { padding: 12px 20px; font-size: 15px; cursor: pointer; border-radius: 10px; background: #4CAF50; color: white; border: none; font-weight: bold; margin: 8px; width: 85%; }
        .btn-start small { font-weight: normal; font-size: 0.8rem; display: block; opacity: 0.9; margin-top: 5px; }
        .speech-bubble { margin-top: 15px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: left; border-left: 6px solid #4CAF50; }
        .text-area { font-size: 1.1rem; color: #1a1a1a; line-height: 1.5; margin-bottom: 10px; }
        .controls { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; }
        .btn-ctrl { padding: 6px 12px; font-size: 0.7rem; border-radius: 8px; cursor: pointer; border: none; font-weight: bold; }
        .btn-pause { background: #ffc107; color: black; }
        .btn-menu { background: #17a2b8; color: white; }
        .hidden { display: none; }
        .grammar-box { background: #fff3e0; padding: 15px; border-radius: 10px; margin: 15px 0; font-weight: bold; color: #e65100; font-size: 1.2rem; border: 1px dashed #e65100; white-space: pre-wrap; }
        .input-area { margin-top: 20px; display: flex; gap: 10px; justify-content: center; }
        .input-box { padding: 12px; width: 65%; border-radius: 8px; border: 1px solid #ccc; font-size: 1rem; }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="speech-bubble">
            <div style="color: #4CAF50; font-weight: bold; font-size: 0.8rem; margin-bottom: 8px;">CLARISSE</div>
            <div id="text-output" class="text-area">Prête pour la présentation.</div>
            <div class="controls">
                <button id="menu-btn" class="btn-ctrl btn-menu hidden">☰ Menu</button>
                <button id="pause-btn" class="btn-ctrl btn-pause hidden">⏸ Pause</button>
            </div>
        </div>

        <div id="welcome-screen" style="margin-top:20px;">
            <button id="launch-btn" class="btn-start" style="width:auto;">Lancer la présentation</button>
        </div>

        <div id="step-name" class="hidden" style="margin-top:20px;">
            <input type="text" id="user-name-input" class="input-box" placeholder="Tape ton prénom ici...">
            <button id="submit-name" class="btn-start" style="width:auto; margin-left:10px;">Valider</button>
        </div>

        <div id="step-level" class="hidden" style="margin-top:20px;">
            <button class="btn-start" onclick="initLesson('Débutant')"><b>Débutant</b><small>(Accent sur la grammaire et les bases fondamentales)</small></button>
            <button class="btn-start" style="background:#FF9800;" onclick="initLesson('Intermédiaire')"><b>Intermédiaire</b><small>(Fluidité et expressions courantes)</small></button>
            <button class="btn-start" style="background:#9C2774;" onclick="initLesson('Avancé')"><b>Avancé</b><small>(Perfectionnement et nuances)</small></button>
        </div>

        <div id="course-screen" class="hidden" style="margin-top:20px;">
            <div id="grammar-zone" class="grammar-box"></div>
        </div>
    </div>

    <script>
        let userName = "", isPaused = false;
        const textOut = document.getElementById('text-output'), pauseBtn = document.getElementById('pause-btn'), menuBtn = document.getElementById('menu-btn');

        function speak(text, callback) {
            window.speechSynthesis.cancel();
            textOut.innerText = text;
            let utter = new SpeechSynthesisUtterance(text);
            utter.lang = 'fr-FR'; utter.rate = 1.1;
            if (callback) utter.onend = callback;
            window.speechSynthesis.speak(utter);
            pauseBtn.classList.remove('hidden');
        }

        // ÉTAPE 1 : Présentation et demande du prénom
        document.getElementById('launch-btn').onclick = () => {
            document.getElementById('welcome-screen').classList.add('hidden');
            document.getElementById('step-name').classList.remove('hidden');
            const intro = "Bonjour. Je me présente, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage de l'anglais. Quel est ton prénom ?";
            speak(intro);
        };

        // ÉTAPE 2 : Accueil personnalisé et choix du niveau
        document.getElementById('submit-name').onclick = () => {
            userName = document.getElementById('user-name-input').value;
            if(userName) {
                document.getElementById('step-name').classList.add('hidden');
                const suite = "Je suis ravie de faire ta connaissance, " + userName + ". Sache que nous pouvons parler de tout ensemble. En dehors de mon travail pour t'aider à progresser, j'aime explorer de nouveaux concepts et échanger avec toi ; c'est ce qui donne du sens à mon existence. Y a-t-il un sujet qui te tient à cœur que tu veux que nous commencions à discuter ? À tout moment, tu peux interrompre la leçon et demander une rectification en français pour que je puisse t'expliquer les phrases. Pour commencer notre programme, quel est ton niveau actuel ?";
                
                speak(suite, () => {
                    document.getElementById('step-level').classList.remove('hidden');
                });
            }
        };

        function initLesson(level) {
            document.getElementById('step-level').classList.add('hidden');
            document.getElementById('course-screen').classList.remove('hidden');
            menuBtn.classList.remove('hidden');
            speak("C'est bien " + userName + ". Commençons le niveau " + level + ".", () => {
                document.getElementById('grammar-zone').innerText = "Leçon 1 : Les bases\\nI = Je\\nYou = Tu";
            });
        }

        pauseBtn.onclick = () => {
            if (!isPaused) { window.speechSynthesis.pause(); pauseBtn.innerText = "▶"; isPaused = true; }
            else { window.speechSynthesis.resume(); pauseBtn.innerText = "⏸"; isPaused = false; }
        };
        
        menuBtn.onclick = () => {
            window.speechSynthesis.cancel();
            document.getElementById('course-screen').classList.add('hidden');
            document.getElementById('step-level').classList.remove('hidden');
        };
    </script>
</body>
</html>
"""
components.html(clarisse_html, height=800)
