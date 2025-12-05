"""
🃏 Blackjack
Casino card game - get 21 or close without busting!

Controls:
- 'h' to hit, 's' to stand
- 'q' to quit, 'p' to play again
"""

import random

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def create_deck():
    return [(r, s) for s in SUITS for r in RANKS]

def card_value(card):
    rank = card[0]
    if rank in ['J', 'Q', 'K']: return 10
    if rank == 'A': return 11
    return int(rank)

def hand_value(hand):
    value = sum(card_value(c) for c in hand)
    aces = sum(1 for c in hand if c[0] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def display_card(card):
    return f"[{card[0]}{card[1]}]"

def display_hand(hand, hide_first=False):
    if hide_first:
        return "[??] " + " ".join(display_card(c) for c in hand[1:])
    return " ".join(display_card(c) for c in hand)

def main():
    print("\n" + "=" * 50)
    print("           🃏 BLACKJACK 🃏")
    print("=" * 50)
    
    balance = 100
    
    while balance > 0:
        print(f"\n💰 Balance: ${balance}")
        bet = min(10, balance)
        print(f"🎰 Betting: ${bet}")
        
        deck = create_deck()
        random.shuffle(deck)
        
        player = [deck.pop(), deck.pop()]
        dealer = [deck.pop(), deck.pop()]
        
        # Player turn
        while True:
            print(f"\n👤 Your hand: {display_hand(player)} = {hand_value(player)}")
            print(f"🎩 Dealer: {display_hand(dealer, True)}")
            
            if hand_value(player) == 21:
                print("🎉 BLACKJACK!")
                break
            if hand_value(player) > 21:
                print("💥 BUST!")
                break
            
            action = input("\n(H)it or (S)tand? ").lower().strip()
            if action in ['h', 'hit']:
                player.append(deck.pop())
            elif action in ['s', 'stand']:
                break
        
        player_val = hand_value(player)
        
        # Dealer turn
        if player_val <= 21:
            print(f"\n🎩 Dealer reveals: {display_hand(dealer)} = {hand_value(dealer)}")
            while hand_value(dealer) < 17:
                dealer.append(deck.pop())
                print(f"🎩 Dealer hits: {display_hand(dealer)} = {hand_value(dealer)}")
        
        dealer_val = hand_value(dealer)
        
        # Determine winner
        print("\n" + "-" * 40)
        if player_val > 21:
            print("❌ You busted! Dealer wins.")
            balance -= bet
        elif dealer_val > 21:
            print("✅ Dealer busted! You win!")
            balance += bet
        elif player_val > dealer_val:
            print("✅ You win!")
            balance += bet
        elif player_val < dealer_val:
            print("❌ Dealer wins!")
            balance -= bet
        else:
            print("🤝 Push! It's a tie.")
        
        if balance <= 0:
            print("\n💸 You're out of money! Game over.")
            break
        
        again = input("\n(P)lay again or (Q)uit? ").lower().strip()
        if again in ['q', 'quit']:
            print(f"\n👋 Thanks for playing! Final balance: ${balance}")
            break

if __name__ == "__main__":
    main()
