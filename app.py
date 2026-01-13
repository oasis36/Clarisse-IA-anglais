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
        .btn-start { padding: 12px 25px; font-size: 15px; cursor: pointer; border-radius: 10px; background-color: #4CAF50; color: white; border: none; font-weight: bold; margin: 10px; display: inline-block; width: 85%; }
        .btn-next { background-color: #2196F3; width: auto; }
        .hidden { display: none; }
        .speech-bubble { margin-top: 15px; font-size: 1.1rem; color: #1a1a1a; line-height: 1.5; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); min-height: 60px; text-align: left; border-left: 6px solid #4CAF50; }
        .grammar-box { background: #fff3e0; padding: 15px; border-radius: 10px; margin: 15px 0; font-family: 'Segoe UI', sans-serif; font-weight: bold; color: #e65100; font-size: 1.2rem; white-space: pre-wrap; text-align: center; border: 1px dashed #e65100; }
        .clarisse-label { font-weight: bold; color: #4CAF50; text-transform: uppercase; font-size: 0.8rem; }
    </style>
</head>
<body>
    <div class="main-container">
        <div id="clarisse-bubble" class="speech-bubble">
            <span class="clarisse-label">Clarisse :</span>
            <span id="text-output">Cliquez pour lancer la présentation.</span>
        </div>

        <div id="welcome-screen" style="margin-top:20px;">
            <button id="launch-btn" class="btn-start" style="width:auto;">Lancer la conversation</button>
        </div>

        <div id="step-name" class="hidden" style="margin-top:20px;">
            <input type="text" id="user-name" style="padding:12px; width:70%; border-radius:8px; border:1px solid #ccc;" placeholder="Ton prénom...">
            <br><br>
            <button id="submit-name" class="btn-start" style="width:auto;">Valider mon prénom</button>
        </div>

        <div id="step-level" class="hidden" style="margin-top:20px;">
            <button class="btn-start" onclick="initLesson('Débutant')"><b>Débutant</b><br><small>(Grammaire et bases fondamentales)</small></button>
            <button class="btn-start" style="background-color: #FF9800;" onclick="initLesson('Intermédiaire')"><b>Intermédiaire</b><br><small>(Fluidité et expressions courantes)</small></button>
            <button class="btn-start" style="background-color: #9C2774;" onclick="initLesson('Avancé')"><b>Avancé</b><br><small>(Perfectionnement et nuances)</small></button>
        </div>

        <div id="course-screen" class="hidden" style="margin-top:20px;">
            <div id="grammar-zone" class="grammar-box"></div>
            <button id="next-btn" class="btn-start btn-next">Continuer la leçon</button>
        </div>
    </div>

    <script>
        let currentStep = 0;
        let userName = "";
        const textOutput = document.getElementById('text-output');
        
        const fullProgram = [
            { 
                text: "Étape 1 : Les pronoms personnels. Je te donne le mot anglais et sa traduction :", 
                rule: "I = Je \\n You = Tu \\n He = Il \\n She = Elle \\n We = Nous \\n They = Ils",
                pairs: [["I", "Je"], ["You", "Tu"], ["He", "Il"], ["She", "Elle"], ["We", "Nous"], ["They", "Ils"]]
            },
            { 
                text: "Étape 2 : Les verbes Être et Avoir :", 
                rule: "I am = Je suis \\n I have = J'ai \\n You are = Tu es \\n You have = Tu as",
                pairs: [["I am", "Je suis"], ["I have", "J'ai"], ["You are", "Tu es"], ["You have", "Tu as"]]
            }
        ];

        function speakText(msg, onEndCallback) {
            window.speechSynthesis.cancel();
            textOutput.innerText = msg;
            const utter = new SpeechSynthesisUtterance(msg);
            utter.lang = 'fr-FR';
            utter.rate = 1.25; 
            if (onEndCallback) utter.onend = onEndCallback;
            window.speechSynthesis.speak(utter);
        }

        function speakStep(frIntro, pairs) {
            window.speechSynthesis.cancel();
            textOutput.innerText = frIntro;
            const utterIntro = new SpeechSynthesisUtterance(frIntro);
            utterIntro.lang = 'fr-FR';
            utterIntro.rate = 1.25; 
            
            utterIntro.onend = function() {
                pairs.forEach((pair, index) => {
                    setTimeout(() => {
                        const utterEN = new SpeechSynthesisUtterance(pair[0]);
                        utterEN.lang = 'en-US';
                        utterEN.rate = 0.9;
                        window.speechSynthesis.speak(utterEN);

                        const utterFR = new SpeechSynthesisUtterance("veut dire " + pair[1]);
                        utterFR.lang = 'fr-FR';
                        utterFR.rate = 1.25;
                        window.speechSynthesis.speak(utterFR);
                    }, index * 320); 
                });
            };
            window.speechSynthesis.speak(utterIntro);
        }

        document.getElementById('launch-btn').onclick = function() {
            document.getElementById('welcome-screen').style.display = 'none';
            document.getElementById('step-name').classList.remove('hidden');
            speakText("Bonjour. Je me présente, je m'appelle Clarisse. Je suis ton IA dédiée à ton programme d'apprentissage de l'anglais, mais nous pouvons parler de tout ensemble. Pour commencer, comment t'appelles-tu ?");
        };

        document.getElementById('submit-name').onclick = function() {
            userName = document.getElementById('user-name').value;
            if(userName.trim() !== "") {
                document.getElementById('step-name').classList.add('hidden');
                const phraseAccueil = "Enchantée " + userName + ". Y a-t-il un sujet qui te tient à cœur que tu veux que nous commencions à discuter ? À tout moment, tu peux interrompre la leçon et demander une rectification en français pour que je puisse t'expliquer les phrases. Pour commencer notre programme, quel est ton niveau actuel ?";
                speakText(phraseAccueil, function() {
                    document.getElementById('step-level').classList.remove('hidden');
                });
            }
        };

        function initLesson(level) {
            document.getElementById('step-level').classList.add('hidden');
            document.getElementById('course-screen').classList.remove('hidden');
            speakStep("C'est noté. Commençons le niveau " + level + ".", []);
            showStep();
        }

        function showStep() {
            const grammarZone = document.getElementById('grammar-zone');
            if (currentStep < fullProgram.length) {
                const data = fullProgram[currentStep];
                grammarZone.innerText = data.rule.replace(/\\\\n/g, '\\n');
                speakStep(data.text, data.pairs);
            } else {
                const fin = "Félicitations " + userName + " ! C'est bien.";
                grammarZone.innerText = "✅ Session terminée !";
                document.getElementById('next-btn').style.display = 'none';
                speakStep(fin, []);
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

components.html(clarisse_html, height=800)
E
