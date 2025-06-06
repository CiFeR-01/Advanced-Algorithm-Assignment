import random

def folding_hash(ic_number: str, table_size: int) -> int:
    """
    Computes a hash value for a Malaysian IC number using the folding method.

    The IC number is split into three 4-digit parts, these parts are summed,
    and the result is modulo the table_size.

    Args:
        ic_number: The 12-digit Malaysian IC number string.
        table_size: The size of the hash table.

    Returns:
        The computed hash index.
    """
    # Split the 12-digit IC number into three 4-digit parts
    parts = [ic_number[i:i+4] for i in range(0, 12, 4)]
    
    # Sum the integer values of these parts
    total = sum(int(part) for part in parts)
    
    # Apply modulo to get the hash index within the table size
    return total % table_size

def generate_ic() -> str:
    """
    Generates a random 12-digit Malaysian IC number in the format YYMMDDSSSSGG.
    """
    # Generate year (50-99 for simplicity)
    yy = f"{random.randint(50, 99):02}" 
    # Generate month (01-12)
    mm = f"{random.randint(1, 12):02}" 
    # Generate day (simplified to 01-28 to avoid complex date validation)
    dd = f"{random.randint(1, 28):02}" 
    # Generate a random 4-digit serial number
    ssss = f"{random.randint(0, 9999):04}"
    # Generate a random 2-digit state/gender code
    gg = f"{random.randint(0, 99):02}"
    
    return yy + mm + dd + ssss + gg

def insert_into_table(table_size: int, ic_list: list[str]) -> int:
    """
    Inserts a list of IC numbers into a hash table using separate chaining
    and counts the number of collisions.

    Args:
        table_size: The size of the hash table.
        ic_list: A list of IC number strings to insert.

    Returns:
        The total number of collisions encountered during insertion.
    """
    # Initialize the hash table with empty lists for separate chaining
    table = [[] for _ in range(table_size)]
    collisions = 0

    for ic in ic_list:
        # Get the hash index for the current IC number
        index = folding_hash(ic, table_size)
        
        # If the slot at the index is not empty, a collision has occurred
        if table[index]:
            collisions += 1
        
        # Add the IC number to the chain at the computed index
        table[index].append(ic)
    
    return collisions

def simulate():
    """
    Runs the hash table simulation for multiple rounds, comparing collision
    counts for two different table sizes.
    """
    # Define the two hash table sizes to compare (often prime numbers are preferred)
    size1 = 1009
    size2 = 2003
    num_rounds = 2
    
    # Lists to store collision counts for each table size per round
    collisions_size1 = []
    collisions_size2 = []

    print("Starting Hash Table Collision Simulation...\n")

    for round_num in range(num_rounds):
        # Generate 1000 unique IC numbers for the current round
        ic_numbers_to_insert = [generate_ic() for _ in range(1000)]
        
        # Insert into table 1 and count collisions
        current_collisions_size1 = insert_into_table(size1, ic_numbers_to_insert)
        collisions_size1.append(current_collisions_size1)
        
        # Insert into table 2 and count collisions
        current_collisions_size2 = insert_into_table(size2, ic_numbers_to_insert)
        collisions_size2.append(current_collisions_size2)
        
        print(f"Round {round_num + 1}: Collisions in table size {size1} = {current_collisions_size1}, "
              f"Collisions in table size {size2} = {current_collisions_size2}")

    # Calculate and print average collisions
    avg_collisions_size1 = sum(collisions_size1) / num_rounds
    avg_collisions_size2 = sum(collisions_size2) / num_rounds

    print("\n--- Simulation Summary ---")
    print(f"Average collisions for table size {size1}: {avg_collisions_size1:.2f}")
    print(f"Average collisions for table size {size2}: {avg_collisions_size2:.2f}")
    print("--------------------------")

if __name__ == "__main__":
    simulate()