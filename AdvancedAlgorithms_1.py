import random

class HashTable:
    """
    A simple hash table implementation using separate chaining for collision resolution.
    """
    def __init__(self, size):
        """
        Initializes the hash table with a specified size.
        Each slot in the table is a list (chain) to store elements that hash to the same index.
        """
        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.collisions = 0 # Counter for collisions

    def _hash(self, ic_number_str):
        """
        Generates a hash code (index) for a given Malaysian IC number string.
        It uses the folding technique:
        1. The 12-digit IC number string is split into three 4-digit parts.
        2. These parts are converted to integers and summed.
        3. The sum is then modulo the hash table size to get the final index.

        Args:
            ic_number_str (str): A 12-digit string representing the Malaysian IC number.

        Returns:
            int: The calculated hash index for the IC number.

        Raises:
            ValueError: If the input IC number is not a valid 12-digit string.
        """
        # Validate the input IC number string
        if not isinstance(ic_number_str, str) or len(ic_number_str) != 12 or not ic_number_str.isdigit():
            raise ValueError("IC number must be a 12-digit string containing only digits.")

        # Split the 12-digit IC number string into three 4-digit parts
        # Example: "YYYYMMDDPBNNN#" -> "YYYY", "MMDD", "PBNN", "N#"
        # For simplicity and effectiveness, we'll take consecutive 4-digit chunks.
        part1 = int(ic_number_str[0:4])   # First 4 digits
        part2 = int(ic_number_str[4:8])   # Next 4 digits
        part3 = int(ic_number_str[8:12])  # Last 4 digits

        # Sum the integer values of these parts
        sum_of_parts = part1 + part2 + part3

        # Apply the modulo operator with the table size to get the hash index
        return sum_of_parts % self.size

    def insert(self, ic_number_str):
        """
        Inserts a Malaysian IC number into the hash table.
        It calculates the hash index and adds the IC number to the chain at that index.
        If the chain at the calculated index is not empty before adding the new element,
        it increments the collision counter.

        Args:
            ic_number_str (str): The 12-digit IC number string to insert.
        """
        try:
            index = self._hash(ic_number_str)

            # A collision occurs if the list (chain) at this index is not empty
            # before we add the current item.
            if len(self.table[index]) > 0:
                self.collisions += 1

            # Add the IC number to the end of the chain (list) at the calculated index
            self.table[index].append(ic_number_str)
        except ValueError as e:
            print(f"Error inserting IC number '{ic_number_str}': {e}")

    def get_total_collisions(self):
        """
        Returns the total number of collisions recorded during insertions into this hash table.

        Returns:
            int: The total count of collisions.
        """
        return self.collisions

def generate_unique_ic_numbers(count):
    """
    Generates a list of unique 12-digit random IC number strings.
    Each IC number is a sequence of 12 random digits.

    Args:
        count (int): The number of unique IC numbers to generate.

    Returns:
        list: A list of unique 12-digit IC number strings.
    """
    ic_numbers = set() # Use a set to ensure uniqueness
    while len(ic_numbers) < count:
        # Generate a random 12-digit string
        # Each digit is randomly chosen from 0 to 9
        digits = "".join([str(random.randint(0, 9)) for _ in range(12)])
        ic_numbers.add(digits)
    return list(ic_numbers) # Convert set to list for iteration

# Main program execution block
if __name__ == "__main__":
    num_ics_to_insert = 1000 # Number of IC numbers to insert in each round
    num_rounds = 10          # Number of rounds for each hash table size
    
    # Define the sizes of the two hash tables
    table_sizes = [1009, 2003] # Prime numbers are often chosen for hash table sizes
    
    # Dictionary to store collision data for all rounds for each table size
    all_table_collisions = {size: [] for size in table_sizes}

    print("--- Starting Hashing Simulation ---\n")

    # Iterate through each specified hash table size
    for table_size in table_sizes:
        print(f"Simulating for Hash Table Size: {table_size}")
        round_collisions = [] # List to store collision counts for current table size's rounds
        
        # Run the simulation for the specified number of rounds
        for round_num in range(1, num_rounds + 1):
            # Create a new hash table instance for each round to reset collision count
            hash_table = HashTable(table_size)
            
            # Generate 1000 unique IC numbers for the current round
            ic_numbers_for_round = generate_unique_ic_numbers(num_ics_to_insert)
            
            # Display the first 10 generated IC numbers for this round
            print(f"  Round {round_num}: Generated {num_ics_to_insert} IC numbers. ")
            for i, ic in enumerate(ic_numbers_for_round[:10]):
                print(f"    - {ic}")

            # Insert each generated IC number into the hash table
            for ic in ic_numbers_for_round:
                hash_table.insert(ic)
            
            # Get the total collisions recorded for this round
            collisions_this_round = hash_table.get_total_collisions()
            round_collisions.append(collisions_this_round) # Store the collision count
            
            # Display total collisions for the current round
            print(f"  Round {round_num}: Total Collisions = {collisions_this_round}")
            
        # Store all round collision data for the current table size
        all_table_collisions[table_size] = round_collisions
        
        # Calculate the average collisions for this hash table size over all rounds
        average_collisions = sum(round_collisions) / num_rounds
        
        # Display the average collisions for the current table size
        print(f"Average Collisions for Table Size {table_size}: {average_collisions:.2f}\n")

    print("--- Simulation Complete ---")
