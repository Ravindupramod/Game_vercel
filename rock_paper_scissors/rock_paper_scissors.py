"""
✊ Rock Paper Scissors
Classic hand game vs computer!

Controls:
- Type 'rock', 'paper', or 'scissors' (or r/p/s)
- Type 'quit' to exit
"""

import random

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(player, computer):
    if player == computer:
        return 'tie'
    wins = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
    return 'player' if wins[player] == computer else 'computer'

def get_emoji(choice):
    emojis = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
    return emojis.get(choice, '')

def main():
    print("\n" + "=" * 50)
    print("       ✊ ROCK  📄 PAPER  ✂️  SCISSORS")
    print("=" * 50)
    
    player_score = 0
    computer_score = 0
    
    while True:
        print(f"\nScore - You: {player_score} | Computer: {computer_score}")
        print("-" * 40)
        
        choice = input("\nEnter your choice (rock/paper/scissors or r/p/s): ").lower().strip()
        
        if choice in ('q', 'quit', 'exit'):
            print("\n👋 Thanks for playing!")
            break
        
        # Handle shortcuts
        shortcuts = {'r': 'rock', 'p': 'paper', 's': 'scissors'}
        if choice in shortcuts:
            choice = shortcuts[choice]
        
        if choice not in ['rock', 'paper', 'scissors']:
            print("❌ Invalid choice! Please enter rock, paper, or scissors.")
            continue
        
        computer = get_computer_choice()
        
        print(f"\nYou chose: {get_emoji(choice)} {choice.upper()}")
        print(f"Computer chose: {get_emoji(computer)} {computer.upper()}")
        
        result = determine_winner(choice, computer)
        
        if result == 'tie':
            print("\n🤝 It's a TIE!")
        elif result == 'player':
            print("\n🎉 YOU WIN!")
            player_score += 1
        else:
            print("\n💻 Computer wins!")
            computer_score += 1

if __name__ == "__main__":
    main()
