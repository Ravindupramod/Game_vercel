"""
⚔️ War Card Game
Simple card battle game!

Controls:
- Press ENTER to draw cards
- Type 'quit' to exit
"""

import random

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUES = {r: i for i, r in enumerate(RANKS)}

def create_deck():
    return [(r, s) for s in SUITS for r in RANKS]

def display_card(card):
    return f"[{card[0]}{card[1]}]"

def main():
    print("\n" + "=" * 50)
    print("           ⚔️ WAR CARD GAME ⚔️")
    print("=" * 50)
    
    deck = create_deck()
    random.shuffle(deck)
    
    player_deck = deck[:26]
    computer_deck = deck[26:]
    
    round_num = 0
    
    while player_deck and computer_deck:
        print(f"\n{'=' * 40}")
        print(f"Round {round_num + 1}")
        print(f"Your cards: {len(player_deck)} | Computer cards: {len(computer_deck)}")
        
        action = input("\nPress ENTER to draw (or 'quit'): ").strip().lower()
        if action in ['q', 'quit']:
            break
        
        player_card = player_deck.pop(0)
        computer_card = computer_deck.pop(0)
        
        print(f"\n👤 You drew: {display_card(player_card)}")
        print(f"💻 Computer drew: {display_card(computer_card)}")
        
        player_val = VALUES[player_card[0]]
        computer_val = VALUES[computer_card[0]]
        
        if player_val > computer_val:
            print("\n✅ You win this round!")
            player_deck.extend([player_card, computer_card])
        elif computer_val > player_val:
            print("\n❌ Computer wins this round!")
            computer_deck.extend([player_card, computer_card])
        else:
            print("\n⚔️ WAR! Cards go to war pile...")
            # Simple war - each reveals one more card
            war_pile = [player_card, computer_card]
            if player_deck and computer_deck:
                war_pile.append(player_deck.pop(0))
                war_pile.append(computer_deck.pop(0))
                if VALUES[war_pile[-2][0]] >= VALUES[war_pile[-1][0]]:
                    print("You win the war!")
                    player_deck.extend(war_pile)
                else:
                    print("Computer wins the war!")
                    computer_deck.extend(war_pile)
        
        round_num += 1
        
        if round_num >= 50:  # Limit rounds
            print("\n⏱️ 50 rounds reached!")
            break
    
    print("\n" + "=" * 50)
    print("FINAL RESULTS")
    print("=" * 50)
    print(f"\nYour cards: {len(player_deck)}")
    print(f"Computer cards: {len(computer_deck)}")
    
    if len(player_deck) > len(computer_deck):
        print("\n🎉 YOU WIN THE WAR!")
    elif len(computer_deck) > len(player_deck):
        print("\n💻 Computer wins the war!")
    else:
        print("\n🤝 It's a draw!")

if __name__ == "__main__":
    main()
