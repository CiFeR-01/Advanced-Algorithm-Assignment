import random
import datetime

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.collisions = 0  # Counter for collisions

    def _hash(self, ic_number_str):
        # The IC number string is expected in "YYMMDD-PB-XXXX" format (14 characters long)
        # We need to remove the hyphens to get a 12-digit numeric string for the original hash logic.
        
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

        # Sum the integer values of these parts
        sum_of_parts = part1 + part2 + part3

        # Apply the modulo operator with the table size to get the hash index
        return sum_of_parts % self.size

    def insert(self, ic_number_str):
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
        return self.collisions

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
    Generates a random two-digit place of birth (PB) code 
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
    """
    ic_numbers = set()  # Use a set to ensure uniqueness
    while len(ic_numbers) < count:
        yymmdd = generate_random_date_yymmdd()
        pb = generate_random_pb_code() # Use the new function for realistic PB codes
        xxxx = generate_random_four_digits()
        
        formatted_ic = f"{yymmdd}-{pb}-{xxxx}"
        ic_numbers.add(formatted_ic)
    return list(ic_numbers)  # Convert set to list for iteration

# Main program execution block
if __name__ == "__main__":
    num_ics_to_insert = 1000  # Number of IC numbers to insert in each round
    num_rounds = 10           # Number of rounds for each hash table size
    
    # Define the sizes of the two hash tables
    table_sizes = [1009, 2003]  # Prime numbers are often chosen for hash table sizes
    
    # Dictionary to store collision data for all rounds for each table size
    all_table_collisions = {size: [] for size in table_sizes}

    print("--- Starting Hashing Simulation ---")

    # Iterate through each specified hash table size
    for table_size in table_sizes:
        print(f"\nSimulating for Hash Table Size: {table_size}")
        round_collisions = []  # List to store collision counts for current table size's rounds
        
        # Run the simulation for the specified number of rounds
        for round_num in range(1, num_rounds + 1):
            # Create a new hash table instance for each round to reset collision count
            hash_table = HashTable(table_size)
            
            # Generate 1000 unique IC numbers for the current round
            ic_numbers_for_round = generate_unique_ic_numbers(num_ics_to_insert)
            
            print(f"  Round {round_num}: Generated {num_ics_to_insert} IC numbers. ")
            # Display the first 10 generated IC numbers for this round for verification
            print("  Sample ICs generated for this round:")
            for i, ic in enumerate(ic_numbers_for_round[:10]):
                print(f"    - {ic}")

            # Insert each generated IC number into the hash table
            for ic in ic_numbers_for_round:
                hash_table.insert(ic)
            
            # Get the total collisions recorded for this round
            collisions_this_round = hash_table.get_total_collisions()
            round_collisions.append(collisions_this_round)  # Store the collision count
            
            # Display total collisions for the current round
            print(f"  Round {round_num}: Total Collisions = {collisions_this_round}")
            
        # Store all round collision data for the current table size
        all_table_collisions[table_size] = round_collisions
        
        # Calculate the average collisions for this hash table size over all rounds
        average_collisions = sum(round_collisions) / num_rounds
        
        # Display the average collisions for the current table size
        print(f"Average Collisions for Table Size {table_size}: {average_collisions:.2f}")

    print("\n--- Simulation Complete ---")
    
    # Optional: Print summary of all collisions for all tables
    print("\n--- Summary of Collisions Per Round ---")
    print(f"{'Round':<8} {'Table 1 (Size 1009) Collisions':<35} {'Table 2 (Size 2003) Collisions':<35}")
    for i in range(num_rounds):
        col1 = all_table_collisions[1009][i]
        col2 = all_table_collisions[2003][i]
        print(f"{i+1:<8} {col1:<35} {col2:<35}")
