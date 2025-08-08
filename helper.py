import random
import string
import os
import csv

# Define the CSV file path
csv_file = 'data.csv'

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

def generate_OU_path(grade):
    primary = "/Students/Primary School/"
    intermediate = "/Students/Intermediate School/"
    middle = "Students/Middle School/"
    high = "Students/High School/"

    if grade == 'TK':
        return primary + 'TK'
    elif grade == 'KN':
        return primary + 'Kindergarten'
    elif grade == '01':
        return primary + '1st Grade'
    elif grade == '02':
        return primary + '2nd Grade'
    elif grade == '03':
        return primary + '3rd Grade'
    elif grade == '04':
        return intermediate + '4th Grade'
    elif grade == '05':
        return intermediate + '5th Grade'
    elif grade == '06':
        return middle + '6th Grade'
    elif grade == '07':
        return middle + '7th Grade'
    elif grade == '08':
        return middle + '8th Grade'
    elif grade == '09':
        return high + '9th Grade'
    elif grade == '10':
        return high + '10th Grade'
    elif grade == '11':
        return high + '11th Grade'
    elif grade == '12':
        return high + '12th Grade'

    return 'NA'

def add_user_to_csv(row):
    # Define header
    header = ["First Name", "Last Name", "Email Address", "Password", "Org Unit Path", "ES First Name", "ES Last Name", "ES Email"]
    
    # Check if file exists
    file_exists = os.path.exists(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # If file doesn't exist, write the header first
        if not file_exists:
            writer.writerow(header)
        
        # Write the user data row
        writer.writerow(row)

