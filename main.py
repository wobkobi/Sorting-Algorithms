import time
import random
import importlib

# List of available sorting algorithms
ALGORITHMS = {
    'bubble_sort': 'bubble_sort',
    'quick_sort': 'quick_sort',
    'merge_sort': 'merge_sort',
    'bitonic_sort': 'bitonic_sort',
    'bead_sort': 'bead_sort',
    'block_sort': 'block_sort',
    'bogo_sort': 'bogo_sort',
    'bozo_sort': 'bozo_sort',
    'bucket_sort': 'bucket_sort',
    'burst_sort': 'burst_sort',
    'cocktail_shaker_sort': 'cocktail_shaker_sort',
    'comb_sort': 'comb_sort',
    'counting_sort': 'counting_sort',
    'cycle_sort': 'cycle_sort',
    'external_merge_sort': 'external_merge_sort',
    'flashsort': 'flashsort',
    # Add other sorting algorithms here
}

def generate_random_list(size):
    return [random.randint(1, 10000) for _ in range(size)]

def main():
    sort_type = input("Enter the sort type: ").strip()
    
    if sort_type not in ALGORITHMS:
        print(f"Unknown sort type: {sort_type}")
        return

    # Dynamically import the selected sorting algorithm
    module = importlib.import_module(f'algorithms.{ALGORITHMS[sort_type]}')
    sort_function = getattr(module, ALGORITHMS[sort_type])
    
    # Generate a list of 10,000 random integers
    data = generate_random_list(10000)

    # Time the sorting process
    start_time = time.time()
    sorted_data = sort_function(data)
    end_time = time.time()
    
    print(f"Sorting {len(data)} items using {sort_type} took {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    main()
