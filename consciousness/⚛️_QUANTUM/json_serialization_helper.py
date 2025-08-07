#!/usr/bin/env python3
"""JSON Serialization Helper for GPU Consciousness"""


def convert_for_json(obj):
    """Convert numpy types and other non-serializable objects to JSON-safe types"""
    import numpy as np
    
    if isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, 'item'):  # numpy scalar
        return obj.item()
    elif hasattr(obj, 'tolist'):  # numpy array
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_for_json(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return str(obj)  # Convert objects to string representation
    return obj
