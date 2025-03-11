import string
import random


# Function to generate a dictionary with `n` unique keys
def generate_dict(n):
    mydict = {}  # Create an empty dictionary to store key-value pairs
    keys = set()  # Create a set to keep track of unique keys already added
    while len(keys) < n:  # Continue until we have `n` unique keys
        key = random.choice(string.ascii_lowercase)  # Randomly choose a lowercase letter as the key
        if key not in keys:  # If the key is not already in the set
            mydict[key] = random.randrange(101)  # Assign a random integer (0 to 100) as the value for the key
            keys.add(key)  # Add the key to the set of unique keys
    return mydict  # Return the generated dictionary


l1 = []  # Create an empty list to store dictionaries
for i in range(2, 11):  # Loop through numbers from 2 to 10 (inclusive)
    l1.append(generate_dict(random.randrange(1, 10)))  # Append a dictionary with a random number of keys (1 to 9)

# Dictionary to track the number of times each key appears across all dictionaries
key_occurrences = {}
for d in l1:  # Iterate over each dictionary in `l1`
    for key in d.keys():  # Iterate over the keys in the current dictionary
        if key not in key_occurrences:  # If the key is not already tracked
            key_occurrences[key] = 0  # Initialize its count to 0
        key_occurrences[key] += 1  # Increment the count for this key

# Create a temporary structure to track the maximum value and source dictionary index for each key
key_tracker = {}

for i, d in enumerate(l1):  # Enumerate over `l1` to get both the dictionary and its index
    for key, value in d.items():  # Iterate over the key-value pairs in the current dictionary
        if key not in key_tracker:  # If the key is not already in the tracker
            # Add the key with its value and the index of the dictionary
            key_tracker[key] = (value, i)
        else:  # If the key is already in the tracker
            # Compare the current value with the existing tracked value
            current_value, current_index = key_tracker[key]
            if value > current_value:  # Update only if the new value is greater
                key_tracker[key] = (value, i)

# Create the final `common_dict` with keys appropriately renamed (if necessary)
common_dict = {}
for key, (value, index) in key_tracker.items():  # Iterate over the key-value pairs in `key_tracker`
    if key_occurrences[key] == 1:  # If the key appears in only one dictionary
        common_dict[key] = value  # Add the key as is to `common_dict`
    else:  # If the key appears in multiple dictionaries
        # Rename the key to include the dictionary index (add 1 to make it 1-based indexing)
        common_dict[f"{key}_{index+1}"] = value

# Print the list of dictionaries and the resulting `common_dict`
print(l1)  # Print all the generated dictionaries
print(common_dict)  # Print the final dictionary with keys and their respective maximum values
