"""
Hybrid encryption and decryption functions.
"""
from transposition_cipher import encrypt_transposition, decrypt_transposition
from cryptarithmetic import solve_cryptarithmetic, create_substitution_key
from genetic_algorithm import generate_puzzle_ga


def encrypt(plaintext, keyword):
    """
    Encrypt plaintext using the hybrid approach: columnar transposition followed
    by cryptarithmetic-based substitution with genetic algorithm puzzle generation.
    
    Args:
        plaintext (str): The plaintext to encrypt
        keyword (str): The keyword for columnar transposition
        
    Returns:
        tuple: A tuple containing (cryptarithmetic_puzzle, transposition_key)
            where cryptarithmetic_puzzle is the encrypted message and
            transposition_key is the keyword used for transposition
    """
    # Step 1: Perform columnar transposition
    transposed_text = encrypt_transposition(plaintext, keyword)
    
    # Step 2: Use genetic algorithm to generate a cryptarithmetic puzzle
    # that uses the letters in the transposed text
    puzzle_individual = generate_puzzle_ga(transposed_text)
    
    # Step 3: Return the puzzle as the encrypted message
    return (puzzle_individual.puzzle_string, keyword)


def decrypt(encrypted_puzzle, keyword, use_heuristic=False):
    """
    Decrypt an encrypted message using the hybrid approach.
    
    Args:
        encrypted_puzzle (str): The cryptarithmetic puzzle
        keyword (str): The keyword for columnar transposition
        use_heuristic (bool): Whether to use a heuristic for cryptarithmetic solving
        
    Returns:
        str: The decrypted plaintext
    """
    # Step 1: Solve the cryptarithmetic puzzle
    solution = solve_cryptarithmetic(encrypted_puzzle, use_heuristic)
    
    if solution is None:
        raise ValueError("Failed to solve the cryptarithmetic puzzle.")
    
    # Step 2: Create a substitution key from the solution
    substitution_key = create_substitution_key(encrypted_puzzle, solution)
    
    # Step 3: Extract the letters from the puzzle
    # We'll use the puzzle format directly as our ciphertext
    ciphertext = encrypted_puzzle
    
    # Step 4: Perform reverse substitution to get the transposed text
    transposed_text = ""
    for char in ciphertext:
        if char.isalpha():
            # Use the substitution key to map back to digits
            transposed_text += str(substitution_key.get(char, char))
        else:
            # Keep non-alphabetic characters as is
            transposed_text += char
    
    # Remove any non-alphanumeric characters (spaces, +, =, etc.)
    transposed_text = ''.join(char for char in transposed_text if char.isalnum())
    
    # Step 5: Perform reverse transposition
    plaintext = decrypt_transposition(transposed_text, keyword)
    
    return plaintext