"""
Genetic algorithm for cryptarithmetic puzzle generation.
"""
import random
import string
from cryptarithmetic import generate_simple_puzzle, parse_puzzle, solve_cryptarithmetic, is_puzzle_solvable


class PuzzleIndividual:
    """
    Represents a single cryptarithmetic puzzle in the genetic algorithm population.
    """
    def __init__(self, puzzle_string=None, letters=None):
        """
        Initialize a puzzle individual, either with a provided puzzle or by generating a random one.
        
        Args:
            puzzle_string (str, optional): A puzzle string. If None, a random puzzle will be generated.
            letters (str, optional): Letters to use for puzzle generation. Required if puzzle_string is None.
        """
        if puzzle_string:
            self.puzzle_string = puzzle_string
        else:
            self.puzzle_string = generate_simple_puzzle(letters)
        
        self.words, self.unique_letters = parse_puzzle(self.puzzle_string)
        self.fitness = 0
        self.solution = None
    
    def calculate_fitness(self, target_letters):
        """
        Calculate the fitness of this puzzle.
        
        Args:
            target_letters (set): The set of letters we want to include in the puzzle
            
        Returns:
            float: The fitness score (higher is better)
        """
        # Try to solve the puzzle
        self.solution = solve_cryptarithmetic(self.puzzle_string)
        
        # If the puzzle is not solvable, it has minimum fitness
        if self.solution is None:
            self.fitness = 0
            return self.fitness
        
        # Calculate completeness: how many of the target letters are used
        used_letters = set(self.unique_letters)
        completeness = len(used_letters.intersection(target_letters)) / len(target_letters)
        
        # Calculate complexity: based on the number of letters used
        complexity = len(used_letters) / 10  # Assuming we won't use more than 10 letters
        
        # Calculate the final fitness (weighted sum)
        self.fitness = 0.7 * completeness + 0.3 * complexity
        
        return self.fitness


def initial_population(size, letters):
    """
    Create an initial population of puzzle individuals.
    
    Args:
        size (int): The population size
        letters (str): The letters to use for puzzle generation
        
    Returns:
        list: A list of PuzzleIndividual objects
    """
    population = []
    for _ in range(size):
        individual = PuzzleIndividual(letters=letters)
        population.append(individual)
    
    return population


def selection(population, tournament_size=3):
    """
    Select individuals from the population using tournament selection.
    
    Args:
        population (list): The population of PuzzleIndividual objects
        tournament_size (int): The number of individuals in each tournament
        
    Returns:
        PuzzleIndividual: The selected individual
    """
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=lambda x: x.fitness)


def crossover(parent1, parent2):
    """
    Perform crossover between two parent puzzles to create a child puzzle.
    
    Args:
        parent1 (PuzzleIndividual): The first parent
        parent2 (PuzzleIndividual): The second parent
        
    Returns:
        PuzzleIndividual: The child puzzle
    """
    # Simple implementation: take one word from each parent
    words1 = parent1.words
    words2 = parent2.words
    
    # Randomly select which words to take from which parent
    if random.random() < 0.5:
        new_puzzle = f"{words1[0]} + {words2[1]} = {words1[2]}"
    else:
        new_puzzle = f"{words2[0]} + {words1[1]} = {words2[2]}"
    
    return PuzzleIndividual(puzzle_string=new_puzzle)


def mutation(individual, mutation_rate=0.2):
    """
    Mutate a puzzle individual.
    
    Args:
        individual (PuzzleIndividual): The puzzle to mutate
        mutation_rate (float): The probability of mutation
        
    Returns:
        PuzzleIndividual: The mutated puzzle
    """
    if random.random() > mutation_rate:
        return individual
    
    words = individual.words
    unique_letters = list(individual.unique_letters)
    
    # Randomly choose a mutation type
    mutation_type = random.choice(["swap", "replace"])
    
    if mutation_type == "swap" and len(unique_letters) >= 2:
        # Swap two letters in the puzzle
        letter1, letter2 = random.sample(unique_letters, 2)
        
        new_puzzle = individual.puzzle_string.replace(letter1, '#')
        new_puzzle = new_puzzle.replace(letter2, letter1)
        new_puzzle = new_puzzle.replace('#', letter2)
        
    else:
        # Replace a random letter in a random word
        word_idx = random.randint(0, len(words) - 1)
        if len(words[word_idx]) <= 1:
            return individual  # Can't mutate if word is too short
        
        char_idx = random.randint(1, len(words[word_idx]) - 1)  # Avoid first letter
        
        # Get a new letter not in the current unique letters
        available_letters = set(string.ascii_uppercase) - set(unique_letters)
        if not available_letters:
            return individual  # Can't mutate if all letters are used
        
        new_letter = random.choice(list(available_letters))
        
        # Create new word
        new_word = words[word_idx][:char_idx] + new_letter + words[word_idx][char_idx+1:]
        
        # Create new puzzle string
        new_words = words.copy()
        new_words[word_idx] = new_word
        new_puzzle = f"{new_words[0]} + {new_words[1]} = {new_words[2]}"
    
    return PuzzleIndividual(puzzle_string=new_puzzle)


def generate_puzzle_ga(letters, population_size=50, generations=20, tournament_size=3, mutation_rate=0.2):
    """
    Generate a cryptarithmetic puzzle using a genetic algorithm.
    
    Args:
        letters (str): The letters to include in the puzzle
        population_size (int): The size of the population
        generations (int): The number of generations to run
        tournament_size (int): The tournament size for selection
        mutation_rate (float): The mutation rate
        
    Returns:
        PuzzleIndividual: The best puzzle found
    """
    # Convert letters to uppercase set
    target_letters = set(letters.upper())
    
    # Initialize population
    population = initial_population(population_size, letters)
    
    # Calculate initial fitness
    for individual in population:
        individual.calculate_fitness(target_letters)
    
    # Main GA loop
    for generation in range(generations):
        new_population = []
        
        # Elitism: keep the best individual
        best_individual = max(population, key=lambda x: x.fitness)
        new_population.append(best_individual)
        
        # Create the rest of the new population
        while len(new_population) < population_size:
            # Selection
            parent1 = selection(population, tournament_size)
            parent2 = selection(population, tournament_size)
            
            # Crossover
            child = crossover(parent1, parent2)
            
            # Mutation
            child = mutation(child, mutation_rate)
            
            # Calculate fitness
            child.calculate_fitness(target_letters)
            
            # Add to new population
            new_population.append(child)
        
        # Replace old population
        population = new_population
    
    # Return the best individual found
    best_individual = max(population, key=lambda x: x.fitness)
    
    # If the best individual has a fitness of 0 (no solution), try again with a simple puzzle
    if best_individual.fitness == 0:
        while True:
            puzzle = generate_simple_puzzle(letters)
            if is_puzzle_solvable(puzzle):
                individual = PuzzleIndividual(puzzle_string=puzzle)
                individual.calculate_fitness(target_letters)
                return individual
    
    return best_individual