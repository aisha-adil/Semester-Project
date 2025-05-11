"""
Utility functions for the hybrid encryption application.
"""
import os


def save_to_file(content, filename):
    """
    Save content to a file.
    
    Args:
        content (str): The content to save
        filename (str): The filename to save to
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False


def load_from_file(filename):
    """
    Load content from a file.
    
    Args:
        filename (str): The filename to load from
        
    Returns:
        str: The content of the file, or None if an error occurred
    """
    try:
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            return None
            
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error loading from file: {e}")
        return None


def is_valid_keyword(keyword):
    """
    Check if a keyword is valid for columnar transposition.
    
    Args:
        keyword (str): The keyword to check
        
    Returns:
        bool: True if the keyword is valid, False otherwise
    """
    # Check if the keyword has at least 2 characters
    if len(keyword) < 2:
        return False
    
    # Check if the keyword contains only letters
    if not keyword.isalpha():
        return False
    
    # Check if the keyword has unique letters (optional)
    # if len(set(keyword)) != len(keyword):
    #     return False
    
    return True


def format_puzzle_display(puzzle_string):
    """
    Format a cryptarithmetic puzzle for display.
    
    Args:
        puzzle_string (str): The puzzle string
        
    Returns:
        str: The formatted puzzle string
    """
    # Split the puzzle into its components
    parts = puzzle_string.split("=")
    left_side = parts[0].strip()
    right_side = parts[1].strip()
    
    # Split the left side into its components
    addends = left_side.split("+")
    
    # Format the puzzle
    max_length = max(len(addend.strip()) for addend in addends + [right_side])
    
    formatted = []
    for i, addend in enumerate(addends):
        formatted.append(addend.strip().rjust(max_length))
        if i < len(addends) - 1:
            formatted.append("+" + " " * (max_length - 1))
    
    formatted.append("-" * max_length)
    formatted.append(right_side.strip().rjust(max_length))
    
    return "\n".join(formatted)