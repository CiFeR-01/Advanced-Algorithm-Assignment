import random

# Hash function using folding (grouping by 4 digits and summing)
def folding_hash(ic_number: str, table_size: int) -> int:
    parts = [ic_number[i:i+4] for i in range(0, 12, 4)]
    total = sum(int(part) for part in parts)
    return total % table_size

# Generate random Malaysian IC number: YYMMDDSSSSGG
def generate_ic():
    yy = f"{random.randint(50, 99):02}"  # Year
    mm = f"{random.randint(1, 12):02}"   # Month
    dd = f"{random.randint(1, 28):02}"   # Day (simplified)
    ssss = f"{random.randint(0, 9999):04}"
    gg = f"{random.randint(0, 99):02}"
    return yy + mm + dd + ssss + gg

# Insert into hash table with separate chaining
def insert_into_table(table_size, ic_list):
    table = [[] for _ in range(table_size)]
    collisions = 0
    for ic in ic_list:
        index = folding_hash(ic, table_size)
        if table[index]:
            collisions += 1
        table[index].append(ic)
    return collisions

# Run simulation for 10 rounds
def simulate():
    size1 = 1009
    size2 = 2003
    rounds = 10
    collisions1 = []
    collisions2 = []

    for round_num in range(rounds):
        ic_numbers = [generate_ic() for _ in range(1000)]
        col1 = insert_into_table(size1, ic_numbers)
        col2 = insert_into_table(size2, ic_numbers)
        collisions1.append(col1)
        collisions2.append(col2)
        print(f"Round {round_num + 1}: Collisions in table 1009 = {col1}, table 2003 = {col2}")

    avg1 = sum(collisions1) / rounds
    avg2 = sum(collisions2) / rounds
    print(f"\nAverage collisions for table size 1009: {avg1:.2f}")
    print(f"Average collisions for table size 2003: {avg2:.2f}")

if __name__ == "__main__":
    simulate()
