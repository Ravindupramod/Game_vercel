"""
🔢 Number Guessing Game
Guess the secret number!

Controls:
- Enter a number to guess
- Type 'quit' to exit
"""

import random

def main():
    print("\n" + "=" * 50)
    print("        🔢 NUMBER GUESSING GAME 🔢")
    print("=" * 50)
    
    while True:
        print("\nDifficulty:")
        print("1. Easy (1-50, 10 guesses)")
        print("2. Medium (1-100, 7 guesses)")
        print("3. Hard (1-200, 6 guesses)")
        
        choice = input("\nSelect difficulty (1-3): ").strip()
        
        if choice == '1':
            max_num, max_guesses = 50, 10
        elif choice == '2':
            max_num, max_guesses = 100, 7
        elif choice == '3':
            max_num, max_guesses = 200, 6
        else:
            max_num, max_guesses = 100, 7
        
        secret = random.randint(1, max_num)
        guesses = 0
        
        print(f"\n🎯 I'm thinking of a number between 1 and {max_num}")
        print(f"📊 You have {max_guesses} guesses. Good luck!\n")
        
        while guesses < max_guesses:
            try:
                guess = input(f"Guess {guesses + 1}/{max_guesses}: ").strip()
                
                if guess.lower() in ['q', 'quit']:
                    print(f"\n👋 The number was {secret}. Goodbye!")
                    return
                
                guess = int(guess)
                guesses += 1
                
                if guess == secret:
                    print(f"\n🎉 Correct! You got it in {guesses} guesses!")
                    break
                elif guess < secret:
                    print("📈 Too low! Try higher.")
                else:
                    print("📉 Too high! Try lower.")
                
                remaining = max_guesses - guesses
                if remaining > 0:
                    print(f"   ({remaining} guesses left)")
                    
            except ValueError:
                print("❌ Please enter a valid number!")
        
        if guesses >= max_guesses and guess != secret:
            print(f"\n😢 Out of guesses! The number was {secret}")
        
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again not in ['y', 'yes']:
            print("\n👋 Thanks for playing!")
            break

if __name__ == "__main__":
    main()
