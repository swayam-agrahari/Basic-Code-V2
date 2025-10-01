MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
    ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.',
    '-': '-....-', '(': '-.--.', ')': '-.--.-', '!': '-.-.--',
    ':': '---...', ';': '-.-.-.', "'": '.----.', '&': '.-...',
    '=': '-...-', '+': '.-.-.', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-', '@': '.--.-.'
}

MORSE_CODE_DICT_REVERSED = {value: key for key, value in MORSE_CODE_DICT.items()}

def text_to_morse(text: str) -> str:
    text = text.upper()
    morse_code = []
    for word in text.split(" "):  
        morse_word = []
        for char in word:
            if char in MORSE_CODE_DICT:
                morse_word.append(MORSE_CODE_DICT[char])
        morse_code.append(" ".join(morse_word))
    return " / ".join(morse_code)  

def morse_to_text(morse: str) -> str:
    text = []
    words = morse.split(" / ") 
    for word in words:
        letters = word.split()
        decoded_word = ""
        for letter in letters:
            decoded_word += MORSE_CODE_DICT_REVERSED.get(letter, "")
        text.append(decoded_word)
    return " ".join(text)

if __name__ == "__main__":
    text = "Hello World"
    encoded = text_to_morse(text)
    print("Text to Morse:", encoded)

    morse = ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
    decoded = morse_to_text(morse)
    print("Morse to Text:", decoded)