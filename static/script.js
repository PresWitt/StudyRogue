$(document).ready(function() {
    // Button click event handlers
    $('#attack-btn').click(function() {
        executeAction('attack');
    });

    $('#defend-btn').click(function() {
        executeAction('defend');
    });

    $('#heal-btn').click(function() {
        executeAction('heal');
    });

    // Update health bars on page load
    updateHealthBars();
});

function executeAction(action) {
    $.ajax({
        url: '/execute_action',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ action: action }),
        success: function(response) {
            $('#game-output').html(response.result);
            $('#player-health').text(response.player_health);
            $('#enemy-health').text(response.enemy_health);
            $('#enemy-name').text(response.enemy_name); // Update enemy name
            $('#enemy-image').attr('src', response.enemy_image); // Update enemy image source
            updateHealthBars();
        }
    });
}

function updateHealthBars() {
    var playerHealth = document.getElementById('player-health').textContent;
    var enemyHealth = document.getElementById('enemy-health').textContent;

    updateHealthBar('player-health-bar', playerHealth);
    updateHealthBar('enemy-health-bar', enemyHealth);
}

function updateHealthBar(barId, health) {
    var barElement = document.getElementById(barId);
    var percentage = (health / 100) * 100; // Calculate health percentage

    // Remove previous color classes
    barElement.classList.remove('green', 'yellow', 'red');

    // Set color based on health percentage
    if (percentage > 66) {
        barElement.classList.add('green');
    } else if (percentage > 33) {
        barElement.classList.add('yellow');
    } else {
        barElement.classList.add('red');
    }

    // Set width of the health bar
    barElement.style.width = percentage + '%';
}
