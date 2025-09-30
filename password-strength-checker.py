import re
import random
import string
from typing import Tuple, List

COMMON_PASSWORDS = {
    'password', 'password123', '123456', '12345678', 'qwerty', 'abc123',
    'monkey', '1234567', 'letmein', 'trustno1', 'dragon', 'baseball',
    'iloveyou', 'master', 'sunshine', 'ashley', 'bailey', 'passw0rd',
    'shadow', '123123', '654321', 'superman', 'qazwsx', 'michael',
    'football', 'welcome', 'jesus', 'ninja', 'mustang', 'password1'
}

def evaluate_password_strength(password: str) -> Tuple[str, int, List[str]]:
    score = 0
    suggestions = []
    length = len(password)

    if length < 8:
        suggestions.append("Password must be at least 8 characters long")
    elif length < 12:
        suggestions.append("Increase the length to at least 12 characters")
        score += 1
    elif length < 16:
        score += 2
    else:
        score += 3

    if re.search(r'[a-z]', password):
        score += 1
    else:
        suggestions.append("Add lowercase letters")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        suggestions.append("Add uppercase letters")

    if re.search(r'\d', password):
        score += 1
    else:
        suggestions.append("Add numbers")

    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        score += 2
    else:
        suggestions.append("Add special characters")

    if password.lower() in COMMON_PASSWORDS:
        score = 0
        suggestions.append("This is a commonly used password. Choose something unique")

    if re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def)', password.lower()):
        suggestions.append("Avoid sequential characters (e.g., 123, abc)")
        score = max(0, score - 1)

    if re.search(r'(.)\1{2,}', password):
        suggestions.append("Avoid repeating characters (e.g., aaa, 111)")
        score = max(0, score - 1)

    if score <= 3:
        strength = "Weak"
    elif score <= 6:
        strength = "Moderate"
    else:
        strength = "Strong"

    if not suggestions:
        suggestions.append("This password is very strong")

    return strength, score, suggestions


def generate_password(length: int = 16, 
                      use_uppercase: bool = True,
                      use_lowercase: bool = True,
                      use_digits: bool = True,
                      use_special: bool = True) -> str:
    if length < 8 or length > 20:
        length = 16

    char_pool = ''
    password_chars = []

    if use_lowercase:
        char_pool += string.ascii_lowercase
        password_chars.append(random.choice(string.ascii_lowercase))

    if use_uppercase:
        char_pool += string.ascii_uppercase
        password_chars.append(random.choice(string.ascii_uppercase))

    if use_digits:
        char_pool += string.digits
        password_chars.append(random.choice(string.digits))

    if use_special:
        special_chars = '!@#$%^&*()_+-=[]{};\':"|,.<>?/\\`~'
        char_pool += special_chars
        password_chars.append(random.choice(special_chars))

    if not char_pool:
        char_pool = string.ascii_letters + string.digits + '!@#$%^&*()_+-='

    remaining_length = length - len(password_chars)
    password_chars.extend(random.choice(char_pool) for _ in range(remaining_length))
    random.shuffle(password_chars)

    return ''.join(password_chars)


def display_strength_bar(strength: str, score: int):
    max_score = 9
    filled = int((score / max_score) * 20)
    bar = '█' * filled + '░' * (20 - filled)

    colors = {
        'Weak': '\033[91m',
        'Moderate': '\033[93m',
        'Strong': '\033[92m'
    }
    reset = '\033[0m'

    color = colors.get(strength, '')
    print(f"\nStrength: {color}{strength}{reset}")
    print(f"Score: {score}/9")
    print(f"[{color}{bar}{reset}]")


def main():
    while True:
        print("\nOptions:")
        print("1. Check password strength")
        print("2. Generate a strong password")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            password = input("\nEnter password to check: ")
            strength, score, suggestions = evaluate_password_strength(password)
            display_strength_bar(strength, score)
            print("\nFeedback:")
            for suggestion in suggestions:
                print(f"  {suggestion}")
        
        elif choice == '2':
            try:
                length = int(input("Password length (8-20, default 16): ") or "16")
                length = max(8, min(20, length))
            except ValueError:
                length = 16
            
            use_upper = input("Include uppercase letters? (Y/n): ").strip().lower() != 'n'
            use_lower = input("Include lowercase letters? (Y/n): ").strip().lower() != 'n'
            use_digits = input("Include digits? (Y/n): ").strip().lower() != 'n'
            use_special = input("Include special characters? (Y/n): ").strip().lower() != 'n'
            
            generated = generate_password(length, use_upper, use_lower, use_digits, use_special)
            print(f"\nGenerated Password: {generated}")
            
            strength, score, suggestions = evaluate_password_strength(generated)
            display_strength_bar(strength, score)
        
        elif choice == '3':
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
