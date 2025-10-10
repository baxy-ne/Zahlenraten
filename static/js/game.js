// Spiel-Logik für Zahlenraten

let gameActive = false;

// Spiel starten
async function startGame() {
    try {
        const response = await fetch('/api/game/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            gameActive = true;
            document.getElementById('game-status').textContent = data.message;
            document.getElementById('guess-input').disabled = false;
            document.getElementById('guess-button').disabled = false;
            document.getElementById('start-button').disabled = true;
            document.getElementById('guess-input').focus();
            document.getElementById('attempts-list').innerHTML = '';
        } else {
            alert('Fehler: ' + data.message);
        }
    } catch (error) {
        console.error('Fehler beim Starten des Spiels:', error);
        alert('Fehler beim Starten des Spiels');
    }
}

// Rate-Versuch senden
async function makeGuess() {
    const guessInput = document.getElementById('guess-input');
    const guess = guessInput.value;
    
    if (!guess) {
        alert('Bitte gib eine Zahl ein!');
        return;
    }
    
    try {
        const response = await fetch('/api/game/guess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ guess: parseInt(guess) })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            // Nachricht anzeigen
            document.getElementById('game-status').textContent = data.message;
            
            // Versuch zur Liste hinzufügen
            const attemptsList = document.getElementById('attempts-list');
            const attemptItem = document.createElement('li');
            attemptItem.textContent = `Versuch ${data.versuche}: ${guess} - ${getResultText(data.result)}`;
            attemptItem.className = `attempt-${data.result}`;
            attemptsList.appendChild(attemptItem);
            
            // Input leeren
            guessInput.value = '';
            
            // Wenn gewonnen, Spiel beenden
            if (data.result === 'correct') {
                gameActive = false;
                document.getElementById('guess-input').disabled = true;
                document.getElementById('guess-button').disabled = true;
                document.getElementById('start-button').disabled = false;
                document.getElementById('start-button').textContent = 'Neues Spiel starten';
                
                // Highscores neu laden
                setTimeout(() => {
                    loadHighscores();
                }, 500);
            } else {
                guessInput.focus();
            }
        } else {
            alert('Fehler: ' + data.message);
        }
    } catch (error) {
        console.error('Fehler beim Raten:', error);
        alert('Fehler beim Raten');
    }
}

// Hilfsfunktion für Ergebnis-Text
function getResultText(result) {
    switch(result) {
        case 'too_low': return '📈 Zu niedrig';
        case 'too_high': return '📉 Zu hoch';
        case 'correct': return '🎉 Richtig!';
        default: return '';
    }
}

// Highscores laden
async function loadHighscores() {
    try {
        const response = await fetch('/api/highscores');
        const data = await response.json();
        
        if (data.status === 'success') {
            const highscoresList = document.getElementById('highscores-list');
            highscoresList.innerHTML = '';
            
            if (data.highscores.length === 0) {
                highscoresList.innerHTML = '<li>Noch keine Highscores vorhanden</li>';
            } else {
                data.highscores.forEach((score, index) => {
                    const scoreItem = document.createElement('li');
                    scoreItem.textContent = `${index + 1}. ${score.username}: ${score.versuche} Versuche`;
                    if (index === 0) {
                        scoreItem.className = 'top-score';
                    }
                    highscoresList.appendChild(scoreItem);
                });
            }
        }
    } catch (error) {
        console.error('Fehler beim Laden der Highscores:', error);
    }
}

// Event Listener
document.addEventListener('DOMContentLoaded', function() {
    // Start-Button
    const startButton = document.getElementById('start-button');
    if (startButton) {
        startButton.addEventListener('click', startGame);
    }
    
    // Guess-Button
    const guessButton = document.getElementById('guess-button');
    if (guessButton) {
        guessButton.addEventListener('click', makeGuess);
    }
    
    // Enter-Taste im Input-Feld
    const guessInput = document.getElementById('guess-input');
    if (guessInput) {
        guessInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !guessInput.disabled) {
                makeGuess();
            }
        });
    }
    
    // Highscores beim Laden der Seite laden
    loadHighscores();
});