from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

class Character:
    def __init__(self, name, health, image):
        self.name = name
        self.health = health
        self.attack_power = 0
        self.defense_power = 0
        self.image = image

    def attack(self, target):
        if isinstance(target, Character):
            attack_damage = max(0, self.attack_power - target.defense_power)
            target.health -= attack_damage
            return attack_damage
        else:
            return 0

    def defend(self):
        return self.defense_power

    def heal(self):
        heal_amount = random.randint(5, 10)
        self.health = min(100, self.health + heal_amount)  # Cap at maximum health of 100
        return heal_amount

def get_random_enemy():
    enemy_names = ["Chicken", "Goblin", "Skeleton", "Assassin"]
    enemy_name = random.choice(enemy_names)
    enemy_image = f"static/{enemy_name.lower()}.png"  # Generate image filename
    
    if enemy_name == "Chicken":
        return Character(enemy_name, 25, enemy_image)
    
    if enemy_name == "Goblin":
        return Character(enemy_name, 50, enemy_image)
    
    if enemy_name == "Skeleton":
        return Character(enemy_name, 75, enemy_image)
    
    if enemy_name == "Assassin":
        return Character(enemy_name, 100, enemy_image)


player = Character("Player", 100, "")
enemy = get_random_enemy()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute_action', methods=['POST'])
def execute_action():
    global enemy

    data = request.get_json()
    action = data["action"]

    result = ""
    # Player's turn
    if action == "attack":
        player.defense_power = 0
        player.attack_power = random.randint(1, 10)
        result += f"Player attacks with {player.attack_power} power!<br>"
    elif action == "defend":
        player.attack_power = 0
        player.defense_power = random.randint(1, 10)
        result += f"Player defends with {player.defense_power} power!<br>"
    elif action == "heal":
        player.defense_power = 0
        player.attack_power = 0
        heal_amount = player.heal()
        result += f"Player heals for {heal_amount} health.<br>"

    # Enemy's turn
    enemy_action = random.choice(["attack", "defend"])
    if enemy_action == "attack":

        if enemy.name == "Chicken":
            enemy.defense_power = 0
            enemy.attack_power = random.randint(1, 2)
        if enemy.name == "Goblin":
            enemy.defense_power = 0
            enemy.attack_power = random.randint(1, 5)
        if enemy.name == "Skeleton":
            enemy.defense_power = 0
            enemy.attack_power = random.randint(1, 8)
        if enemy.name == "Assassin":
            enemy.defense_power = 0
            enemy.attack_power = random.randint(1, 10)

        result += f"{enemy.name} attacks with {enemy.attack_power} power!<br>"
        
    else:

        if enemy.name == "Chicken":
            enemy.attack_power = 0
            enemy.defense_power = random.randint(1, 2)
        if enemy.name == "Goblin":
            enemy.attack_power = 0
            enemy.defense_power = random.randint(1, 5)
        if enemy.name == "Skeleton":
            enemy.attack_power = 0
            enemy.defense_power = random.randint(1, 8)
        if enemy.name == "Assassin":
            enemy.attack_power = 0
            enemy.defense_power = random.randint(1, 10)
       
        result += f"{enemy.name} defends with {enemy.defense_power} power!<br>"

    # Resolve actions and calculate damage
    player_damage = player.attack(enemy) if player.attack_power > enemy.defense_power else 0
    enemy_damage = enemy.attack(player) if enemy.attack_power > player.defense_power else 0

    result += f"Player attacks {enemy.name} for {player_damage} damage!<br>"
    result += f"{enemy.name} attacks Player for {enemy_damage} damage!<br>"

    # Check if either player or enemy is defeated
    if player.health <= 0:
        result += "Player is defeated! Game over."
    elif enemy.health <= 0:
        result += f"{enemy.name} is defeated! You win!"
        enemy = get_random_enemy()  # Generate a new random enemy

    return jsonify({'result': result, 'player_health': player.health, 'enemy_health': enemy.health, 'enemy_name': enemy.name, 'enemy_image': enemy.image})

if __name__ == '__main__':
    app.run(debug=True)
