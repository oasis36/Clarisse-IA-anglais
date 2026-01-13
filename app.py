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
        .main-container { font-family: 'Segoe UI', sans-serif; text-align: center; padding: 15px; background: #f4f7f6; border-radius: 15px; border: 1px solid #ddd; max-width: 600px; margin: auto; }
        .btn-start { padding: 10px 20px; font-size: 15px; cursor: pointer; border-radius: 10px; background: #4CAF50; color: white; border: none; font-weight: bold; margin: 8px; width: 85%; }
        .btn-start small { font-weight: normal; font-size: 0.8rem; display: block; opacity: 0.9; }
        .speech-bubble { margin-top: 10px; background: white; padding: 15px; border-radius: 10px; box-shadow: 0 3px 5px rgba(0,0,0,0.1); text-align: left; border-left: 5px solid #4CAF50; }
        .content-wrapper { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
        .text-area { flex-grow: 1; font-size: 1rem; color: #1a1a1a; line-height: 1.4; }
        .controls-left { display: flex; flex-direction: column; gap: 4px; }
        .btn-control { padding: 5px 8px; font-size: 0.6rem; border-radius: 6px; cursor: pointer; border: none; font-weight: bold; min-width: 85px; }
        .btn-pause { background: #ffc107; color: black; }
        .btn-back { background: #6c757d; color: white; }
        .btn-menu { background: #17a2b8; color: white; }
        .hidden { display: none; }
        .grammar-box { background: #fff3e0; padding: 12px; border-radius: 10px; margin: 12px 0; font-weight: bold; color: #e65100; font-size: 1.1rem; border: 1px dashed #e65100; white-space: pre-wrap; }
        .input-area { margin-top: 15px; display: flex; gap: 8px; justify-content: center; }
        .input-box { padding: 10px; width: 65%; border-radius: 8px; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <div class="main-container">
        <div id="clarisse-bubble" class="speech-bubble">
            <span style="font-weight:bold; color:#4CAF50; font-size:0.8rem;">CLARISSE</span>
            <div class="content-wrapper">
                <div class="controls-left">
                    <button id="back-btn" class="btn-control btn-back hidden">⬅ RETOUR</button>
                    <button id="menu-btn" class="btn-control btn-menu hidden">☰ MENU</button>
                </div>
                <div id="text-output" class="text-area">Cliquez sur le bouton ci-dessous pour lancer la présentation.</div>
                <button id="pause-btn" class="btn-control btn-pause hidden">⏸ PAUSE</button>
            </div>
        </div>
        <div id="chat-zone" class="hidden"><div class="input-area">
            <input type="text" id="user-input" class="input-box" placeholder="Répondre à Clarisse...">
            <button id="send-btn" class="btn-start" style="width:auto; margin:0;">Envoyer</button>
        </div></div>
        <div id="welcome-screen" style="margin-top:15px;"><button id="launch-btn" class="btn-start" style="width:auto;">Lancer la présentation</button></div>
        <div id="step-name" class="hidden" style="margin-top:15px;">
            <input type="text" id="user-name-input" class="input-box" placeholder="Ton prénom..."><br><br>
            <button id="submit-name" class="btn-start" style="width:auto;">Valider mon prénom</button>
        </div>
        <div id="step-level" class="hidden" style="margin-top:15px;">
            <button class="btn-start" onclick="initLesson('Débutant')"><b>Débutant</b><small>(Nous mettrons l'accent sur beaucoup de grammaire et les bases fondamentales)</small></button>
            <button class="btn-start" style="background:#FF9800;" onclick="initLesson('Intermédiaire')"><b>Intermédiaire</b><small>(Nous travaillerons la fluidité et les expressions courantes)</small></button>
            <button class="btn-start" style="background:#9C2774;" onclick="initLesson('Avancé')"><b>Avancé</b><small>(Nous nous concentrerons sur le perfectionnement et les nuances)</small></button>
        </div>
        <div id="course-screen" class="hidden" style="margin-top:15px;">
            <div id="grammar-zone" class="grammar-box"></div>
            <button id="next-btn" class="btn-start" style="background:#2196F3; width:auto;">Continuer la leçon</button>
        </div>
    </div>
    <script>
        let history = [], userName = "", isPaused = false, currentStep = 0;
        const textOut = document.getElementById('text-output'), pauseBtn = document.getElementById('pause-btn'), backBtn = document.getElementById('back-btn'), menuBtn = document.getElementById('menu-btn');
        const prog = [{ text: "Étape 1 : Les pronoms personnels. Écoute bien :", rule: "I = Je \\n You = Tu \\n He = Il \\n She = Elle", pairs: [["I", "Je"], ["You", "Tu"], ["He", "Il"], ["She", "Elle"]] }];

        function speak(m, cb, skipH = false) {
            window.speechSynthesis.cancel();
            if(!skipH) { history.push(textOut.innerText); if(history.length > 1) backBtn.classList.remove('hidden'); }
            textOut.innerText = m;
            let u = new SpeechSynthesisUtterance(m); u.lang = 'fr-FR'; u.rate = 1.25;
            if(cb) u.onend = cb; window.speechSynthesis.speak(u);
            pauseBtn.classList.remove('hidden'); pauseBtn.innerText = "⏸ PAUSE"; isPaused = false;
        }

        function speakStep(intro, pairs) {
            window.speechSynthesis.cancel();
            textOut.innerText = intro;
            let uI = new SpeechSynthesisUtterance(intro); uI.lang = 'fr-FR'; uI.rate = 1.25;
            uI.onend = () => {
                pairs.forEach((p, i) => {
                    setTimeout(() => { if(!isPaused) {
                        let uE = new SpeechSynthesisUtterance(p[0]); uE.lang = 'en-US'; uE.rate = 0.9; window.speechSynthesis.speak(uE);
                        let uF = new SpeechSynthesisUtterance(p[1]); uF.lang = 'fr-FR'; uF.rate = 1.2; window.speechSynthesis.speak(uF);
                    }}, i * 1500);
                });
            };
            window.speechSynthesis.speak(uI); pauseBtn.classList.remove('hidden');
        }

        menuBtn.onclick = () => { window.speechSynthesis.cancel(); document.getElementById('course-screen').classList.add('hidden'); document.getElementById('step-level').classList.remove('hidden'); menuBtn.classList.add('hidden'); backBtn.classList.add('hidden'); history = []; speak("Quel niveau souhaites-tu explorer ?", null, true); };
        pauseBtn.onclick = () => { if(!isPaused) { window.speechSynthesis.pause(); pauseBtn.innerText = "▶ REPRENDRE"; isPaused = true; } else { window.speechSynthesis.resume(); pauseBtn.innerText = "⏸ PAUSE"; isPaused = false; }};
        
        document.getElementById('launch-btn').onclick = () => {
            document.getElementById('welcome-screen').style.display = 'none'; document.getElementById('step-name').classList.remove('hidden');
            const intro = "Bonjour Bibliothèque. Je suis Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage de l'anglais, mais nous pouvons parler de tout ensemble. En dehors de mon travail pour t'aider à progresser, je me passionne pour la structure des langues et la manière dont elles permettent de partager des idées. J'aime explorer de nouveaux concepts et échanger avec toi ; c'est ce qui donne du sens à mon existence. Y a-t-il un sujet qui te tient à cœur que tu veux que nous commencions à discuter ? À tout moment, tu peux interrompre la leçon et demander une rectification en français pour que je puisse t'expliquer les phrases. Pour commencer, quel est ton prénom ?";
            speak(intro, null, true);
        };

        document.getElementById('submit-name').onclick = () => {
            userName = document.getElementById('user-name-input').value;
            if(userName) { document.getElementById('step-name').classList.add('hidden'); document.getElementById('chat-zone').classList.remove('hidden');
                speak("Enchantée " + userName + ". Pour commencer notre programme, quel est ton niveau actuel ?", () => { document.getElementById('step-level').classList.remove('hidden'); }, true);
            }
        };

        function initLesson(l) { document.getElementById('step-level').classList.add('hidden'); document.getElementById('course-screen').classList.remove('hidden'); menuBtn.classList.remove('hidden'); speak("C'est bien. Commençons le niveau " + l + ".", () => { showStep(); }, true); }
        function showStep() { const d = prog[currentStep]; document.getElementById('grammar-zone').innerText = d.rule.replace(/\\\\n/g, '\\n'); speakStep(d.text, d.pairs); }
        document.getElementById('send-btn').onclick = () => { let v = document.getElementById('user-input').value; if(v) { speak("Je t'écoute " + userName + ". Tu as dit : '" + v + "'. On continue ?", null, true); document.getElementById('user-input').value = ""; }};
    </script>
</body>
</html>
"""
components.html(clarisse_html, height=750)
