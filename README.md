# Vampire Survivors Clone

## Overview
This project is a **Python-based Vampire Survivors clone** built using the `pygame` library. Players navigate a top-down environment, battling waves of enemies while collecting pickups and leveling up. The game challenges players to survive as long as possible while managing health, shields, and increasing enemy difficulty.

---

## Features

### Core Mechanics
- **Player Movement:** Navigate the map using the `W`, `A`, `S`, `D` keys.
- **Combat:** Utilize projectiles and melee weapons to defeat waves of enemies.
- **Leveling Up:** Gain experience points (XP) by defeating enemies to enhance your stats.
  
### Enemy System
- Multiple enemy types with varying health, size, and damage:
  - Basic enemies (green slimes)
  - Tank enemies (bit more hp than basic and a lot more damage)
  - Large Slimes (larger, tougher enemies)
  - Red slimes (slimes but fast and a bit more health and damage)

### Pickup Items
- **Shield:** Protects the player from one collision, kills the enemy the player collided with.
- **Medkit:** Restores health.

### Procedural Spawning
- Enemies and pickups spawn dynamically at randomized intervals and locations.
- Increasing difficulty over time:
  - Spawn frequency increases gradually.
  - New enemy types become available as the player's level increases.
---

## Installation

### Prerequisites
- Python 3.8+
- `pygame` library

## How to Play
1. **Movement:** Use the `W`, `A`, `S`, `D` keys to move your character.
2. **Survive:** Avoid or defeat incoming waves of enemies.
3. **Collect:** Pick up shields and medkits to enhance your chances of survival.
4. **Level Up:** Defeat enemies to gain XP and unlock stronger abilities.
5. **Win Condition:** There is no "winning"—survive as long as possible!

---


## Future Enhancements
- Add more enemy types.
- Introduce new weapon types and upgrades.
- Implement a scoring system.
- Add a main menu

---

## Credits
Developed using Python and `pygame`.

Enjoy the game!