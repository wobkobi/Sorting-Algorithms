import os
import heapq

def sort_and_save_chunk(chunk, chunk_id):
    chunk.sort()
    chunk_filename = f"chunk_{chunk_id}.txt"
    with open(chunk_filename, 'w') as chunk_file:
        for item in chunk:
            chunk_file.write(f"{item}\n")
    return chunk_filename

def merge_sorted_chunks(chunk_files, output_file):
    min_heap = []
    chunk_file_pointers = []
    for i, chunk_filename in enumerate(chunk_files):
        chunk_file = open(chunk_filename, 'r')
        chunk_file_pointers.append(chunk_file)
        first_item = chunk_file.readline().strip()
        if first_item:
            heapq.heappush(min_heap, (int(first_item), i))

    with open(output_file, 'w') as out_file:
        while min_heap:
            smallest, file_index = heapq.heappop(min_heap)
            out_file.write(f"{smallest}\n")
            next_item = chunk_file_pointers[file_index].readline().strip()
            if next_item:
                heapq.heappush(min_heap, (int(next_item), file_index))

    for chunk_file in chunk_file_pointers:
        chunk_file.close()
        os.remove(chunk_file.name)

def external_merge_sort(input_file, output_file, chunk_size):
    chunk_files = []
    chunk = []
    chunk_id = 0

    with open(input_file, 'r') as in_file:
        for line in in_file:
            chunk.append(int(line.strip()))
            if len(chunk) == chunk_size:
                chunk_files.append(sort_and_save_chunk(chunk, chunk_id))
                chunk_id += 1
                chunk = []

    if chunk:
        chunk_files.append(sort_and_save_chunk(chunk, chunk_id))

    merge_sorted_chunks(chunk_files, output_file)