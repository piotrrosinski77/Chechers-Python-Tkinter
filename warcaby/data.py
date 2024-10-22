from datasets import load_dataset

def data_loader():
    # Load the dataset from Hugging Face
    dataset = load_dataset("NikolaiZhdanov/historical-checkers-games")
    
    moves = []
    # Iterate over each game in the 'train' split of the dataset
    for example in dataset['train']:
        for move in example['moves']:
            if '-' in move:  # Regular moves
                parts = move.split('-')
                if len(parts) == 2:
                    start, end = parts
                    moves.append((start, end))
            elif 'x' in move:  # Capture moves
                captures = move.split('x')
                if len(captures) >= 2:
                    moves.append(tuple(captures))

    return moves



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
