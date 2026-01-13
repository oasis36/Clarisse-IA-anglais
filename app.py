<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Programme Clarisse - Anglais</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f4f7f6; margin: 0; }
        #chat-container { background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; max-width: 500px; width: 90%; }
        button { padding: 15px 30px; font-size: 18px; cursor: pointer; border-radius: 10px; background-color: #4CAF50; color: white; border: none; transition: background 0.3s; }
        button:hover { background-color: #45a049; }
        input { padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 15px; width: 80%; }
        .hidden { display: none; }
        #message-display { font-size: 1.1rem; color: #333; line-height: 1.5; margin-top: 20px; }
        .level-btn { background-color: #008CBA; margin: 5px; font-size: 14px; }
    </style>
</head>
<body>

<div id="chat-container">
    <button id="btn-lancer">Lancer la conversation</button>

    <div id="etape-nom" class="hidden">
        <p id="phrase-intro"></p>
        <input type="text" id="input-nom" placeholder="Ton nom ici...">
        <br>
        <button id="btn-valider-nom">Valider</button>
    </div>

    <div id="etape-niveau" class="hidden">
        <p id="phrase-accueil"></p>
        <div id="boutons-niveaux">
            <button class="level-btn" onclick="choisirNiveau('Débutant')">Débutant</button>
            <button class="level-btn" onclick="choisirNiveau('Intermédiaire')">Intermédiaire</button>
            <button class="level-btn" onclick="choisirNiveau('Avancé')">Avancé</button>
        </div>
    </div>

    <div id="message-display"></div>
</div>

<script>
    const btnLancer = document.getElementById('btn-lancer');
    const etapeNom = document.getElementById('etape-nom');
    const etapeNiveau = document.getElementById('etape-niveau');
    const inputNom = document.getElementById('input-nom');
    const btnValiderNom = document.getElementById('btn-valider-nom');
    const messageDisplay = document.getElementById('message-display');

    function parler(texte) {
        const synthese = window.speechSynthesis;
        const phrase = new SpeechSynthesisUtterance(texte);
        phrase.lang = 'fr-FR';
        synthese.speak(phrase);
    }

    // --- PREMIER TEMPS ---
    btnLancer.addEventListener('click', () => {
        btnLancer.classList.add('hidden');
        etapeNom.classList.remove('hidden');
        const txt = "Bonjour ! Je suis Clarisse, ton IA dédiée à l'apprentissage de l'anglais. Et toi, comment t'appelles-tu ?";
        messageDisplay.innerText = txt;
        parler(txt);
    });

    // --- DEUXIÈME TEMPS ---
    btnValiderNom.addEventListener('click', () => {
        const nom = inputNom.value;
        if(nom) {
            etapeNom.classList.add('hidden');
            etapeNiveau.classList.remove('hidden');
            
            const accueil = C'est un plaisir de faire ta connaissance, ${nom} ! Sache que nous pouvons parler de tout ensemble. Mon but est de t'aider à progresser. À tout moment, tu peux m'interrompre en français pour me demander une explication sur une phrase. Pour commencer notre programme, quel est ton niveau actuel ?;
            
            messageDisplay.innerText = accueil;
            parler(accueil);
        }
    });

    function choisirNiveau(niveau) {
        alert("Niveau choisi : " + niveau + ". Le programme va commencer !");
    }
</script>

</body>
</html>
