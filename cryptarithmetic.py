"""
Cryptarithmetic puzzle generation and solving.
"""
import random
import re


def generate_simple_puzzle(letters):
    """
    Generate a simple cryptarithmetic puzzle (WORD1 + WORD2 = WORD3) using the given letters.
    
    Args:
        letters (str): The letters to use in the puzzle
        
    Returns:
        str: A cryptarithmetic puzzle string
    """
    # Ensure we have enough letters
    if len(set(letters)) < 6:
        # Add some random letters if needed
        additional_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for char in additional_letters:
            if char not in letters:
                letters += char
                if len(set(letters)) >= 6:
                    break
    
    # Ensure we're working with unique letters
    unique_letters = list(set(letters.upper()))
    random.shuffle(unique_letters)
    
    # Create three words of different lengths for the puzzle
    word1_len = random.randint(2, 4)
    word2_len = random.randint(2, 4)
    word3_len = random.randint(max(word1_len, word2_len), word1_len + word2_len)
    
    # Ensure first letters are not zero
    first_letters = unique_letters[:3]
    remaining_letters = unique_letters[3:min(10, len(unique_letters))]
    
    # Create the words
    word1 = first_letters[0] + ''.join(random.choices(remaining_letters, k=word1_len-1))
    word2 = first_letters[1] + ''.join(random.choices(remaining_letters, k=word2_len-1))
    word3 = first_letters[2] + ''.join(random.choices(remaining_letters, k=word3_len-1))
    
    # Create the puzzle string
    puzzle = f"{word1} + {word2} = {word3}"
    
    return puzzle


def parse_puzzle(puzzle_string):
    """
    Parse a cryptarithmetic puzzle string into its components.
    
    Args:
        puzzle_string (str): The puzzle string (e.g., "SEND + MORE = MONEY")
        
    Returns:
        tuple: A tuple containing the words in the puzzle and the set of unique letters
    """
    # Extract the words from the puzzle
    words = re.findall(r'\b[A-Z]+\b', puzzle_string.upper())
    
    # Extract the unique letters
    unique_letters = set(''.join(words))
    
    return words, unique_letters


def evaluate_puzzle(puzzle, assignment):
    """
    Evaluate a cryptarithmetic puzzle with a given digit assignment.
    
    Args:
        puzzle (tuple): A tuple containing the words in the puzzle
        assignment (dict): A dictionary mapping letters to digits
        
    Returns:
        bool: True if the assignment satisfies the puzzle, False otherwise
    """
    words = puzzle
    
    # Convert words to numbers based on the assignment
    numbers = []
    for word in words:
        # Check if any letter in the word is not in the assignment
        if any(letter not in assignment for letter in word):
            return False
        
        # Check for leading zeros
        if assignment[word[0]] == 0 and len(word) > 1:
            return False
        
        # Convert the word to a number
        number = 0
        for letter in word:
            number = number * 10 + assignment[letter]
        numbers.append(number)
    
    # Check if the equation is satisfied (assuming WORD1 + WORD2 = WORD3)
    return numbers[0] + numbers[1] == numbers[2]


def solve_cryptarithmetic(puzzle_string, use_heuristic=False):
    """
    Solve a cryptarithmetic puzzle using backtracking search.
    
    Args:
        puzzle_string (str): The puzzle string (e.g., "SEND + MORE = MONEY")
        use_heuristic (bool): Whether to use a heuristic for variable ordering
        
    Returns:
        dict: A dictionary mapping letters to digits, or None if no solution exists
    """
    words, letters = parse_puzzle(puzzle_string)
    letters = list(letters)
    
    # Use heuristic: order variables by frequency (most frequent first)
    if use_heuristic:
        letter_counts = {}
        for word in words:
            for letter in word:
                letter_counts[letter] = letter_counts.get(letter, 0) + 1
        letters.sort(key=lambda letter: letter_counts.get(letter, 0), reverse=True)
    
    # Get the first letters of each word (can't be assigned 0)
    first_letters = {word[0] for word in words}
    
    def backtrack(index, assignment, used_digits):
        # Base case: all letters assigned
        if index == len(letters):
            return assignment if evaluate_puzzle(words, assignment) else None
        
        current_letter = letters[index]
        
        # Try each possible digit
        for digit in range(10):
            # Skip if digit already used
            if digit in used_digits:
                continue
            
            # Skip if trying to assign 0 to a first letter
            if digit == 0 and current_letter in first_letters:
                continue
            
            # Make the assignment
            assignment[current_letter] = digit
            used_digits.add(digit)
            
            # Recursive call
            result = backtrack(index + 1, assignment, used_digits)
            if result is not None:
                return result
            
            # Backtrack
            assignment.pop(current_letter)
            used_digits.remove(digit)
        
        return None
    
    return backtrack(0, {}, set())


def is_puzzle_solvable(puzzle_string):
    """
    Check if a cryptarithmetic puzzle has a unique solution.
    
    Args:
        puzzle_string (str): The puzzle string
        
    Returns:
        bool: True if the puzzle has a unique solution, False otherwise
    """
    solution = solve_cryptarithmetic(puzzle_string)
    return solution is not None


def create_substitution_key(puzzle_string, solution):
    """
    Create a substitution key from a solved cryptarithmetic puzzle.
    
    Args:
        puzzle_string (str): The puzzle string
        solution (dict): The solution to the puzzle (letter-to-digit mapping)
        
    Returns:
        dict: A dictionary mapping letters to their corresponding digits
    """
    # Just return the solution directly as it's already a letter-to-digit mapping
    return solution