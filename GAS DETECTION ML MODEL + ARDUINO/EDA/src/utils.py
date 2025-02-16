import yaml
import pickle

def load_config(config_path='config.yaml'):
    """Load configuration file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def pickle_load(path):
    """Load data from pickle file."""
    with open(path, 'rb') as file:
        return pickle.load(file)
