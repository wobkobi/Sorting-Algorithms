# Sorting Algorithms Benchmark Results

## Overall Top 20 Algorithms (by average time across sizes)

| Rank | Algorithms | Overall Average Time |
| ---- | ---------- | -------------------- |
| 1st | [Replacement Selection Sort](results/algorithms/Replacement_Selection_Sort.md), [Cubesort](results/algorithms/Cubesort.md) | 24us |
| 3rd | [Flash Sort](results/algorithms/Flash_Sort.md), [Shell Sort](results/algorithms/Shell_Sort.md), [Intro Sort](results/algorithms/Intro_Sort.md), [Spreadsort](results/algorithms/Spreadsort.md), [Merge Insertion Sort](results/algorithms/Merge_Insertion_Sort.md), [Bucket Sort](results/algorithms/Bucket_Sort.md), [Burst Sort](results/algorithms/Burst_Sort.md), [Patience Sort](results/algorithms/Patience_Sort.md) | 28us |
| 11th | [Franceschini's Method](results/algorithms/Franceschini's_Method.md), [Polyphase Merge Sort](results/algorithms/Polyphase_Merge_Sort.md), [Tree Sort](results/algorithms/Tree_Sort.md), [Tim Sort](results/algorithms/Tim_Sort.md), [Spaghetti Sort](results/algorithms/Spaghetti_Sort.md), [Comb Sort](results/algorithms/Comb_Sort.md) | 33us |
| 17th | [Hyper Quick](results/algorithms/Hyper_Quick.md) | 46us |
| 18th | [Merge Sort In-Place](results/algorithms/Merge_Sort_In-Place.md) | 47us |
| 19th | [MSD Radix Sort](results/algorithms/MSD_Radix_Sort.md), [Heap Sort](results/algorithms/Heap_Sort.md), [Strand Sort](results/algorithms/Strand_Sort.md), [MSD Radix Sort In-Place](results/algorithms/MSD_Radix_Sort_In-Place.md) | 49us |

*Note: The 20th rank falls within a tie group, so all tied algorithms are shown.*

## Skipped Algorithms

| Algorithm | Skipped At Size |
| --------- | --------------- |
| Bogo Sort | 12 |

## Detailed Benchmark Results

### Array Size: 5

| Rank | Algorithm(s) | Average Time | Median Time |
| ---- | ------------ | ------------ | ----------- |
| 1st | Insertion Sort, Cocktail Sort, Gnome Sort, Exchange Sort, Selection Sort, Merge Insertion Sort, Shell Sort, Bubble Sort, Odd-Even Sort, Spaghetti Sort, Tim Sort, Franceschini's Method, Comb Sort, Cycle Sort, Slowsort, Tree Sort, Heap Sort, Merge Sort In-Place, Strand Sort, Intro Sort, Library Sort, Quick Sort, Burst Sort, Hyper Quick, Pancake Sort, Patience Sort, I Can't Believe It Can Sort, Stooge Sort, Bucket Sort, Polyphase Merge Sort, Spreadsort, Merge Sort, Cubesort, Smooth Sort, MSD Radix Sort In-Place, MSD Radix Sort, Flash Sort, Replacement Selection Sort, Tournament Sort, Sorting Network, Block Sort, Sample Sort, Radix Sort, LSD Radix Sort, Postman Sort, Bogo Sort, Bitonic Sort Parallel | less than a ms | less than a ms |
| 48th | Counting Sort | 127ms | 130ms |
| 49th | Bead Sort | 543ms | 535ms |
| 50th | Pigeonhole Sort | 980ms | 1s 6ms |
| 51st | Sleep Sort | 1s 324ms | 1s 373ms |

### Array Size: 7

