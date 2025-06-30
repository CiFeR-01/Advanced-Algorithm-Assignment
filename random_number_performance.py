import random
import threading
import time
import statistics
from typing import List, Dict, Any

# Overall simulation parameters, defined globally as requested.
# These values will be used by both multithreaded and sequential tests.
GLOBAL_NUM_SETS = 3
GLOBAL_NUM_ROUNDS = 10
GLOBAL_NUM_RANDOM_NUMBERS_PER_SET = 100
GLOBAL_MIN_VAL = 0
GLOBAL_MAX_VAL = 10000

def generate_random_numbers(num_count: int = GLOBAL_NUM_RANDOM_NUMBERS_PER_SET, 
                            min_val: int = GLOBAL_MIN_VAL, 
                            max_val: int = GLOBAL_MAX_VAL) -> List[int]:
    # Generates a list of random numbers within a specified range.
    return [random.randint(min_val, max_val) for _ in range(num_count)]

# Global variables and lock for thread synchronization.
thread_results: List[Dict[str, Any]] = []
thread_start_times: Dict[str, int] = {}
thread_end_times: Dict[str, int] = {}
thread_lock = threading.Lock()

def thread_task(set_id: str) -> None:
    # Generates random numbers and records thread-specific start/end times.
    start_time_thread = time.monotonic_ns()
    
    with thread_lock: # Safely record thread's start time
        thread_start_times[set_id] = start_time_thread

    numbers = generate_random_numbers(GLOBAL_NUM_RANDOM_NUMBERS_PER_SET, GLOBAL_MIN_VAL, GLOBAL_MAX_VAL) # Generate numbers
    
    end_time_thread = time.monotonic_ns()
    
    with thread_lock: # Safely record thread's end time and results
        thread_end_times[set_id] = end_time_thread
        thread_results.append({
            "set_id": set_id,
            "numbers": numbers,
            "start_time": start_time_thread,
            "end_time": end_time_thread
        })

def run_with_multithreading() -> List[int]:
    # Runs random number generation using multiple threads and measures performance.
    print(f"\n--- Running with Multithreading ({GLOBAL_NUM_ROUNDS} rounds, {GLOBAL_NUM_SETS} sets of {GLOBAL_NUM_RANDOM_NUMBERS_PER_SET} numbers) ---")
    round_times: List[int] = []

    for round_num in range(1, GLOBAL_NUM_ROUNDS + 1):
        # Reset global data for each new round.
        global thread_results, thread_start_times, thread_end_times
        thread_results = []
        thread_start_times = {}
        thread_end_times = {}

        threads: List[threading.Thread] = []
        for i in range(GLOBAL_NUM_SETS): # Create and start threads.
            thread_name = f"Set_{i+1}"
            thread = threading.Thread(
                target=thread_task,
                args=(thread_name,)
            )
            threads.append(thread)
            thread.start()

        for thread in threads: # Wait for all threads to complete.
            thread.join()

        overall_start_time = float('inf')
        overall_end_time = 0

        with thread_lock: # Calculate overall elapsed time.
            if thread_start_times and thread_end_times:
                overall_start_time = min(thread_start_times.values())
                overall_end_time = max(thread_end_times.values())
            else:
                print(f"Warning: No thread times recorded for Round {round_num}. Skipping time calculation.")
                continue

        time_elapsed_ns = overall_end_time - overall_start_time
        round_times.append(time_elapsed_ns)
        print(f"Round {round_num}: Time Taken (T) = {time_elapsed_ns:,} ns")

    if round_times:
        average_time_ns = statistics.mean(round_times)
        print(f"\nAverage Time Taken (Multithreading) over {GLOBAL_NUM_ROUNDS} rounds: {average_time_ns:,.0f} ns")
    else:
        print("\nCould not calculate average time for Multithreading (no valid rounds recorded).")
    return round_times


def run_without_multithreading() -> List[int]:
    # Runs random number generation sequentially and measures performance.
    print(f"\n--- Running without Multithreading ({GLOBAL_NUM_ROUNDS} rounds, {GLOBAL_NUM_SETS} sets of {GLOBAL_NUM_RANDOM_NUMBERS_PER_SET} numbers) ---")
    round_times: List[int] = []

    for round_num in range(1, GLOBAL_NUM_ROUNDS + 1):
        start_time_sequential = time.monotonic_ns() # Record start time.
        
        sequential_results: List[Dict[str, List[int]]] = []
        for i in range(GLOBAL_NUM_SETS): # Generate numbers sequentially.
            numbers = generate_random_numbers(GLOBAL_NUM_RANDOM_NUMBERS_PER_SET, GLOBAL_MIN_VAL, GLOBAL_MAX_VAL)
            sequential_results.append({f"Set_{i+1}": numbers})
            
        end_time_sequential = time.monotonic_ns() # Record end time.
        
        time_elapsed_ns = end_time_sequential - start_time_sequential
        round_times.append(time_elapsed_ns)
        print(f"Round {round_num}: Time Taken (T) = {time_elapsed_ns:,} ns")

    if round_times:
        average_time_ns = statistics.mean(round_times)
        print(f"\nAverage Time Taken (Without Multithreading) over {GLOBAL_NUM_ROUNDS} rounds: {average_time_ns:,.0f} ns")
    else:
        print("\nCould not calculate average time for Sequential (no valid rounds recorded).")
    return round_times

def main():
    # Orchestrates the random number generation performance comparison.

    # Perform tests for both multithreaded and sequential scenarios.
    # Functions now called without specific test parameters as they use globals.
    multithreaded_times = run_with_multithreading()
    sequential_times = run_without_multithreading()

    print("\n--- Final Performance Summary ---")
    
    if multithreaded_times: # Display multithreaded average.
        avg_multithreaded = statistics.mean(multithreaded_times)
        print(f"Multithreaded Average Time: {avg_multithreaded:,.0f} ns")
    else:
        avg_multithreaded = 0
        print("Multithreaded Average Time: N/A (no data)")

    if sequential_times: # Display sequential average.
        avg_sequential = statistics.mean(sequential_times)
        print(f"Sequential Average Time: {avg_sequential:,.0f} ns")
    else:
        avg_sequential = 0
        print("Sequential Average Time: N/A (no data)")

    if avg_multithreaded > 0 and avg_sequential > 0: # Calculate and display percentage difference.
        if avg_sequential > 0:
            percentage_diff = ((avg_sequential - avg_multithreaded) / avg_sequential) * 100
            if percentage_diff > 0:
                print(f"Multithreaded execution was {percentage_diff:.2f}% faster than Sequential.")
            elif percentage_diff < 0:
                print(f"Multithreaded execution was {-percentage_diff:.2f}% slower than Sequential.")
            else:
                print("Multithreaded and Sequential execution times were approximately the same.")
        else:
            print("Cannot calculate percentage difference as sequential average time is zero.")
    else:
        print("Not enough data to calculate percentage difference.")

if __name__ == "__main__":
    main()
