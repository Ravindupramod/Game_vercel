import asyncio
"""
📝 Hangman
Guess the word letter by letter!

Controls:
- Enter a letter to guess
- Type 'quit' to exit
"""

import random

WORDS = [
    'python', 'programming', 'computer', 'keyboard', 'algorithm',
    'variable', 'function', 'database', 'network', 'software',
    'developer', 'interface', 'application', 'framework', 'terminal'
]

HANGMAN = [
    """
      +---+
          |
          |
          |
         ===""",
    """
      +---+
      O   |
          |
          |
         ===""",
    """
      +---+
      O   |
      |   |
          |
         ===""",
    """
      +---+
      O   |
     /|   |
          |
         ===""",
    """
      +---+
      O   |
     /|\\  |
          |
         ===""",
    """
      +---+
      O   |
     /|\\  |
     /    |
         ===""",
    """
      +---+
      O   |
     /|\\  |
     / \\  |
         ==="""
]

def main():
    print("\n" + "=" * 50)
    print("           📝 HANGMAN 📝")
    print("=" * 50)
    
    while True:
        word = random.choice(WORDS).upper()
        guessed = set()
        wrong = 0
        
        while wrong < 6:
            # Display
            display = ' '.join(c if c in guessed else '_' for c in word)
            print(HANGMAN[wrong])
            print(f"\nWord: {display}")
            print(f"Guessed: {' '.join(sorted(guessed)) if guessed else 'None'}")
            print(f"Wrong guesses left: {6 - wrong}")
            
            if all(c in guessed for c in word):
                print(f"\n🎉 Congratulations! The word was: {word}")
                break
            
            guess = input("\nGuess a letter: ").strip().upper()
            
            if guess.lower() == 'quit':
                print(f"\n👋 The word was: {word}. Goodbye!")
                return
            
            if len(guess) != 1 or not guess.isalpha():
                print("❌ Please enter a single letter!")
                continue
            
            if guess in guessed:
                print("⚠️ You already guessed that letter!")
                continue
            
            guessed.add(guess)
            
            if guess in word:
                print(f"✅ Correct! '{guess}' is in the word!")
            else:
                wrong += 1
                print(f"❌ Wrong! '{guess}' is not in the word.")
        
        if wrong >= 6:
            print(HANGMAN[6])
            print(f"\n💀 Game Over! The word was: {word}")
        
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again not in ['y', 'yes']:
            print("\n👋 Thanks for playing!")
            break

if __name__ == "__main__":
    main()