| Rank | Algorithm(s) | Average Time | Median Time |
| ---- | ------------ | ------------ | ----------- |
| 1st | Insertion Sort, Merge Insertion Sort, Exchange Sort, Selection Sort, Shell Sort, Cocktail Sort, Gnome Sort, Spaghetti Sort, Bubble Sort, Odd-Even Sort, Tim Sort, Franceschini's Method, Comb Sort, Cycle Sort, Tree Sort, Heap Sort, Intro Sort, Strand Sort, Library Sort, Merge Sort In-Place, Burst Sort, Patience Sort, Pancake Sort, Quick Sort, Spreadsort, Cubesort, Bucket Sort, I Can't Believe It Can Sort, Hyper Quick, Slowsort, Polyphase Merge Sort, Merge Sort, Flash Sort, MSD Radix Sort In-Place, Smooth Sort, MSD Radix Sort, Replacement Selection Sort, Stooge Sort, Sorting Network, Sample Sort, Tournament Sort, Block Sort, Radix Sort, LSD Radix Sort, Postman Sort, Bitonic Sort Parallel | less than a ms | less than a ms |
| 47th | Bogo Sort | 15ms | 9ms |
| 48th | Counting Sort | 138ms | 141ms |
| 49th | Bead Sort | 790ms | 801ms |
| 50th | Pigeonhole Sort | 1s 80ms | 1s 106ms |
| 51st | Sleep Sort | 1s 495ms | 1s 540ms |

### Array Size: 9

| Rank | Algorithm(s) | Average Time | Median Time |
| ---- | ------------ | ------------ | ----------- |
| 1st | Insertion Sort, Merge Insertion Sort, Spaghetti Sort, Selection Sort, Exchange Sort, Shell Sort, Tim Sort, Cocktail Sort, Odd-Even Sort, Franceschini's Method, Comb Sort, Gnome Sort, Tree Sort, Bubble Sort, Cycle Sort, Intro Sort, Heap Sort, Library Sort, Strand Sort, Merge Sort In-Place, Burst Sort, Patience Sort, Spreadsort, Hyper Quick, Quick Sort, Pancake Sort, Bucket Sort, Polyphase Merge Sort, I Can't Believe It Can Sort, Flash Sort, Merge Sort, Replacement Selection Sort, MSD Radix Sort In-Place, Cubesort, MSD Radix Sort, Smooth Sort, Stooge Sort, Slowsort, Block Sort, Sample Sort, Tournament Sort, Radix Sort, Sorting Network, LSD Radix Sort, Postman Sort, Bitonic Sort Parallel | less than a ms | less than a ms |
| 47th | Counting Sort | 156ms | 158ms |
| 48th | Bead Sort | 1s 96ms | 1s 101ms |
| 49th | Pigeonhole Sort | 1s 208ms | 1s 242ms |
| 50th | Bogo Sort | 1s 275ms | 880ms |
| 51st | Sleep Sort | 1s 605ms | 1s 636ms |

### Array Size: 12

| Rank | Algorithm(s) | Average Time | Median Time |
| ---- | ------------ | ------------ | ----------- |
| 1st | Insertion Sort, Merge Insertion Sort, Selection Sort, Spaghetti Sort, Tim Sort, Shell Sort, Comb Sort, Bubble Sort, Exchange Sort, Cocktail Sort, Franceschini's Method, Odd-Even Sort, Tree Sort, Polyphase Merge Sort, Intro Sort, Gnome Sort, Strand Sort, Patience Sort, Burst Sort, Bucket Sort, Library Sort, Heap Sort, Spreadsort, Merge Sort In-Place, Cubesort, Cycle Sort, Quick Sort, Replacement Selection Sort, Hyper Quick, Flash Sort, I Can't Believe It Can Sort, Pancake Sort, Merge Sort, MSD Radix Sort, MSD Radix Sort In-Place, Smooth Sort, Block Sort, Sample Sort, Radix Sort, Tournament Sort, Sorting Network, Postman Sort, LSD Radix Sort, Slowsort, Stooge Sort, Bitonic Sort Parallel | less than a ms | less than a ms |
| 47th | Counting Sort | 146ms | 148ms |
| 48th | Pigeonhole Sort | 435ms | 432ms |
| 49th | Bead Sort | 1s 547ms | 1s 560ms |
| 50th | Sleep Sort | 1s 681ms | 1s 720ms |
| 51st | Bogo Sort | 29min 10s 132ms | 20min 26s 932ms |

