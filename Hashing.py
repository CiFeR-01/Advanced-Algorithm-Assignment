import random
import datetime

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.collisions = 0

    def _hash(self, ic_number_str):
        # Generates hash code for a 12-digit Malaysian IC using a folding technique.
        numeric_ic_str = ic_number_str.replace('-', '')

        if not (isinstance(numeric_ic_str, str) and
                len(numeric_ic_str) == 12 and
                numeric_ic_str.isdigit()):
            raise ValueError(
                f"Processed IC number '{numeric_ic_str}' is not a valid 12-digit numeric string."
            )

        # Split the 12-digit IC number string into three 4-digit parts
        part1 = int(numeric_ic_str[0:4])
        part2 = int(numeric_ic_str[4:8])
        part3 = int(numeric_ic_str[8:12])

        sum_of_parts = part1 + part2 + part3
        return sum_of_parts % self.size

    def insert(self, ic_number_str):
        try:
            index = self._hash(ic_number_str)

            # Check for collision: if the chain is not empty, a collision occurred
            if len(self.table[index]) > 0:
                self.collisions += 1

            self.table[index].append(ic_number_str)
        except ValueError as e:
            print(f"Error inserting IC number '{ic_number_str}': {e}")

    def get_total_collisions(self):
        return self.collisions

    def display_table(self, limit=None):
        print(f"\n--- Hash Table with size {self.size} Contents ---")
        if limit is not None and limit < self.size:
            print(f"--- Displaying first {limit} entries ---")

        display_count = 0
        for i, chain in enumerate(self.table):
            if limit is not None and display_count >= limit:
                break
            
            if chain:
                print(f"table[{i}] --> {' --> '.join(chain)}")
            else:
                print(f"table[{i}]")
            display_count += 1
            
        print(f"--- End of Hash Table Contents (Size {self.size}) ---\n")


def generate_random_date_yymmdd():
    return datetime.date(random.randrange(1950, 2006), random.randrange(1, 13), random.randrange(1, 29)).strftime('%y%m%d')

def generate_random_pb_code():
    ic_codes = [
        "01", "21", "22", "23", "24",   # Johor
        "02", "25", "26", "27",   # Kedah
        "03", "28", "29",   # Kelantan
        "04", "30",   # Melaka
        "05", "31", "59",   # Negeri Sembilan
        "06", "32", "33",   # Pahang
        "07", "34", "35",   # Penang
        "08", "36", "37", "38", "39",   # Perak
        "09", "40",   # Perlis
        "10", "41", "42", "43", "44",   # Selangor
        "11", "45", "46",   # Terengganu
        "12", "47", "48", "49",   # Sabah
        "13", "50", "51", "52", "53",   # Sarawak
        "14", "54", "55", "56", "57",   # W.P.(KL)
        "15", "58",   # W.P.(Labuan)
        "16",   # W.P.(Putrajaya)
        "82"    # Unknown State
    ]
    return random.choice(ic_codes)

def generate_random_four_digits():
    return str(random.randint(0, 9999)).zfill(4)

def generate_unique_ic_numbers(count):
    ic_numbers = set()
    print(f"Generating {count} unique IC numbers...")
    while len(ic_numbers) < count:
        yymmdd = generate_random_date_yymmdd()
        pb = generate_random_pb_code()
        xxxx = generate_random_four_digits()
        
        formatted_ic = f"{yymmdd}-{pb}-{xxxx}"
        ic_numbers.add(formatted_ic)
    print(f"Finished generating {len(ic_numbers)} unique IC numbers.\n")
    return list(ic_numbers)

if __name__ == "__main__":
    num_ics_to_insert = 1000
    num_rounds = 10

    # Define the sizes of the two hash tables.
    # Prime numbers are often chosen for hash table sizes to reduce collisions.
    table_sizes = [1009, 2003]
    
    all_table_collisions = {size: [] for size in table_sizes}
    average_collisions_per_table = {}

    print("--- Starting Hashing Simulation ---")

    for table_size in table_sizes:
        print(f"\nSimulating for Hash Table Size: {table_size}")
        round_collisions = []
        
        for round_num in range(1, num_rounds + 1):
            hash_table = HashTable(table_size)
            ic_numbers_for_round = generate_unique_ic_numbers(num_ics_to_insert)
            
            print(f"  Round {round_num}: Inserting {num_ics_to_insert} IC numbers into table of size {table_size}...")

            for ic in ic_numbers_for_round:
                hash_table.insert(ic)
            
            # Display the first 20 entries of the hash table for visualization
            hash_table.display_table(limit=20)

            collisions_this_round = hash_table.get_total_collisions()
            round_collisions.append(collisions_this_round)
            
            print(f"  Round {round_num}: Total Collisions = {collisions_this_round}")
            
        all_table_collisions[table_size] = round_collisions
        
        average_collisions = sum(round_collisions) / num_rounds
        average_collisions_per_table[table_size] = average_collisions
        
    print("\n--- Simulation Complete ---")
    
    print("\n--- Summary of Collisions Per Round ---")
    print(f"----------------------------------------------------------------------------------------")
    print(f"| {'Round':<8} | {'Table 1 (Size 1009) Collisions':<35} | {'Table 2 (Size 2003) Collisions':<35} |")
    print(f"----------------------------------------------------------------------------------------")
    for i in range(num_rounds):
        col1 = all_table_collisions[1009][i]
        col2 = all_table_collisions[2003][i]
        print(f"| {i+1:<8} | {col1:<35} | {col2:<35} |")

    print(f"----------------------------------------------------------------------------------------")    

    print("\n--- Average Collisions Across All Rounds ---")
    for table_size, avg_collisions in average_collisions_per_table.items():
        print(f"Average Collisions for Table Size {table_size}: {avg_collisions:.2f}")
