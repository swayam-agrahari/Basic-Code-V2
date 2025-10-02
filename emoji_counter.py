import argparse
import emoji
import regex
from collections import Counter

def extract_emojis(text):
    emoji_pattern = regex.compile(r'\X', flags=regex.UNICODE)
    emojis = [char for char in emoji_pattern.findall(text) if any(char in e for e in emoji.UNICODE_EMOJI_ENGLISH)]
    return emojis

def count_emojis_in_files(files):
    counter = Counter()
    for file in files:
        try:
            with open(file, encoding='utf-8') as f:
                text = f.read()
                emojis_found = extract_emojis(text)
                counter.update(emojis_found)
        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"Error reading {file}: {e}")
    return counter

def main():
    parser = argparse.ArgumentParser(description="Emoji Usage Counter in Text Files")
    parser.add_argument('files', nargs='+', help="Text files to analyze")
    parser.add_argument('--top', type=int, default=None, help="Show top N emojis")
    args = parser.parse_args()

    emoji_counts = count_emojis_in_files(args.files)

    sorted_emojis = emoji_counts.most_common(args.top)

    print(f"{'Emoji':<10} {'Count':>5}")
    print("-" * 17)
    for emj, count in sorted_emojis:
        print(f"{emj:<10} {count:>5}")

if __name__ == "__main__":
    main()