**Note:** The following algorithm were removed for this array size due to performance issues: Bogo Sort (at size 12)

### Array Size: 17

| Rank | Algorithm(s) | Average Time | Median Time |
| ---- | ------------ | ------------ | ----------- |
| 1st | Spaghetti Sort, Insertion Sort, Tim Sort, Shell Sort, Selection Sort, Merge Insertion Sort, Exchange Sort, Comb Sort, Franceschini's Method, Intro Sort, Tree Sort, Cocktail Sort, Odd-Even Sort, Patience Sort, Cubesort, Spreadsort, Bucket Sort, Library Sort, Replacement Selection Sort, Strand Sort, Burst Sort, Heap Sort, Gnome Sort, Flash Sort, Merge Sort In-Place, Polyphase Merge Sort, Bubble Sort, Cycle Sort, Hyper Quick, Quick Sort, I Can't Believe It Can Sort, Pancake Sort, Merge Sort, MSD Radix Sort In-Place, MSD Radix Sort, Smooth Sort, Sample Sort, Block Sort, Radix Sort, LSD Radix Sort, Tournament Sort, Postman Sort, Sorting Network, Stooge Sort, Slowsort, Bitonic Sort Parallel | less than a ms | less than a ms |
| 47th | Counting Sort | 143ms | 141ms |
| 48th | Pigeonhole Sort | 1s 246ms | 1s 254ms |
| 49th | Sleep Sort | 1s 774ms | 1s 812ms |
| 50th | Bead Sort | 2s 30ms | 2s 27ms |

### Array Size: 25

| Rank | Algorithm(s) | Average Time | Median Time |
| ---- | ------------ | ------------ | ----------- |
| 1st | Spaghetti Sort, Insertion Sort, Cubesort, Merge Insertion Sort, Tim Sort, Shell Sort, Selection Sort, Franceschini's Method, Replacement Selection Sort, Intro Sort, Comb Sort, Patience Sort, Tree Sort, Spreadsort, Bucket Sort, Flash Sort, Polyphase Merge Sort, Burst Sort, Exchange Sort, Library Sort, Strand Sort, Heap Sort, Merge Sort In-Place, Odd-Even Sort, Hyper Quick, Quick Sort, Cocktail Sort, Bubble Sort, I Can't Believe It Can Sort, MSD Radix Sort, MSD Radix Sort In-Place, Gnome Sort, Merge Sort, Cycle Sort, Block Sort, Pancake Sort, Sample Sort, Smooth Sort, Radix Sort, LSD Radix Sort, Tournament Sort, Postman Sort, Sorting Network, Stooge Sort, Bitonic Sort Parallel, Slowsort | less than a ms | less than a ms |
| 47th | Counting Sort | 150ms | 147ms |
| 48th | Pigeonhole Sort | 1s 301ms | 1s 309ms |
| 49th | Sleep Sort | 1s 854ms | 1s 871ms |
| 50th | Bead Sort | 3s 89ms | 3s 86ms |

### Array Size: 30

| Rank | Algorithm(s) | Average Time | Median Time |
| ---- | ------------ | ------------ | ----------- |
| 1st | Spaghetti Sort, Shell Sort, Merge Insertion Sort, Insertion Sort, Franceschini's Method, Tim Sort, Intro Sort, Patience Sort, Spreadsort, Comb Sort, Tree Sort, Selection Sort, Flash Sort, Polyphase Merge Sort, Cubesort, Replacement Selection Sort, Burst Sort, Bucket Sort, Strand Sort, Exchange Sort, Library Sort, Merge Sort In-Place, Heap Sort, Hyper Quick, Quick Sort, Odd-Even Sort, MSD Radix Sort, I Can't Believe It Can Sort, MSD Radix Sort In-Place, Merge Sort, Cocktail Sort, Block Sort, Bubble Sort, Gnome Sort, Pancake Sort, Cycle Sort, Sample Sort, LSD Radix Sort, Smooth Sort, Sorting Network, Radix Sort, Tournament Sort, Postman Sort, Bitonic Sort Parallel, Slowsort, Stooge Sort | less than a ms | less than a ms |
| 47th | Counting Sort | 151ms | 150ms |
| 48th | Pigeonhole Sort | 1s 331ms | 1s 334ms |
| 49th | Sleep Sort | 1s 877ms | 1s 893ms |
| 50th | Bead Sort | 3s 730ms | 3s 747ms |

