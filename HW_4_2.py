import string
import random


# Function to generate a random dictionary with `n` unique keys
def generate_dict(n):
    def generate_unique_key(existing_keys):
        """Generate a unique key not in the existing keys."""
        while True:
            key = random.choice(string.ascii_lowercase)  # Randomly select a lowercase letter
            if key not in existing_keys:  # Check if the key is unique
                return key  # Return the unique key

    def generate_key_value_pair(existing_keys):
        """Generate a unique key-value pair."""
        key = generate_unique_key(existing_keys)  # Get a unique key
        value = random.randrange(101)  # Generate a random integer value between 0 and 100
        return key, value  # Return the key-value pair

    keys = set()  # Create an empty set to track unique keys
    result = {}  # Initialize an empty dictionary to store key-value pairs
    while len(keys) < n:  # Continue until we have `n` unique keys
        key, value = generate_key_value_pair(keys)  # Generate a unique key-value pair
        result[key] = value  # Add the key-value pair to the dictionary
        keys.add(key)  # Add the key to the set of unique keys
    return result  # Return the generated dictionary


# Function to generate a list of random dictionaries
def generate_list_of_dicts():
    """Generate a list of dictionaries, each with random sizes and contents."""
    return [generate_dict(random.randrange(1, 10)) for _ in range(2, 11)]  # Generate between 2 and 10 dictionaries


# Function to calculate key occurrences across dictionaries
def calculate_key_occurrences(dict_list):
    """Count how many times each key appears across all dictionaries."""
    def update_occurrences(occurrences, keys):
        """Update the occurrences count for the keys of a single dictionary."""
        for key in keys:  # Iterate over all keys in the current dictionary
            occurrences[key] = occurrences.get(key, 0) + 1  # Increment the key's count in `occurrences`

    occurrences = {}  # Initialize an empty dictionary to track key occurrences
    for d in dict_list:  # Iterate over all dictionaries in the list
        update_occurrences(occurrences, d.keys())  # Update occurrences for the current dictionary's keys
    return occurrences  # Return the dictionary of key occurrences


# Function to track the maximum value and source dictionary for each key
def track_max_values(dict_list):
    """Track the maximum value and its source dictionary index for each key."""
    def update_key_tracker(tracker, d, index):
        """Update the tracker with key-value pairs from a single dictionary."""
        for key, value in d.items():  # Iterate over key-value pairs in the dictionary
            # If the key is not in the tracker or the value is greater than the current tracked value, update it
            if key not in tracker or value > tracker[key][0]:
                tracker[key] = (value, index)  # Store the new value and the index of the source dictionary

    tracker = {}  # Initialize an empty dictionary to track maximum values and their source dictionaries
    for i, d in enumerate(dict_list):  # Enumerate over dictionaries with their indices
        update_key_tracker(tracker, d, i)  # Update the tracker for the current dictionary
    return tracker  # Return the tracker with maximum values and their sources


# Function to build the final common dictionary
def build_common_dict(key_tracker, key_occurrences):
    """Create the final dictionary with renamed keys if necessary."""
    def rename_key(key, index, occurrences):
        """Rename the key with the dictionary index if it occurs in multiple dictionaries."""
        return f"{key}_{index+1}" if occurrences[key] > 1 else key  # Add index if the key occurs more than once

    result = {}  # Initialize an empty dictionary to store the final result
    for key, (value, index) in key_tracker.items():  # Iterate over the tracked keys, values, and indices
        final_key = rename_key(key, index, key_occurrences)  # Get the final key name (renamed if necessary)
        result[final_key] = value  # Add the key-value pair to the result dictionary
    return result  # Return the final dictionary


# Main execution flow
def main():
    # Step 1: Generate a list of random dictionaries
    dict_list = generate_list_of_dicts()  # Create a list of dictionaries with random contents

    # Step 2: Calculate how many times each key occurs across all dictionaries
    key_occurrences = calculate_key_occurrences(dict_list)  # Count key occurrences in all dictionaries

    # Step 3: Track the maximum value and the source dictionary for each key
    key_tracker = track_max_values(dict_list)  # Find the maximum value for each key and its source dictionary

    # Step 4: Build the final dictionary with renamed keys
    common_dict = build_common_dict(key_tracker, key_occurrences)  # Construct the final dictionary

    # Output the results
    print(dict_list)  # Print the list of generated dictionaries
    print(common_dict)  # Print the final dictionary with keys and their respective maximum values


# Call the main function
if __name__ == "__main__":
    main()  # Start the program by calling the main function