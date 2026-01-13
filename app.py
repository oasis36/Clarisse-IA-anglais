import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Clarisse - English Learning", layout="centered")
st.write("### 🎓 Clarisse : Parcours d'Apprentissage")

clarisse_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        .main-container { font-family: 'Segoe UI', sans-serif; text-align: center; padding: 15px; background: #f4f7f6; border-radius: 15px; border: 1px solid #ddd; max-width: 600px; margin: auto; }
        .btn-start { padding: 12px 20px; font-size: 15px; cursor: pointer; border-radius: 10px; background: #4CAF50; color: white; border: none; font-weight: bold; margin: 8px; width: 85%; }
        .btn-start small { font-weight: normal; font-size: 0.8rem; display: block; opacity: 0.9; margin-top: 5px; }
        .speech-bubble { margin-top: 15px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: left; border-left: 5px solid #4CAF50; }
        .text-area { font-size: 1.1rem; color: #1a1a1a; line-height: 1.5; margin-bottom: 10px; }
        .controls { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; }
        .btn-ctrl { padding: 6px 12px; font-size: 0.7rem; border-radius: 8px; cursor: pointer; border: none; font-weight: bold; }
        .btn-pause { background: #ffc107; color: black; }
        .btn-menu { background: #17a2b8; color: white; }
        .hidden { display: none; }
        .grammar-box { background: #fff3e0; padding: 15px; border-radius: 10px; margin: 15px 0; font-weight: bold; color: #e65100; font-size: 1.1rem; border: 1px dashed #e65100; white-space: pre-wrap; text-align: left; }
        .btn-next { background: #2196F3; color: white; margin-top: 10px; width: 100%; }
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
            <input type="text" id="user-name-input" style="padding:10px; width:60%; border-radius:8px; border:1px solid #ccc;" placeholder="Ton prénom...">
            <button id="submit-name" class="btn-start" style="width:auto; margin-left:10px;">Valider</button>
        </div>

        <div id="step-level" class="hidden" style="margin-top:20px;">
            <button class="btn-start" onclick="startLevel('Débutant')"><b>Débutant</b><small>(Être, Avoir et Objets)</small></button>
            <button class="btn-start" style="background:#FF9800;" onclick="startLevel('Intermédiaire')"><b>Intermédiaire</b><small>(Actions et Quotidien)</small></button>
            <button class="btn-start" style="background:#9C2774;" onclick="startLevel('Avancé')"><b>Avancé</b><small>(Nuances et Partage d'idées)</small></button>
        </div>

        <div id="course-screen" class="hidden" style="margin-top:20px;">
            <div id="grammar-zone" class="grammar-box"></div>
            <button id="next-btn" class="btn-start btn-next hidden">Passer à la leçon suivante</button>
        </div>
    </div>

    <script>
        let userName = "", currentLevel = "", currentLessonIdx = 0, isPaused = false;
        const textOut = document.getElementById('text-output'), pauseBtn = document.getElementById('pause-btn'), 
              menuBtn = document.getElementById('menu-btn'), nextBtn = document.getElementById('next-btn');

        const syllabus = {
            'Débutant': [
                {
                    intro: "Leçon 1 : Les deux verbes piliers, Être et Avoir.",
                    content: "TO BE (Être) : I am, You are\\nTO HAVE (Avoir) : I have, You have",
                    audio: [["I am", "Je suis"], ["You are", "Tu es"], ["I have", "J'ai"], ["You have", "Tu as"]]
                },
                {
                    intro: "Leçon 2 : Apprenons à désigner les objets qui nous entourent.",
                    content: "A book = Un livre\\nThe key = La clé\\nThis is a car = C'est une voiture",
                    audio: [["A book", "Un livre"], ["The key", "La clé"], ["This is a car", "C'est une voiture"]]
                }
            ],
            'Intermédiaire': [
                {
                    intro: "Leçon 1 : Décrire une action en cours.",
                    content: "I am working = Je travaille\\nHe is sleeping = Il dort",
                    audio: [["I am working", "Je travaille"], ["He is sleeping", "Il dort"]]
                }
            ]
        };

        function speak(text, callback, lang = 'fr-FR') {
            window.speechSynthesis.cancel();
            textOut.innerText = text;
            let utter = new SpeechSynthesisUtterance(text);
            utter.lang = lang; utter.rate = 1.1;
            if (callback) utter.onend = callback;
            window.speechSynthesis.speak(utter);
            pauseBtn.classList.remove('hidden');
        }

        function playLessonAudio(pairs, index = 0) {
            if (index >= pairs.length || isPaused) {
                if(index >= pairs.length) nextBtn.classList.remove('hidden');
                return;
            }
            let eng = new SpeechSynthesisUtterance(pairs[index][0]);
            eng.lang = 'en-US'; eng.rate = 0.9;
            eng.onend = () => {
                setTimeout(() => {
                    let fra = new SpeechSynthesisUtterance(pairs[index][1]);
                    fra.lang = 'fr-FR'; fra.rate = 1.1;
                    fra.onend = () => setTimeout(() => playLessonAudio(pairs, index + 1), 1000);
                    window.speechSynthesis.speak(fra);
                }, 500);
            };
            window.speechSynthesis.speak(eng);
        }

        document.getElementById('launch-btn').onclick = () => {
            document.getElementById('welcome-screen').classList.add('hidden');
            document.getElementById('step-name').classList.remove('hidden');
            speak("Bonjour. Je me présente, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage de l'anglais. Quel est ton prénom ?");
        };

        document.getElementById('submit-name').onclick = () => {
            userName = document.getElementById('user-name-input').value;
            if(userName) {
                document.getElementById('step-name').classList.add('hidden');
                speak("Enchantée " + userName + ". Quel est ton niveau actuel ?", () => { document.getElementById('step-level').classList.remove('hidden'); });
            }
        };

        function startLevel(level) {
            currentLevel = level;
            currentLessonIdx = 0;
            loadLesson();
        }

        function loadLesson() {
            document.getElementById('step-level').classList.add('hidden');
            document.getElementById('course-screen').classList.remove('hidden');
            nextBtn.classList.add('hidden');
            menuBtn.classList.remove('hidden');
            
            const lesson = syllabus[currentLevel][currentLessonIdx];
            document.getElementById('grammar-zone').innerText = lesson.content.replace(/\\\\n/g, '\\n');
            speak(lesson.intro, () => playLessonAudio(lesson.audio));
        }

        nextBtn.onclick = () => {
            currentLessonIdx++;
            if(currentLessonIdx < syllabus[currentLevel].length) {
                loadLesson();
            } else {
                speak("Félicitations " + userName + " ! Tu as terminé ce module.");
                nextBtn.classList.add('hidden');
            }
        };

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