### Array Size: 41

| Rank | Algorithm(s) | Average Time | Median Time |
| ---- | ------------ | ------------ | ----------- |
| 1st | Spaghetti Sort, Shell Sort, Cubesort, Replacement Selection Sort, Intro Sort, Merge Insertion Sort, Bucket Sort, Flash Sort, Patience Sort, Burst Sort, Spreadsort, Franceschini's Method, Comb Sort, Tree Sort, Polyphase Merge Sort, Tim Sort, Insertion Sort, Strand Sort, Library Sort, Merge Sort In-Place, Selection Sort, Hyper Quick, MSD Radix Sort, Exchange Sort, MSD Radix Sort In-Place, Heap Sort, I Can't Believe It Can Sort, Quick Sort, Merge Sort, Odd-Even Sort, Block Sort, Cocktail Sort, Sample Sort, Pancake Sort, Radix Sort, Bubble Sort, LSD Radix Sort, Gnome Sort, Cycle Sort, Postman Sort, Smooth Sort, Tournament Sort, Sorting Network, Bitonic Sort Parallel | less than a ms | less than a ms |
| 45th | Stooge Sort | 1ms | 1ms |
| 46th | Slowsort | 4ms | 4ms |
| 47th | Counting Sort | 154ms | 153ms |
| 48th | Pigeonhole Sort | 1s 358ms | 1s 365ms |
| 49th | Sleep Sort | 1s 907ms | 1s 918ms |
| 50th | Bead Sort | 5s 156ms | 5s 138ms |

### Array Size: 55

| Rank | Algorithm(s) | Average Time | Median Time |
| ---- | ------------ | ------------ | ----------- |
| 1st | Replacement Selection Sort, Cubesort, Spaghetti Sort, Shell Sort, Spreadsort, Flash Sort, Merge Insertion Sort, Intro Sort, Patience Sort, Polyphase Merge Sort, Burst Sort, Franceschini's Method, Bucket Sort, Tim Sort, Tree Sort, Comb Sort, Strand Sort, Insertion Sort, Hyper Quick, Merge Sort In-Place, Library Sort, Selection Sort, MSD Radix Sort, Heap Sort, MSD Radix Sort In-Place, Quick Sort, I Can't Believe It Can Sort, Sample Sort, Merge Sort, Block Sort, Exchange Sort, LSD Radix Sort, Radix Sort, Odd-Even Sort, Pancake Sort, Cocktail Sort, Postman Sort, Bubble Sort, Gnome Sort, Cycle Sort, Sorting Network, Tournament Sort, Smooth Sort, Bitonic Sort Parallel | less than a ms | less than a ms |
| 45th | Stooge Sort | 4ms | 3ms |
| 46th | Slowsort | 19ms | 18ms |
| 47th | Counting Sort | 155ms | 153ms |
| 48th | Pigeonhole Sort | 1s 385ms | 1s 382ms |
| 49th | Sleep Sort | 1s 941ms | 1s 950ms |
| 50th | Bead Sort | 6s 997ms | 6s 987ms |

### Array Size: 75

