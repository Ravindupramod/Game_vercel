import asyncio
"""
🎲 Dice Rolling Simulator
Roll virtual dice!

Controls:
- Press ENTER to roll
- Type number of dice (1-10)
- Type 'quit' to exit
"""

import random
import time

def roll_dice(num_dice=1, sides=6):
    return [random.randint(1, sides) for _ in range(num_dice)]

def draw_die(value):
    dice_art = {
        1: ["┌─────────┐", "│         │", "│    ●    │", "│         │", "└─────────┘"],
        2: ["┌─────────┐", "│  ●      │", "│         │", "│      ●  │", "└─────────┘"],
        3: ["┌─────────┐", "│  ●      │", "│    ●    │", "│      ●  │", "└─────────┘"],
        4: ["┌─────────┐", "│  ●   ●  │", "│         │", "│  ●   ●  │", "└─────────┘"],
        5: ["┌─────────┐", "│  ●   ●  │", "│    ●    │", "│  ●   ●  │", "└─────────┘"],
        6: ["┌─────────┐", "│  ●   ●  │", "│  ●   ●  │", "│  ●   ●  │", "└─────────┘"]
    }
    return dice_art.get(value, dice_art[1])

def display_dice(values):
    if len(values) > 5:
        # Just show numbers for many dice
        print(" ".join(f"[{v}]" for v in values))
        return
    
    dice_art = [draw_die(v) for v in values]
    for i in range(5):
        print("  ".join(d[i] for d in dice_art))

def main():
    print("\n" + "=" * 50)
    print("          🎲 DICE ROLLING SIMULATOR 🎲")
    print("=" * 50)
    
    num_dice = 2
    
    while True:
        print(f"\nRolling {num_dice} dice...")
        print("-" * 40)
        
        # Animation
        for _ in range(3):
            print("🎲 Rolling...", end="\r")
            time.sleep(0.2)
            print("   Rolling...", end="\r")
            time.sleep(0.2)
        
        results = roll_dice(num_dice)
        print("\n")
        display_dice(results)
        
        total = sum(results)
        print(f"\n📊 Results: {results}")
        print(f"📈 Total: {total}")
        if num_dice > 1:
            print(f"📉 Average: {total / num_dice:.1f}")
        
        print("\n" + "-" * 40)
        user_input = input("Press ENTER to roll again, enter number of dice (1-10), or 'quit': ").strip()
        
        if user_input.lower() in ('q', 'quit', 'exit'):
            print("\n👋 Thanks for playing!")
            break
        elif user_input.isdigit():
            num_dice = max(1, min(10, int(user_input)))
            print(f"✅ Set to {num_dice} dice")

if __name__ == "__main__":
    main()