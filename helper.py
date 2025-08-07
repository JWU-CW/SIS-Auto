import random
import string

def split_name(full_name: str) -> dict:
    """
    Splits a full name into first and last name.
    Handles middle initials if present.
    
    Examples:
    - "Jack Miller" ➜ {'first_name': 'Jack', 'last_name': 'Miller'}
    - "Jack M Miller" ➜ {'first_name': 'Jack', 'last_name': 'Miller'}
    """
    parts = full_name.strip().split()

    if len(parts) == 2:
        # Simple case: first and last
        first_name, last_name = parts
    elif len(parts) == 3:
        # Middle initial present: assume format "First M Last"
        first_name, _, last_name = parts
    else:
        raise ValueError(f"Unexpected name format: '{full_name}'")

    return {'first_name': first_name, 'last_name': last_name}

def generate_random_string(length=8):
    """
    generate temporary password
    """
    characters = string.ascii_lowercase + string.digits  # a-z and 0-9
    return ''.join(random.choices(characters, k=length))