| Rank | Algorithm(s) | Average Time | Median Time |
| ---- | ------------ | ------------ | ----------- |
| 1st | Replacement Selection Sort, Flash Sort, Cubesort, Spreadsort, Bucket Sort, Intro Sort, Shell Sort, Patience Sort, Spaghetti Sort, Merge Insertion Sort, Polyphase Merge Sort, Burst Sort, Franceschini's Method, Tree Sort, Tim Sort, Comb Sort, Hyper Quick, MSD Radix Sort, Merge Sort In-Place, MSD Radix Sort In-Place, Strand Sort, Heap Sort, Library Sort, I Can't Believe It Can Sort, Insertion Sort, Quick Sort, Merge Sort, Selection Sort, Sample Sort, Block Sort, LSD Radix Sort, Radix Sort, Exchange Sort, Postman Sort, Odd-Even Sort, Pancake Sort, Cocktail Sort, Bubble Sort, Gnome Sort, Cycle Sort, Tournament Sort, Sorting Network, Smooth Sort, Bitonic Sort Parallel | less than a ms | less than a ms |
| 45th | Stooge Sort | 11ms | 10ms |
| 46th | Slowsort | 103ms | 100ms |
| 47th | Counting Sort | 155ms | 154ms |
| 48th | Pigeonhole Sort | 1s 391ms | 1s 387ms |
| 49th | Sleep Sort | 1s 956ms | 1s 966ms |
| 50th | Bead Sort | 9s 638ms | 9s 638ms |

### Array Size: 100

| Rank | Algorithm(s) | Average Time | Median Time |
| ---- | ------------ | ------------ | ----------- |
| 1st | Replacement Selection Sort, Cubesort, Flash Sort, Spreadsort, Intro Sort, Bucket Sort, Burst Sort, Patience Sort, Shell Sort, Merge Insertion Sort, Polyphase Merge Sort, Franceschini's Method, Tree Sort, Spaghetti Sort, Comb Sort, Tim Sort, MSD Radix Sort, Hyper Quick, MSD Radix Sort In-Place, Merge Sort In-Place, Quick Sort, Heap Sort, I Can't Believe It Can Sort, Strand Sort, Block Sort, Merge Sort, Library Sort, LSD Radix Sort, Radix Sort, Sample Sort, Insertion Sort, Selection Sort, Postman Sort, Exchange Sort, Odd-Even Sort, Pancake Sort, Cocktail Sort, Bubble Sort, Tournament Sort, Gnome Sort, Sorting Network, Cycle Sort, Smooth Sort, Bitonic Sort Parallel | less than a ms | less than a ms |
| 45th | Stooge Sort | 34ms | 33ms |
| 46th | Counting Sort | 157ms | 155ms |
| 47th | Slowsort | 499ms | 499ms |
| 48th | Pigeonhole Sort | 1s 411ms | 1s 409ms |
| 49th | Sleep Sort | 1s 970ms | 1s 976ms |
| 50th | Bead Sort | 13s 318ms | 13s 9ms |

### Array Size: 136

| Rank | Algorithm(s) | Average Time | Median Time |
| ---- | ------------ | ------------ | ----------- |
| 1st | Replacement Selection Sort, Cubesort, Flash Sort, Burst Sort, Bucket Sort, Intro Sort, Spreadsort, Patience Sort, Polyphase Merge Sort, Shell Sort, Merge Insertion Sort, Franceschini's Method, Tree Sort, Tim Sort, Comb Sort, MSD Radix Sort, Hyper Quick, MSD Radix Sort In-Place, Merge Sort In-Place, Heap Sort, I Can't Believe It Can Sort, Spaghetti Sort, Quick Sort, Merge Sort, LSD Radix Sort, Strand Sort, Block Sort, Sample Sort, Radix Sort, Library Sort, Postman Sort, Insertion Sort, Selection Sort, Exchange Sort, Pancake Sort, Odd-Even Sort, Bubble Sort, Cocktail Sort, Tournament Sort, Gnome Sort, Cycle Sort, Sorting Network, Smooth Sort, Bitonic Sort Parallel | less than a ms | less than a ms |
| 45th | Stooge Sort | 34ms | 32ms |
| 46th | Counting Sort | 158ms | 154ms |
| 47th | Pigeonhole Sort | 1s 424ms | 1s 423ms |
| 48th | Sleep Sort | 1s 983ms | 1s 988ms |
| 49th | Slowsort | 2s 995ms | 2s 997ms |
| 50th | Bead Sort | 17s 835ms | 17s 774ms |

