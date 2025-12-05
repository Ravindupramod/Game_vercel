"""
🔤 Word Scramble
Unscramble the letters to find the word!

Controls:
- Type your guess
- Type 'hint' for a hint
- Type 'skip' to skip
- Type 'quit' to exit
"""

import random

WORDS = {
    'easy': ['cat', 'dog', 'car', 'sun', 'hat', 'book', 'tree', 'fish', 'bird', 'cake'],
    'medium': ['python', 'guitar', 'planet', 'jungle', 'rocket', 'orange', 'dragon', 'castle'],
    'hard': ['adventure', 'beautiful', 'challenge', 'dangerous', 'excellent', 'fantastic']
}

def scramble(word):
    letters = list(word)
    while True:
        random.shuffle(letters)
        scrambled = ''.join(letters)
        if scrambled != word:
            return scrambled

def main():
    print("\n" + "=" * 50)
    print("         🔤 WORD SCRAMBLE 🔤")
    print("=" * 50)
    
    score = 0
    streak = 0
    
    print("\nDifficulty: 1. Easy  2. Medium  3. Hard")
    diff = input("Choose (1-3): ").strip()
    difficulty = {'1': 'easy', '2': 'medium', '3': 'hard'}.get(diff, 'medium')
    
    words = WORDS[difficulty][:]
    random.shuffle(words)
    
    for i, word in enumerate(words):
        scrambled = scramble(word)
        hints_used = 0
        revealed = ['_'] * len(word)
        
        print(f"\n{'=' * 40}")
        print(f"Word {i + 1}/{len(words)} | Score: {score} | Streak: {streak}")
        print(f"\n🔀 Scrambled: {scrambled.upper()}")
        
        attempts = 3
        while attempts > 0:
            guess = input("\nYour guess: ").strip().lower()
            
            if guess == 'quit':
                print(f"\n👋 Final Score: {score}")
                return
            
            if guess == 'skip':
                print(f"⏭️ Skipped! The word was: {word.upper()}")
                streak = 0
                break
            
            if guess == 'hint':
                hidden = [i for i, c in enumerate(revealed) if c == '_']
                if hidden:
                    idx = random.choice(hidden)
                    revealed[idx] = word[idx]
                    hints_used += 1
                    print(f"💡 Hint: {' '.join(revealed).upper()}")
                else:
                    print("No more hints available!")
                continue
            
            if guess == word:
                points = max(10 - hints_used * 3, 3)
                score += points
                streak += 1
                print(f"✅ Correct! +{points} points!")
                if streak > 1:
                    print(f"🔥 {streak} word streak!")
                break
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"❌ Wrong! {attempts} attempts left.")
                else:
                    print(f"❌ The word was: {word.upper()}")
                    streak = 0
    
    print("\n" + "=" * 50)
    print(f"🏆 FINAL SCORE: {score}")
    print("=" * 50)

if __name__ == "__main__":
    main()
