from datasets import load_dataset

def data_loader():
    # Load the dataset from Hugging Face
    dataset = load_dataset("NikolaiZhdanov/historical-checkers-games")
    
    # Parse the dataset to extract moves as lists of moves
    games = []
    for game in dataset['train']:  # Adjust 'train' as per dataset structure
        # Each game is stored as a string, split by commas for individual moves
        moves = game['moves'].split(',')
        games.append(moves)
    
    return games

'''
# Usage
checkers_games = data_loader()
print(checkers_games[0])  # Display the moves of the first game
print(checkers_games[1])  # Display the moves of the first game
'''
'''
moves = []
for example in dataset['train']:
	for move in example['moves']:
		if '-' in move:  # Check if the move contains a hyphen
			start, end = move.split('-')
			moves.append((start, end))

return moves
'''
    
'''
    
historical_moves = data_loader()
print(historical_moves)
'''
'''
from datasets import load_dataset

def data_loader():
    dataset = load_dataset("NikolaiZhdanov/historical-checkers-games")
    
    moves = []
    for example in dataset['train']:
        for move in example['moves']:
            if '-' in move:  # Check if the move contains a hyphen
                start, end = move.split('-')
                moves.append((start, end))

    return moves
    
import pandas as pd

splits = {'train': 'data/train-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet'}
df = pd.read_parquet("hf://datasets/NikolaiZhdanov/historical-checkers-games/" + splits["train"])
'''
