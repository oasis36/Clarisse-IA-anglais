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
        .btn-start { padding: 15px 30px; font-size: 18px; cursor: pointer; border-radius: 10px; background-color: #4CAF50; color: white; border: none; }
        .input-field { padding: 12px; font-size: 16px; margin: 15px; border-radius: 5px; border: 1px solid #ccc; width: 80%; }
        .hidden { display: none; }
        #display-text { margin-top: 20px; font-size: 1.2rem; color: #333; line-height: 1.6; text-align: left; }
        .level-btn { padding: 10px 20px; margin: 10px; cursor: pointer; background-color: #008CBA; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="main-container">
        <button id="launch-btn" class="btn-start">Lancer la conversation</button>

        <div id="step-1" class="hidden">
            <input type="text" id="user-name" class="input-field" placeholder="Entrez votre prénom...">
            <br>
            <button id="submit-name" class="btn-start" style="font-size: 14px;">Valider</button>
        </div>

        <div id="step-2" class="hidden">
            <div id="levels-container">
                <button class="level-btn" onclick="alert('Niveau Débutant sélectionné')">Débutant</button>
                <button class="level-btn" onclick="alert('Niveau Intermédiaire sélectionné')">Intermédiaire</button>
                <button class="level-btn" onclick="alert('Niveau Avancé sélectionné')">Avancé</button>
            </div>
        </div>

        <div id="display-text"></div>
    </div>

    <script>
        const displayText = document.getElementById('display-text');
        
        let voices = [];
        function loadVoices() { voices = window.speechSynthesis.getVoices(); }
        window.speechSynthesis.onvoiceschanged = loadVoices;
        loadVoices();

        // FONCTION POUR UNE VOIX PLUS HUMAINE
        async function speakNatural(text) {
            window.speechSynthesis.cancel();
            
            // On sépare par phrases pour gérer le rythme
            const parts = text.split(/([.!?;])/);
            
            for (let i = 0; i < parts.length; i++) {
                if (parts[i].trim().length === 0) continue;

                const utter = new SpeechSynthesisUtterance(parts[i]);
                const frenchVoice = voices.find(v => v.lang.includes('fr') && (v.name.includes('Google') || v.name.includes('Premium'))) || voices.find(v => v.lang.includes('fr'));
                
                if (frenchVoice) utter.voice = frenchVoice;
                
                utter.lang = 'fr-FR';
                // Rythme dynamique : plus rapide sur le texte, mais pauses nettes
                utter.rate = 1.15; 
                utter.pitch = 1.0;

                window.speechSynthesis.speak(utter);

                // On force une pause de 600ms après chaque point/ponctuation pour "respirer"
                await new Promise(resolve => {
                    utter.onend = () => setTimeout(resolve, 600);
                });
            }
        }

        document.getElementById('launch-btn').onclick = function() {
            this.style.display = 'none';
            document.getElementById('step-1').classList.remove('hidden');
            const intro = "Bonjour ! Je suis Clarisse, ton IA dédiée à l'apprentissage de l'anglais. Et toi, comment t'appelles-tu ?";
            displayText.innerText = intro;
            speakNatural(intro);
        };

        document.getElementById('submit-name').onclick = function() {
            const name = document.getElementById('user-name').value;
            if(name.trim() !== "") {
                document.getElementById('step-1').classList.add('hidden');
                document.getElementById('step-2').classList.remove('hidden');
                const welcome = "C'est un plaisir de faire ta connaissance, " + name + " ! Sache que nous pouvons parler de tout ensemble. Mon but est de t'aider à progresser. À tout moment, tu peux m'interrompre en français pour me demander une explication sur une phrase. Pour commencer notre programme, quel est ton niveau actuel ?";
                displayText.innerText = welcome;
                speakNatural(welcome);
            }
        };
    </script>
</body>
</html>
"""

components.html(clarisse_html, height=600)
