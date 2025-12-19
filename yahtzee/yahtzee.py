import asyncio
"""
🎯 Yahtzee
Dice combination game!

Controls:
- Enter dice numbers to keep (e.g., '1 3 5')
- Press ENTER to roll all
- Type 'score' to see scorecard
"""

import random

def roll_dice(keep=[]):
    return keep + [random.randint(1, 6) for _ in range(5 - len(keep))]

def display_dice(dice):
    return " ".join(f"[{d}]" for d in dice)

def calculate_scores(dice):
    counts = [dice.count(i) for i in range(1, 7)]
    scores = {}
    
    # Upper section
    for i in range(1, 7):
        scores[f'{i}s'] = dice.count(i) * i
    
    # Lower section
    scores['3 of a Kind'] = sum(dice) if max(counts) >= 3 else 0
    scores['4 of a Kind'] = sum(dice) if max(counts) >= 4 else 0
    scores['Full House'] = 25 if 3 in counts and 2 in counts else 0
    scores['Sm Straight'] = 30 if any(all((i+j) in dice for j in range(4)) for i in range(1, 4)) else 0
    scores['Lg Straight'] = 40 if sorted(dice) in [[1,2,3,4,5], [2,3,4,5,6]] else 0
    scores['Yahtzee'] = 50 if 5 in counts else 0
    scores['Chance'] = sum(dice)
    
    return scores

def main():
    print("\n" + "=" * 50)
    print("           🎯 YAHTZEE 🎯")
    print("=" * 50)
    
    scorecard = {}
    categories = ['1s', '2s', '3s', '4s', '5s', '6s', '3 of a Kind', '4 of a Kind',
                  'Full House', 'Sm Straight', 'Lg Straight', 'Yahtzee', 'Chance']
    
    for turn in range(13):
        print(f"\n{'=' * 40}")
        print(f"Turn {turn + 1} of 13")
        
        dice = roll_dice()
        rolls_left = 2
        
        while rolls_left > 0:
            print(f"\n🎲 Dice: {display_dice(dice)}")
            print(f"Rolls left: {rolls_left}")
            
            action = input("\nEnter dice positions to keep (1-5), ENTER to reroll all, 'done' to score: ").strip()
            
            if action.lower() == 'done':
                break
            
            if action == '':
                dice = roll_dice()
            else:
                try:
                    keep_indices = [int(x) - 1 for x in action.split()]
                    keep = [dice[i] for i in keep_indices if 0 <= i < 5]
                    dice = roll_dice(keep)
                except:
                    print("Invalid input!")
                    continue
            
            rolls_left -= 1
        
        print(f"\n🎲 Final dice: {display_dice(dice)}")
        
        scores = calculate_scores(dice)
        print("\nAvailable scores:")
        for i, cat in enumerate(categories):
            if cat not in scorecard:
                print(f"  {i + 1}. {cat}: {scores[cat]}")
        
        while True:
            try:
                choice = int(input("\nChoose category (1-13): ")) - 1
                cat = categories[choice]
                if cat not in scorecard:
                    scorecard[cat] = scores[cat]
                    print(f"✅ Scored {scores[cat]} for {cat}")
                    break
                else:
                    print("Already used!")
            except:
                print("Invalid choice!")
    
    print("\n" + "=" * 50)
    print("FINAL SCORECARD")
    print("=" * 50)
    
    total = 0
    for cat in categories:
        score = scorecard.get(cat, 0)
        print(f"{cat:15} : {score}")
        total += score
    
    upper = sum(scorecard.get(f'{i}s', 0) for i in range(1, 7))
    bonus = 35 if upper >= 63 else 0
    
    print("-" * 25)
    print(f"Upper Bonus    : {bonus}")
    print(f"TOTAL          : {total + bonus}")

if __name__ == "__main__":
    main()