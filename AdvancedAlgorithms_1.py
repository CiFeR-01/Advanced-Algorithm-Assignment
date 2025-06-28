import random
import datetime

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.collisions = 0  # Counter for collisions

    def _hash(self, ic_number_str):
        """
        Generates a hash code for a Malaysian IC Number using a folding technique.
        The IC number is expected as a 12-digit string (e.g., "YYMMDD-PB-XXXX" without hyphens).

        This function strictly processes 12-digit numeric strings.
        It is designed for the standard Malaysian IC Number format.
        It CANNOT handle other formats like a 16-digit IC number, as it explicitly
        validates the input to be a 12-digit string and relies on splitting
        it into three 4-digit parts. Passing a different length string would
        result in a ValueError.
        
        Folding Technique:
        The 12-digit numeric string is conceptually divided into three 4-digit parts.
        These parts are then summed, and the modulo operator is applied with the
        hash table's size to derive the final hash index.
        """
        # Remove hyphens for internal processing
        numeric_ic_str = ic_number_str.replace('-', '')

        # Validate the input numeric IC number string after removing hyphens
        # It should now be a 12-digit string containing only digits.
        if not isinstance(numeric_ic_str, str) or len(numeric_ic_str) != 12 or not numeric_ic_str.isdigit():
            # This should ideally not happen if generate_unique_ic_numbers is working correctly,
            # but it's a good safeguard for unexpected inputs.
            raise ValueError(
                f"Processed IC number '{numeric_ic_str}' is not a valid 12-digit numeric string."
            )

        # Split the 12-digit IC number string into three 4-digit parts
        part1 = int(numeric_ic_str[0:4])   # First 4 digits (YYMM)
        part2 = int(numeric_ic_str[4:8])   # Next 4 digits (DDPB)
        part3 = int(numeric_ic_str[8:12])  # Last 4 digits (XXXX)

        # Sum the integer values of these parts (folding)
        sum_of_parts = part1 + part2 + part3

        # Apply the modulo operator with the table size to get the hash index
        return sum_of_parts % self.size

    def insert(self, ic_number_str):
        """
        Inserts an IC number into the hash table.
        Uses separate chaining to handle collisions: if multiple IC numbers
        hash to the same index, they are stored in a list (chain) at that index.
        Increments a collision counter if an item is inserted into a non-empty chain.
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
        """Returns the total number of collisions recorded during insertions."""
        return self.collisions

    def display_table(self, limit=None): # Added limit parameter
        """
        Displays the contents of the hash table. 
        Each entry shows the index and any IC numbers stored at that index.
        Numbers that caused collisions will be displayed as a chain.
        If 'limit' is specified, only the first 'limit' entries are displayed.
        """
        print(f"\n--- Hash Table with size {self.size} Contents ---")
        if limit and limit < self.size:
            print(f"--- Displaying first {limit} entries ---")

        display_count = 0
        for i, chain in enumerate(self.table):
            if limit and display_count >= limit:
                break
            if chain:  # Only print non-empty chains
                # Join all IC numbers in the chain with ' --> ' to show collisions
                print(f"table[{i}] --> {' --> '.join(chain)}")
            else:
                # Print empty entries as well, similar to the provided image examples
                print(f"table[{i}]")
            display_count += 1
            
        print(f"--- End of Hash Table Contents (Size {self.size}) ---\n")


def generate_random_date_yymmdd():
    """Generates a random date in YYMMDD format for IC numbers."""
    start_date = datetime.date(1950, 1, 1)
    end_date = datetime.date(2005, 12, 31) # Limiting birth year for realism
    
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    
    return random_date.strftime('%y%m%d')

def generate_random_pb_code():
    """
    Generates a random two-digit place of birth (PB) code.
    These codes are based on common Malaysian IC birth codes for realism.
    """

    ic_codes = [
        "01", "21", "22", "23", "24",  # Johor
        "02", "25", "26", "27",  # Kedah
        "03", "28", "29",  # Kelantan
        "04", "30",  # Melaka
        "05", "31", "59",  # Negeri Sembilan
        "06", "32", "33",  # Pahang
        "07", "34", "35",  # Penang
        "08", "36", "37", "38", "39",  # Perak
        "09", "40",  # Perlis
        "10", "41", "42", "43", "44",  # Selangor
        "11", "45", "46",  # Terengganu
        "12", "47", "48", "49",  # Sabah
        "13", "50", "51", "52", "53",  # Sarawak
        "14", "54", "55", "56", "57",  # W.P.(KL)
        "15", "58",  # W.P.(Labuan)
        "16",  # W.P.(Putrajaya)
        "82"   # Unknown State
    ]
    return random.choice(ic_codes)

def generate_random_four_digits():
    """Generates a random four-digit number (0000-9999), padded with leading zeros."""
    return str(random.randint(0, 9999)).zfill(4)

def generate_unique_ic_numbers(count):
    """
    Generates a list of unique Malaysian IC numbers in YYMMDD-PB-XXXX format.
    The function ensures that all generated IC numbers are unique within the list.
    """
    ic_numbers = set()  # Use a set to ensure uniqueness
    print(f"Generating {count} unique IC numbers...")
    while len(ic_numbers) < count:
        yymmdd = generate_random_date_yymmdd()
        pb = generate_random_pb_code() # Use the new function for realistic PB codes
        xxxx = generate_random_four_digits()
        
        formatted_ic = f"{yymmdd}-{pb}-{xxxx}"
        ic_numbers.add(formatted_ic)
    print(f"Finished generating {len(ic_numbers)} unique IC numbers.\n")
    return list(ic_numbers)  # Convert set to list for iteration

# Main program execution block
if __name__ == "__main__":
    num_ics_to_insert = 1000  # Number of IC numbers to insert in each round, as required
    num_rounds = 10           # Number of rounds for each hash table size, as required

    # Define the sizes of the two hash tables as required
    table_sizes = [1009, 2003]  # Prime numbers are often chosen for hash table sizes
    
    # Dictionary to store collision data for all rounds for each table size
    all_table_collisions = {size: [] for size in table_sizes}
    # Dictionary to store average collisions for each table size
    average_collisions_per_table = {}

    print("--- Starting Hashing Simulation ---")

    # Iterate through each specified hash table size
    for table_size in table_sizes:
        print(f"\nSimulating for Hash Table Size: {table_size}")
        round_collisions = []  # List to store collision counts for current table size's rounds
        
        # Run the simulation for the specified number of rounds
        for round_num in range(1, num_rounds + 1):
            # Create a new hash table instance for each round to reset collision count
            hash_table = HashTable(table_size)
            
            # Generate IC numbers for the current round
            ic_numbers_for_round = generate_unique_ic_numbers(num_ics_to_insert)
            
            print(f"  Round {round_num}: Inserting {num_ics_to_insert} IC numbers into table of size {table_size}...")

            # Insert each generated IC number into the hash table
            for ic in ic_numbers_for_round:
                hash_table.insert(ic)
            
            # Display the first 20 entries of the hash table for each round, as requested
            hash_table.display_table(limit=20)

            # Get the total collisions recorded for this round
            collisions_this_round = hash_table.get_total_collisions()
            round_collisions.append(collisions_this_round)  # Store the collision count
            
            # Display total collisions for the current round, as required
            print(f"  Round {round_num}: Total Collisions = {collisions_this_round}")
            
        # Store all round collision data for the current table size
        all_table_collisions[table_size] = round_collisions
        
        # Calculate the average collisions for this hash table size over all rounds
        average_collisions = sum(round_collisions) / num_rounds
        average_collisions_per_table[table_size] = average_collisions # Store average for later display
        
    print("\n--- Simulation Complete ---")
    
    # Display summary of all collisions for all tables, as required (uncommented)
    print("\n--- Summary of Collisions Per Round ---")
    print(f"----------------------------------------------------------------------------------------")
    print(f"| {'Round':<8} | {'Table 1 (Size 1009) Collisions':<35} | {'Table 2 (Size 2003) Collisions':<35} |")
    print(f"----------------------------------------------------------------------------------------")
    for i in range(num_rounds):
        # Retrieve collision counts for both table sizes for the current round
        col1 = all_table_collisions[1009][i]
        col2 = all_table_collisions[2003][i]
        print(f"| {i+1:<8} | {col1:<35} | {col2:<35} |")

    print(f"----------------------------------------------------------------------------------------")    

    # Display average collisions for each table at the end, as requested
    print("\n--- Average Collisions Across All Rounds ---")
    for table_size, avg_collisions in average_collisions_per_table.items():
        print(f"Average Collisions for Table Size {table_size}: {avg_collisions:.2f}")
