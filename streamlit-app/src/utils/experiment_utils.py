# src/utils/experiment_utils.py
import random
from datetime import datetime


def generate_experiment_name(include_timestamp=True):
    adjectives = [
        "neural",
        "deep",
        "quantum",
        "adaptive",
        "cognitive",
        "smart",
        "dynamic",
        "automated",
        "synthetic",
        "augmented",
    ]
    nouns = [
        "tensor",
        "vector",
        "matrix",
        "neuron",
        "transformer",
        "agent",
        "network",
        "model",
        "brain",
        "oracle",
    ]

    name = f"{random.choice(adjectives)}_{random.choice(nouns)}"

    if include_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        name = f"{name}_{timestamp}"

    return name.lower()
