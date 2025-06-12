#!/bin/bash

# Set path to games folder
GAMES_DIR="games"

# Add the current project root to PYTHONPATH so Python can find utils/
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Function to run a Python game by filename
run_game() {
  echo "Launching $1 ..."
  python3 "$GAMES_DIR/$1"
}

# Menu
while true; do
  echo ""
  echo "?? Quantum Game Launcher"
  echo "------------------------"
  echo "1. Shor Game (shor_reb.py)"
  echo "2. Entanglement Game (entanglement_game.py)"
  echo "3. Deu Game (deugame.py)"
  echo "4. Functional Entanglement Game (funcentaglegame.py)"
  echo "5. Quantum Factor Game (quantum_factor_gui.py)"
  echo "6. Quantum Zeno Game (zeno_gui.py)"
  echo ". Exit"
  echo ""

  read -p "Select a game [1-6]: " choice

  case $choice in
    1) run_game "shor_reb.py" ;;
    2) run_game "entanglement_game.py" ;;
    3) run_game "deugame.py" ;;
    4) run_game "funcentaglegame.py" ;;
    5) run_game "quantum_factor_gui.py" ;;
    6) run_game "zeno_gui.py" ;;
    10) echo "Goodbye!"; exit 0 ;;
    *) echo "? Invalid choice. Please try again." ;;
  esac
done
