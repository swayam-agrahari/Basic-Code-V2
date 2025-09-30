import random
import time

word_list = ["keyboard", "python", "programming", "hangman", "algorithm", 
             "molecule", "extraterrestrial", "computer", "universe", 
             "cat", "dog", "bird", "apple", "boat", "tree", "fish", "table"]

difficulty_levels = {
    "easy": (3, 5), 
    "medium": (6, 8), 
    "hard": (9, 12)
}

def get_word_by_difficulty(difficulty):
    min_len, max_len = difficulty_levels[difficulty]
    possible_words = [word for word in word_list if min_len <= len(word) <= max_len]
    
    if not possible_words:
        print(f"Warning: No words found for {difficulty} difficulty. Defaulting to 'medium'.")
        possible_words = [word for word in word_list if 6 <= len(word) <= 8]  
    
    return random.choice(possible_words)

def play_round(difficulty, time_limit=30, max_guesses=3):
    word_to_guess = get_word_by_difficulty(difficulty)
    scrambled_word = ''.join(random.sample(word_to_guess, len(word_to_guess)))
    
    print(f"Scrambled Letters: {scrambled_word}")
    print(f"Guess the word!")

    start_time = time.time()
    remaining_guesses = max_guesses
    score = 0

    while remaining_guesses > 0:
        if time.time() - start_time > time_limit:
            print("Time's up!")
            break
        
        user_guess = input(f"You have {remaining_guesses} guesses left. Your guess: ")

        if user_guess.lower() == word_to_guess:
            time_taken = int(time.time() - start_time)
            score = max(0, 100 - time_taken) 
            print(f"Correct! The word was: {word_to_guess}")
            print(f"Your score for this round: {score}")
            break
        else:
            remaining_guesses -= 1
            print("Incorrect guess.")
        
    if remaining_guesses == 0 and time.time() - start_time <= time_limit:
        print(f"Sorry! The word was: {word_to_guess}")

    return score

def solo_mode():
    total_score = 0
    rounds = 5  
    difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
    
    for round_num in range(rounds):
        print(f"\nRound {round_num + 1}")
        score = play_round(difficulty)
        total_score += score

    print(f"\nYour total score in Solo Mode is: {total_score}")

def challenge_mode():
    total_score = 0
    difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
    
    round_num = 1
    while True:
        print(f"\nChallenge Round {round_num}")
        score = play_round(difficulty)
        total_score += score
        
        if score == 0:  
            print(f"Game over! Final score: {total_score}")
            break
        
        round_num += 1
        if round_num > 10:
            print(f"Game over! Final score: {total_score}")
            break

def multiplayer_mode():
    player1_score = 0
    player2_score = 0
    rounds = 5
    difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
    
    for round_num in range(rounds):
        print(f"\nRound {round_num + 1}")
        print("Player 1's turn")
        player1_score += play_round(difficulty)
        print("Player 2's turn")
        player2_score += play_round(difficulty)

    if player1_score > player2_score:
        print(f"\nPlayer 1 wins with {player1_score} points!")
    elif player2_score > player1_score:
        print(f"\nPlayer 2 wins with {player2_score} points!")
    else:
        print(f"\nIt's a tie! Both players scored {player1_score} points.")

def main():
    print("Welcome to Reverse Hangman!")
    mode = input("Choose game mode (solo, challenge, multiplayer): ").lower()

    if mode == "solo":
        solo_mode()
    elif mode == "challenge":
        challenge_mode()
    elif mode == "multiplayer":
        multiplayer_mode()
    else:
        print("Invalid mode. Please try again.")
        main()

if __name__ == "__main__":
    main()
