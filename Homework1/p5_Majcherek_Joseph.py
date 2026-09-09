def caesar_cipher(text, shift):
    """Encrypts text using a Caesar cipher with letter index shifting."""
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
        elif char.islower():
            result += chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
        else:
            result += char
    return result

def caesar_decipher(ciphertext, shift):
    """Decrypts ciphertext by reversing the shift."""
    return caesar_cipher(ciphertext, -shift)

def letter_frequency(text):
    """Counts lowercase alphabetic characters into a dictionary."""
    frequencies = {}
    for i in range(len(text)):
        char = text[i].lower()
        if char.isalpha() and char.isascii():
            frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies

def main():
    """Terminal menu for user interaction."""
    while True:
        print("\n--- Caesar Cipher Menu ---")
        print("1. Encrypt & Analyze Text")
        print("2. Exit")
        choice = input("Select an option (1-2): ")

        if choice == "1":
            msg = input("Enter message: ")
            shift = int(input("Enter integer shift: "))

            ciphered = caesar_cipher(msg, shift)
            deciphered = caesar_decipher(ciphered, shift)
            freqs = letter_frequency(msg)

            print(f"\nEncrypted Text: {ciphered}")
            print(f"Letter Frequencies:")
            for char in sorted(freqs.keys()):
                print(f"  {char}: {freqs[char]}")
            print(f"Decrypted Text:  {deciphered}")
        elif choice == "2":
            break

if __name__ == "__main__":
    main()