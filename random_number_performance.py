#random_number_performance.py

import random
import threading
import time
import statistics

def generate_random_numbers(num_count=1000, min_val=0, max_val=10000):
    """
    Generates a list of random numbers within a specified range.
    """
    return [random.randint(min_val, max_val) for _ in range(num_count)]

# Global variables for storing thread-specific results and timings.
# A lock is used to synchronize access to these shared resources,
# preventing race conditions when multiple threads write concurrently.
thread_results = []
thread_start_times = {}
thread_end_times = {}
thread_lock = threading.Lock()

def thread_task(set_id):
    """
    The main task executed by each thread: generates random numbers and records
    its precise start and end times in nanoseconds.
    """
    start_time_thread = time.monotonic_ns()
    
    # Safely record thread's start time using the lock
    with thread_lock:
        thread_start_times[set_id] = start_time_thread

    numbers = generate_random_numbers() # Generate the set of random numbers
    
    end_time_thread = time.monotonic_ns()
    
    # Safely record thread's end time and generated numbers
    with thread_lock:
        thread_end_times[set_id] = end_time_thread
        thread_results.append({
            "set_id": set_id,
            "numbers": numbers,
            "start_time": start_time_thread,
            "end_time": end_time_thread
        })

def run_with_multithreading(num_sets=3, num_rounds=10):
    """
    Orchestrates the generation of random numbers using multiple threads
    over several rounds. Measures and displays the total and average
    elapsed times for multithreaded execution.
    """
    print(f"\n--- Running with Multithreading ({num_rounds} rounds) ---")
    round_times = []

    for round_num in range(1, num_rounds + 1):
        # Reset global data for each new round to ensure accuracy
        global thread_results, thread_start_times, thread_end_times
        thread_results = []
        thread_start_times = {}
        thread_end_times = {}

        threads = []
        # Create and start individual threads for each set
        for i in range(num_sets):
            thread_name = f"Set_{i+1}"
            thread = threading.Thread(target=thread_task, args=(thread_name,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete their execution
        for thread in threads:
            thread.join()

        # Calculate the overall elapsed time for the round.
        # This is the span from the earliest thread start to the latest thread end.
        overall_start_time = float('inf')
        overall_end_time = 0

        with thread_lock: # Safely read collected thread times
            overall_start_time = min(thread_start_times.values())
            overall_end_time = max(thread_end_times.values())
        
        time_elapsed_ns = overall_end_time - overall_start_time
        round_times.append(time_elapsed_ns)
        print(f"Round {round_num}: Time Taken (T) = {time_elapsed_ns:,} ns")

    average_time_ns = statistics.mean(round_times)
    print(f"\nAverage Time Taken (Multithreading) over {num_rounds} rounds: {average_time_ns:,.0f} ns")
    return round_times


def run_without_multithreading(num_sets=3, num_rounds=10):
    """
    Executes the random number generation sequentially (without threads)
    over several rounds. Measures and displays the total and average
    elapsed times for sequential execution.
    """
    print(f"\n--- Running without Multithreading ({num_rounds} rounds) ---")
    round_times = []

    for round_num in range(1, num_rounds + 1):
        # Record start time before sequential execution
        start_time_sequential = time.monotonic_ns()
        
        sequential_results = []
        # Generate each set of random numbers one after another
        for i in range(num_sets):
            numbers = generate_random_numbers()
            sequential_results.append({f"Set_{i+1}": numbers})
            
        # Record end time after all sets are generated
        end_time_sequential = time.monotonic_ns()
        
        time_elapsed_ns = end_time_sequential - start_time_sequential
        round_times.append(time_elapsed_ns)
        print(f"Round {round_num}: Time Taken (T) = {time_elapsed_ns:,} ns")

    average_time_ns = statistics.mean(round_times)
    print(f"\nAverage Time Taken (Without Multithreading) over {num_rounds} rounds: {average_time_ns:,.0f} ns")
    return round_times

# Main execution block
if __name__ == "__main__":
    # Perform tests for both multithreaded and sequential scenarios
    multithreaded_times = run_with_multithreading(num_sets=3, num_rounds=10)
    sequential_times = run_without_multithreading(num_sets=3, num_rounds=10)

    # Print a final comparative summary of the test results
    print("\n--- Summary ---")
    print(f"Multithreaded Round Times: {[f'{t:,} ns' for t in multithreaded_times]}")
    print(f"Sequential Round Times: {[f'{t:,} ns' for t in sequential_times]}")
    print(f"Average Multithreaded Time: {statistics.mean(multithreaded_times):,.0f} ns")
    print(f"Average Sequential Time: {statistics.mean(sequential_times):,.0f} ns")
