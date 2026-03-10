# True-Based-Strategy-Game
A grid-based turn-based strategy game inspired by Fire Emblem / Civilization. Features include player movement, enemy AI, attack animations, and a start/game-over screen with restart/exit options. Built with Python


🎮 Features

Single player (selectable icon) vs 1–2 AI enemies

Grid-based movement & attack

Enemy AI moves independently and attempts to approach the player

Attack animations (projectile/laser effect)

Player & Enemy HP tracking

Start screen with rules and icon selection

Game over screen with Restart or Exit buttons

######################################################################################################


📌 How the Game Works

1.Start Screen:

Shows the rules and instructions.

Player selects their icon and the number of enemies (1–2).

Press START to begin the game.

2.Game Loop:

Player moves within a limited range and can attack adjacent enemies.

Enemy AI moves independently to approach or attack the player.

Attack animations show projectiles from attacker to target.

Player and enemy HP are displayed at the top of the screen.

3.Game Over:

If the player HP reaches 0 → enemies win.

If all enemy HP reaches 0 → player wins.

Restart or Exit options appear.

######################################################################################################


⚙️ Design Decisions

Icons and Images:

Player can choose between two icons (player1.png, player2.png) for customization.

Enemies have separate icons (enemy1.png, enemy2.png) for identification.

icon.png sets the window icon.

Game Engine Separation:

game_engine.py handles all logic, keeping main.py clean and focused on the interface / game loop.

######################################################################################################

💻 How to Run

Install dependencies:

pip install pygame

Run the game:

python main.py

Follow the start screen instructions.
