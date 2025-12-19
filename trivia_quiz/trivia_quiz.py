import asyncio
"""
🧠 Trivia Quiz
Test your knowledge!

Controls:
- Enter 1-4 to answer
- Type 'quit' to exit
"""

import random

QUESTIONS = [
    {"q": "What is the capital of France?", "a": ["Paris", "London", "Berlin", "Madrid"], "c": 0},
    {"q": "Which planet is known as the Red Planet?", "a": ["Venus", "Mars", "Jupiter", "Saturn"], "c": 1},
    {"q": "What is the largest mammal?", "a": ["Elephant", "Giraffe", "Blue Whale", "Hippopotamus"], "c": 2},
    {"q": "Who painted the Mona Lisa?", "a": ["Van Gogh", "Picasso", "Da Vinci", "Michelangelo"], "c": 2},
    {"q": "What year did World War II end?", "a": ["1943", "1944", "1945", "1946"], "c": 2},
    {"q": "What is the chemical symbol for gold?", "a": ["Go", "Gd", "Au", "Ag"], "c": 2},
    {"q": "Which country has the largest population?", "a": ["USA", "India", "China", "Russia"], "c": 2},
    {"q": "What is the speed of light?", "a": ["300,000 km/s", "150,000 km/s", "1,000 km/s", "500,000 km/s"], "c": 0},
    {"q": "Who wrote 'Romeo and Juliet'?", "a": ["Dickens", "Shakespeare", "Austen", "Hemingway"], "c": 1},
    {"q": "What is the largest ocean?", "a": ["Atlantic", "Indian", "Pacific", "Arctic"], "c": 2},
    {"q": "How many planets are in our solar system?", "a": ["7", "8", "9", "10"], "c": 1},
    {"q": "What is the hardest natural substance?", "a": ["Gold", "Iron", "Diamond", "Platinum"], "c": 2},
    {"q": "Which element has the symbol 'O'?", "a": ["Gold", "Oxygen", "Osmium", "Oganesson"], "c": 1},
    {"q": "What is the tallest mountain on Earth?", "a": ["K2", "Everest", "Kilimanjaro", "Denali"], "c": 1},
    {"q": "Who invented the telephone?", "a": ["Edison", "Tesla", "Bell", "Marconi"], "c": 2},
]

def main():
    print("\n" + "=" * 50)
    print("           🧠 TRIVIA QUIZ 🧠")
    print("=" * 50)
    
    questions = QUESTIONS[:]
    random.shuffle(questions)
    questions = questions[:10]
    
    score = 0
    
    for i, q in enumerate(questions):
        print(f"\n{'=' * 40}")
        print(f"Question {i + 1}/10")
        print(f"\n📋 {q['q']}")
        print()
        
        answers = q['a'][:]
        correct_answer = answers[q['c']]
        random.shuffle(answers)
        correct_idx = answers.index(correct_answer)
        
        for j, a in enumerate(answers):
            print(f"  {j + 1}. {a}")
        
        while True:
            choice = input("\nYour answer (1-4): ").strip()
            
            if choice.lower() == 'quit':
                print(f"\n👋 Final Score: {score}/{i}")
                return
            
            if choice in ['1', '2', '3', '4']:
                choice = int(choice) - 1
                break
            print("Please enter 1-4!")
        
        if choice == correct_idx:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong! The answer was: {correct_answer}")
        
        print(f"Score: {score}/{i + 1}")
    
    print("\n" + "=" * 50)
    print("           FINAL RESULTS")
    print("=" * 50)
    print(f"\n🏆 Score: {score}/10")
    
    if score == 10:
        print("🌟 PERFECT SCORE! You're a genius!")
    elif score >= 7:
        print("🎉 Great job! You know your stuff!")
    elif score >= 5:
        print("👍 Not bad! Keep learning!")
    else:
        print("📚 Keep studying! You'll get better!")

if __name__ == "__main__":
    main()