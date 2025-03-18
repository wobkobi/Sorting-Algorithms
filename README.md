# Sorting Algorithms Benchmark Results

## Overall Top 20 Algorithms (by average time across sizes)

| Rank | Algorithms | Overall Average Time |
| ---- | ---------- | -------------------- |
| 1st | [Cubesort](results/algorithms/Cubesort.md) | 855us |
| 2nd | [Replacement Selection Sort](results/algorithms/Replacement_Selection_Sort.md) | 1ms 11us |
| 3rd | [Burst Sort](results/algorithms/Burst_Sort.md) | 1ms 511us |
| 4th | [Bucket Sort](results/algorithms/Bucket_Sort.md) | 1ms 721us |
| 5th | [Flash Sort](results/algorithms/Flash_Sort.md) | 1ms 777us |
| 6th | [Spreadsort](results/algorithms/Spreadsort.md) | 2ms 224us |
| 7th | [Polyphase Merge Sort](results/algorithms/Polyphase_Merge_Sort.md) | 2ms 515us |
| 8th | [MSD Radix Sort](results/algorithms/MSD_Radix_Sort.md) | 3ms 508us |
| 9th | [MSD Radix Sort In-Place](results/algorithms/MSD_Radix_Sort_In-Place.md) | 3ms 801us |
| 10th | [Intro Sort](results/algorithms/Intro_Sort.md) | 3ms 942us |
| 11th | [Postman Sort](results/algorithms/Postman_Sort.md) | 4ms 275us |
| 12th | [Radix Sort](results/algorithms/Radix_Sort.md) | 4ms 353us |
| 13th | [LSD Radix Sort](results/algorithms/LSD_Radix_Sort.md) | 4ms 363us |
| 14th | [Merge Insertion Sort](results/algorithms/Merge_Insertion_Sort.md) | 4ms 619us |
| 15th | [Quick Sort](results/algorithms/Quick_Sort.md) | 5ms 130us |
| 16th | [Hyper Quick](results/algorithms/Hyper_Quick.md) | 5ms 268us |
| 17th | [Tree Sort](results/algorithms/Tree_Sort.md) | 5ms 576us |
| 18th | [Franceschini's Method](results/algorithms/Franceschini's_Method.md) | 5ms 893us |
| 19th | [Merge Sort](results/algorithms/Merge_Sort.md) | 6ms 486us |
| 20th | [I Can't Believe It Can Sort](results/algorithms/I_Can't_Believe_It_Can_Sort.md) | 6ms 613us |

## Skipped Algorithms

| Algorithm | Skipped At Size |
| --------- | --------------- |
| Bogo Sort | 12 |
| Slowsort | 333 |
| Bead Sort | 2500 |
| Stooge Sort | 5000 |
| Smooth Sort | 25000 |

## Detailed Benchmark Results

This benchmark report compares various sorting algorithms based on their performance across different array sizes. Each algorithm's performance is evaluated by its average and median runtimes, as well as the variance in its runtime measurements. A low variance (typically below 10%) indicates consistent performance, whereas a high variance (often above 50%) indicates that the algorithm's performance is less predictable. Algorithms that do not meet performance criteria at certain sizes are noted accordingly.

### Table of Contents

- [Array Size: 5](#array-size-5)
- [Array Size: 7](#array-size-7)
- [Array Size: 9](#array-size-9)
- [Array Size: 12](#array-size-12)
- [Array Size: 17](#array-size-17)
- [Array Size: 25](#array-size-25)
- [Array Size: 30](#array-size-30)
- [Array Size: 41](#array-size-41)
- [Array Size: 55](#array-size-55)
- [Array Size: 75](#array-size-75)
- [Array Size: 100](#array-size-100)
- [Array Size: 136](#array-size-136)
- [Array Size: 183](#array-size-183)
- [Array Size: 250](#array-size-250)
- [Array Size: 333](#array-size-333)
- [Array Size: 500](#array-size-500)
- [Array Size: 750](#array-size-750)
- [Array Size: 1000](#array-size-1000)
- [Array Size: 2500](#array-size-2500)
- [Array Size: 5000](#array-size-5000)
- [Array Size: 7500](#array-size-7500)
- [Array Size: 10,000](#array-size-10000)
- [Array Size: 25,000](#array-size-25000)

### Array Size: 5

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Insertion Sort, Exchange Sort, Merge Insertion Sort, Gnome Sort, Selection Sort, Cocktail Sort, Bubble Sort, Shell Sort, Odd-Even Sort, Spaghetti Sort, Comb Sort, Cycle Sort, Franceschini's Method, Tim Sort, Slowsort, Tree Sort, Heap Sort, Merge Sort In-Place, Intro Sort, Quick Sort, Library Sort, Strand Sort, Burst Sort, Pancake Sort, Patience Sort, I Can't Believe It Can Sort, Hyper Quick, Polyphase Merge Sort, Stooge Sort, Bucket Sort, Merge Sort, Spreadsort, Cubesort, MSD Radix Sort In-Place, MSD Radix Sort, Flash Sort, Smooth Sort, Replacement Selection Sort, Sorting Network, Tournament Sort, Sample Sort, Block Sort, Radix Sort, LSD Radix Sort, Postman Sort, Bogo Sort, Bitonic Sort Parallel | less than a ms | less than a ms |  |
| 48th | Counting Sort | 118ms | 119ms | 250% |
| 49th | Bead Sort | 494ms | 487ms | 210% |
| 50th | Pigeonhole Sort | 740ms | 657ms | 214% |
| 51st | Sleep Sort | 1s 328ms | 1s 373ms | 128% |

### Array Size: 7

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Insertion Sort, Merge Insertion Sort, Cocktail Sort, Exchange Sort, Gnome Sort, Shell Sort, Bubble Sort, Selection Sort, Spaghetti Sort, Odd-Even Sort, Franceschini's Method, Tim Sort, Comb Sort, Cycle Sort, Tree Sort, Heap Sort, Patience Sort, Burst Sort, Merge Sort In-Place, Intro Sort, Library Sort, Strand Sort, Bucket Sort, Pancake Sort, Hyper Quick, I Can't Believe It Can Sort, Cubesort, Quick Sort, Polyphase Merge Sort, Spreadsort, Merge Sort, Flash Sort, Slowsort, MSD Radix Sort, MSD Radix Sort In-Place, Smooth Sort, Replacement Selection Sort, Stooge Sort, Sorting Network, Tournament Sort, Block Sort, Sample Sort, Radix Sort, LSD Radix Sort, Postman Sort, Bitonic Sort Parallel | less than a ms | less than a ms |  |
| 47th | Bogo Sort | 14ms | 9ms | 604% |
| 48th | Counting Sort | 143ms | 145ms | 173% |
| 49th | Bead Sort | 784ms | 791ms | 122% |
| 50th | Pigeonhole Sort | 909ms | 887ms | 164% |
| 51st | Sleep Sort | 1s 493ms | 1s 546ms | 103% |

### Array Size: 9

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Insertion Sort, Merge Insertion Sort, Selection Sort, Exchange Sort, Shell Sort, Odd-Even Sort, Cocktail Sort, Tim Sort, Gnome Sort, Bubble Sort, Franceschini's Method, Spaghetti Sort, Comb Sort, Intro Sort, Tree Sort, Cycle Sort, Library Sort, Heap Sort, Merge Sort In-Place, Polyphase Merge Sort, Patience Sort, Burst Sort, Strand Sort, Hyper Quick, Pancake Sort, I Can't Believe It Can Sort, Quick Sort, Bucket Sort, Flash Sort, Replacement Selection Sort, Merge Sort, Cubesort, Spreadsort, MSD Radix Sort In-Place, MSD Radix Sort, Smooth Sort, Slowsort, Stooge Sort, Block Sort, Sample Sort, Radix Sort, Tournament Sort, LSD Radix Sort, Postman Sort, Sorting Network, Bitonic Sort Parallel | less than a ms | less than a ms |  |
| 47th | Counting Sort | 172ms | 172ms | 125% |
| 48th | Pigeonhole Sort | 1s 17ms | 983ms | 130% |
| 49th | Bead Sort | 1s 223ms | 1s 210ms | 143% |
| 50th | Bogo Sort | 1s 479ms | 994ms | 923% |
| 51st | Sleep Sort | 1s 599ms | 1s 639ms | 96% |

### Array Size: 12

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Insertion Sort, Merge Insertion Sort, Spaghetti Sort, Selection Sort, Tim Sort, Shell Sort, Exchange Sort, Comb Sort, Bubble Sort, Cocktail Sort, Franceschini's Method, Odd-Even Sort, Polyphase Merge Sort, Tree Sort, Intro Sort, Gnome Sort, Burst Sort, Patience Sort, Bucket Sort, Library Sort, Strand Sort, Heap Sort, Spreadsort, Merge Sort In-Place, Replacement Selection Sort, Cycle Sort, Quick Sort, Cubesort, Hyper Quick, Flash Sort, I Can't Believe It Can Sort, Pancake Sort, Merge Sort, MSD Radix Sort, MSD Radix Sort In-Place, Smooth Sort, Sample Sort, Block Sort, Radix Sort, Tournament Sort, Sorting Network, Postman Sort, LSD Radix Sort, Slowsort, Stooge Sort, Bitonic Sort Parallel | less than a ms | less than a ms |  |
| 47th | Counting Sort | 176ms | 172ms | 118% |
| 48th | Pigeonhole Sort | 506ms | 488ms | 187% |
| 49th | Sleep Sort | 1s 684ms | 1s 724ms | 62% |
| 50th | Bead Sort | 1s 823ms | 1s 761ms | 120% |
| 51st | Bogo Sort | 32min 50s 58ms | 23min 1s 595ms | 608% |

**Note:** The following algorithm were removed for this array size due to performance issues: Bogo Sort (at size 12)

### Array Size: 17

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Spaghetti Sort, Insertion Sort, Tim Sort, Shell Sort, Selection Sort, Merge Insertion Sort, Exchange Sort, Franceschini's Method, Intro Sort, Tree Sort, Comb Sort, Odd-Even Sort, Patience Sort, Spreadsort, Library Sort, Strand Sort, Cubesort, Gnome Sort, Heap Sort, Flash Sort, Cocktail Sort, Merge Sort In-Place, Burst Sort, Bucket Sort, Cycle Sort, Hyper Quick, Bubble Sort, Polyphase Merge Sort, I Can't Believe It Can Sort, Replacement Selection Sort, Pancake Sort, Merge Sort, MSD Radix Sort In-Place, MSD Radix Sort, Quick Sort, Smooth Sort, Sample Sort, Block Sort, Radix Sort, LSD Radix Sort, Tournament Sort, Postman Sort, Sorting Network, Stooge Sort, Slowsort, Bitonic Sort Parallel | less than a ms | less than a ms |  |
| 47th | Counting Sort | 171ms | 172ms | 92% |
| 48th | Sleep Sort | 1s 779ms | 1s 812ms | 53% |
| 49th | Pigeonhole Sort | 1s 820ms | 1s 587ms | 120% |
| 50th | Bead Sort | 2s 406ms | 2s 351ms | 111% |

### Array Size: 25

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Spaghetti Sort, Insertion Sort, Shell Sort, Merge Insertion Sort, Tim Sort, Cubesort, Selection Sort, Franceschini's Method, Replacement Selection Sort, Intro Sort, Patience Sort, Tree Sort, Spreadsort, Comb Sort, Flash Sort, Exchange Sort, Bucket Sort, Library Sort, Burst Sort, Strand Sort, Heap Sort, Merge Sort In-Place, Polyphase Merge Sort, Odd-Even Sort, Hyper Quick, Quick Sort, I Can't Believe It Can Sort, MSD Radix Sort, Gnome Sort, MSD Radix Sort In-Place, Cocktail Sort, Merge Sort, Cycle Sort, Bubble Sort, Pancake Sort, Sample Sort, Block Sort, Smooth Sort, Radix Sort, LSD Radix Sort, Tournament Sort, Sorting Network, Postman Sort, Stooge Sort, Bitonic Sort Parallel, Slowsort | less than a ms | less than a ms |  |
| 47th | Counting Sort | 179ms | 183ms | 84% |
| 48th | Sleep Sort | 1s 849ms | 1s 871ms | 33% |
| 49th | Pigeonhole Sort | 1s 902ms | 1s 583ms | 128% |
| 50th | Bead Sort | 3s 672ms | 3s 577ms | 94% |

### Array Size: 30

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Spaghetti Sort, Shell Sort, Merge Insertion Sort, Insertion Sort, Franceschini's Method, Tim Sort, Intro Sort, Spreadsort, Patience Sort, Tree Sort, Flash Sort, Selection Sort, Comb Sort, Replacement Selection Sort, Cubesort, Burst Sort, Bucket Sort, Strand Sort, Polyphase Merge Sort, Library Sort, Exchange Sort, Merge Sort In-Place, Heap Sort, Hyper Quick, Odd-Even Sort, I Can't Believe It Can Sort, MSD Radix Sort, MSD Radix Sort In-Place, Quick Sort, Merge Sort, Gnome Sort, Cocktail Sort, Pancake Sort, Bubble Sort, Sample Sort, Cycle Sort, Block Sort, LSD Radix Sort, Smooth Sort, Sorting Network, Radix Sort, Tournament Sort, Postman Sort, Bitonic Sort Parallel, Slowsort, Stooge Sort | less than a ms | less than a ms |  |
| 47th | Counting Sort | 181ms | 184ms | 83% |
| 48th | Sleep Sort | 1s 878ms | 1s 896ms | 29% |
| 49th | Pigeonhole Sort | 1s 937ms | 1s 585ms | 114% |
| 50th | Bead Sort | 4s 447ms | 4s 291ms | 79% |

### Array Size: 41

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Spaghetti Sort, Shell Sort, Intro Sort, Merge Insertion Sort, Cubesort, Flash Sort, Spreadsort, Replacement Selection Sort, Patience Sort, Franceschini's Method, Tree Sort, Tim Sort, Insertion Sort, Bucket Sort, Burst Sort, Comb Sort, Strand Sort, Library Sort, Polyphase Merge Sort, Merge Sort In-Place, Selection Sort, Hyper Quick, Heap Sort, MSD Radix Sort, Exchange Sort, MSD Radix Sort In-Place, I Can't Believe It Can Sort, Merge Sort, Quick Sort, Odd-Even Sort, Block Sort, Sample Sort, Pancake Sort, LSD Radix Sort, Cocktail Sort, Gnome Sort, Radix Sort, Cycle Sort, Bubble Sort, Smooth Sort, Postman Sort, Tournament Sort, Sorting Network, Bitonic Sort Parallel, Stooge Sort | less than a ms | less than a ms |  |
| 46th | Slowsort | 4ms | 4ms | 72% |
| 47th | Counting Sort | 183ms | 188ms | 86% |
| 48th | Sleep Sort | 1s 909ms | 1s 921ms | 20% |
| 49th | Pigeonhole Sort | 1s 981ms | 1s 634ms | 114% |
| 50th | Bead Sort | 6s 181ms | 6s 6ms | 72% |

### Array Size: 55

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Cubesort, Spaghetti Sort, Replacement Selection Sort, Spreadsort, Flash Sort, Shell Sort, Merge Insertion Sort, Intro Sort, Patience Sort, Franceschini's Method, Tim Sort, Tree Sort, Burst Sort, Polyphase Merge Sort, Bucket Sort, Comb Sort, Insertion Sort, Strand Sort, Hyper Quick, Merge Sort In-Place, Library Sort, MSD Radix Sort, Heap Sort, MSD Radix Sort In-Place, Selection Sort, I Can't Believe It Can Sort, Merge Sort, Quick Sort, Sample Sort, Exchange Sort, Block Sort, LSD Radix Sort, Odd-Even Sort, Pancake Sort, Radix Sort, Cocktail Sort, Gnome Sort, Postman Sort, Cycle Sort, Bubble Sort, Sorting Network, Tournament Sort, Smooth Sort, Bitonic Sort Parallel | less than a ms | less than a ms |  |
| 45th | Stooge Sort | 4ms | 5ms | 113% |
| 46th | Slowsort | 20ms | 18ms | 75% |
| 47th | Counting Sort | 185ms | 190ms | 71% |
| 48th | Sleep Sort | 1s 936ms | 1s 945ms | 16% |
| 49th | Pigeonhole Sort | 2s 7ms | 1s 609ms | 125% |
| 50th | Bead Sort | 8s 401ms | 8s 238ms | 74% |

### Array Size: 75

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Replacement Selection Sort, Flash Sort, Spreadsort, Cubesort, Intro Sort, Shell Sort, Patience Sort, Spaghetti Sort, Merge Insertion Sort, Bucket Sort, Burst Sort, Franceschini's Method, Tree Sort, Tim Sort, Polyphase Merge Sort, Comb Sort, Hyper Quick, MSD Radix Sort, Merge Sort In-Place, MSD Radix Sort In-Place, Heap Sort, Library Sort, Strand Sort, I Can't Believe It Can Sort, Insertion Sort, Merge Sort, Quick Sort, Selection Sort, Sample Sort, LSD Radix Sort, Block Sort, Radix Sort, Exchange Sort, Postman Sort, Odd-Even Sort, Pancake Sort, Cocktail Sort, Gnome Sort, Tournament Sort, Bubble Sort, Cycle Sort, Sorting Network, Smooth Sort, Bitonic Sort Parallel | less than a ms | less than a ms |  |
| 45th | Stooge Sort | 14ms | 15ms | 103% |
| 46th | Slowsort | 117ms | 116ms | 67% |
| 47th | Counting Sort | 186ms | 192ms | 66% |
| 48th | Sleep Sort | 1s 954ms | 1s 962ms | 12% |
| 49th | Pigeonhole Sort | 2s 30ms | 1s 654ms | 123% |
| 50th | Bead Sort | 11s 524ms | 11s 589ms | 67% |

### Array Size: 100

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Cubesort, Replacement Selection Sort, Flash Sort, Intro Sort, Spreadsort, Patience Sort, Merge Insertion Sort, Shell Sort, Burst Sort, Bucket Sort, Franceschini's Method, Tree Sort, Tim Sort, Polyphase Merge Sort, Comb Sort, Spaghetti Sort, MSD Radix Sort, Hyper Quick, MSD Radix Sort In-Place, Merge Sort In-Place, Heap Sort, I Can't Believe It Can Sort, Merge Sort, Library Sort, Strand Sort, Quick Sort, LSD Radix Sort, Block Sort, Insertion Sort, Sample Sort, Radix Sort, Selection Sort, Postman Sort, Exchange Sort, Odd-Even Sort, Pancake Sort, Tournament Sort, Cocktail Sort, Gnome Sort, Bubble Sort, Sorting Network, Cycle Sort, Smooth Sort, Bitonic Sort Parallel | less than a ms | less than a ms |  |
| 45th | Stooge Sort | 41ms | 44ms | 81% |
| 46th | Counting Sort | 188ms | 194ms | 83% |
| 47th | Slowsort | 581ms | 563ms | 55% |
| 48th | Sleep Sort | 1s 968ms | 1s 974ms | 9% |
| 49th | Pigeonhole Sort | 2s 48ms | 1s 652ms | 109% |
| 50th | Bead Sort | 15s 619ms | 16s 701ms | 103% |

### Array Size: 136

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Replacement Selection Sort, Cubesort, Flash Sort, Intro Sort, Burst Sort, Patience Sort, Bucket Sort, Spreadsort, Shell Sort, Merge Insertion Sort, Franceschini's Method, Tree Sort, Tim Sort, MSD Radix Sort, Polyphase Merge Sort, Hyper Quick, MSD Radix Sort In-Place, Comb Sort, Merge Sort In-Place, Heap Sort, I Can't Believe It Can Sort, Merge Sort, LSD Radix Sort, Spaghetti Sort, Strand Sort, Quick Sort, Sample Sort, Block Sort, Library Sort, Radix Sort, Postman Sort, Insertion Sort, Selection Sort, Exchange Sort, Pancake Sort, Odd-Even Sort, Cocktail Sort, Bubble Sort, Tournament Sort, Gnome Sort, Cycle Sort, Sorting Network, Smooth Sort, Bitonic Sort Parallel | less than a ms | less than a ms |  |
| 45th | Stooge Sort | 40ms | 41ms | 77% |
| 46th | Counting Sort | 189ms | 197ms | 73% |
| 47th | Sleep Sort | 1s 982ms | 1s 987ms | 8% |
| 48th | Pigeonhole Sort | 2s 79ms | 1s 668ms | 110% |
| 49th | Slowsort | 3s 494ms | 3s 197ms | 46% |
| 50th | Bead Sort | 21s 186ms | 21s 775ms | 59% |

### Array Size: 183

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Cubesort, Replacement Selection Sort, Flash Sort, Burst Sort, Bucket Sort, Intro Sort, Shell Sort, Spreadsort, Patience Sort, Merge Insertion Sort, Franceschini's Method, Polyphase Merge Sort, MSD Radix Sort, Tree Sort, Hyper Quick, MSD Radix Sort In-Place, Tim Sort, I Can't Believe It Can Sort, LSD Radix Sort, Comb Sort, Quick Sort, Merge Sort In-Place, Heap Sort, Merge Sort, Radix Sort, Block Sort, Sample Sort, Postman Sort, Spaghetti Sort, Strand Sort, Library Sort, Insertion Sort, Selection Sort, Exchange Sort, Pancake Sort, Odd-Even Sort, Sorting Network, Bubble Sort, Cocktail Sort, Tournament Sort, Bitonic Sort Parallel, Cycle Sort, Gnome Sort, Smooth Sort | less than a ms | less than a ms |  |
| 45th | Stooge Sort | 140ms | 140ms | 67% |
| 46th | Counting Sort | 243ms | 239ms | 90% |
| 47th | Sleep Sort | 1s 994ms | 1s 997ms | 6% |
| 48th | Pigeonhole Sort | 2s 661ms | 2s 711ms | 92% |
| 49th | Slowsort | 27s 469ms | 26s 848ms | 19% |
| 50th | Bead Sort | 29s 873ms | 32s 243ms | 82% |

### Array Size: 250

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Replacement Selection Sort, Cubesort, Burst Sort, Flash Sort, Bucket Sort, Shell Sort, Spreadsort, Polyphase Merge Sort, Intro Sort, Patience Sort, Merge Insertion Sort, Franceschini's Method, Comb Sort, Tree Sort, MSD Radix Sort In-Place, MSD Radix Sort, Hyper Quick, Tim Sort, Quick Sort, Radix Sort, I Can't Believe It Can Sort, LSD Radix Sort, Merge Sort, Merge Sort In-Place, Heap Sort, Postman Sort, Block Sort, Sample Sort, Strand Sort, Spaghetti Sort, Library Sort, Sorting Network, Selection Sort, Insertion Sort, Bitonic Sort Parallel, Exchange Sort, Cocktail Sort, Pancake Sort, Bubble Sort, Odd-Even Sort, Tournament Sort | less than a ms | less than a ms |  |
| 42nd | Cycle Sort, Gnome Sort, Smooth Sort | 4ms | 4ms |  |
| 45th | Counting Sort | 235ms | 237ms | 50% |
| 46th | Stooge Sort | 417ms | 419ms | 34% |
| 47th | Sleep Sort | 2s 8ms | 2s 9ms | 4% |
| 48th | Pigeonhole Sort | 2s 711ms | 2s 719ms | 91% |
| 49th | Bead Sort | 46s 971ms | 46s 857ms | 49% |
| 50th | Slowsort | 3min 52s 379ms | 3min 47s 804ms | 22% |

### Array Size: 333

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Replacement Selection Sort, Cubesort, Flash Sort, Burst Sort, Bucket Sort, Spreadsort, Polyphase Merge Sort, Intro Sort, Merge Insertion Sort, Patience Sort, Tree Sort, Shell Sort, MSD Radix Sort, MSD Radix Sort In-Place, Franceschini's Method, Comb Sort, Hyper Quick, Tim Sort, LSD Radix Sort, I Can't Believe It Can Sort, Merge Sort, Quick Sort, Block Sort, Heap Sort, Radix Sort, Merge Sort In-Place, Postman Sort, Strand Sort, Sample Sort, Spaghetti Sort, Library Sort | less than a ms | less than a ms |  |
| 32nd | Insertion Sort, Selection Sort, Sorting Network, Bitonic Sort Parallel, Exchange Sort, Pancake Sort, Cocktail Sort, Tournament Sort, Bubble Sort, Odd-Even Sort | 2ms | 3ms |  |
| 42nd | Gnome Sort, Cycle Sort, Smooth Sort | 7ms | 8ms |  |
| 45th | Counting Sort | 218ms | 240ms | 85% |
| 46th | Stooge Sort | 1s 116ms | 1s 143ms | 34% |
| 47th | Sleep Sort | 2s 22ms | 2s 22ms | 6% |
| 48th | Pigeonhole Sort | 2s 25ms | 1s 612ms | 127% |
| 49th | Bead Sort | 55s 301ms | 58s 284ms | 65% |
| 50th | Slowsort | 28min 1s 588ms | 28min 33s 583ms | 70% |

**Note:** The following algorithm were removed for this array size due to performance issues: Slowsort (at size 333)

### Array Size: 500

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Replacement Selection Sort, Cubesort, Bucket Sort, Burst Sort, Spreadsort, Flash Sort, Polyphase Merge Sort, Intro Sort, Merge Insertion Sort, Tree Sort, Patience Sort, MSD Radix Sort, Shell Sort, MSD Radix Sort In-Place, Tim Sort, Franceschini's Method, Comb Sort, Quick Sort, Hyper Quick, Postman Sort, LSD Radix Sort, Radix Sort, I Can't Believe It Can Sort, Merge Sort, Block Sort, Heap Sort, Merge Sort In-Place, Sample Sort, Strand Sort, Spaghetti Sort | less than a ms | less than a ms |  |
| 31st | Sorting Network, Library Sort, Bitonic Sort Parallel | 3ms | 3ms |  |
| 34th | Insertion Sort, Selection Sort | 6ms | 6ms |  |
| 36th | Pancake Sort, Tournament Sort, Exchange Sort | 9ms | 9ms |  |
| 39th | Cocktail Sort, Bubble Sort | 11ms | 11ms |  |
| 41st | Odd-Even Sort | 13ms | 13ms | 61% |
| 42nd | Gnome Sort | 17ms | 17ms | 73% |
| 43rd | Smooth Sort, Cycle Sort | 19ms | 18ms |  |
| 45th | Counting Sort | 210ms | 210ms | 49% |
| 46th | Pigeonhole Sort | 1s 409ms | 1s 419ms | 78% |
| 47th | Sleep Sort | 2s 57ms | 2s 58ms | 6% |
| 48th | Stooge Sort | 3s 106ms | 3s 99ms | 21% |
| 49th | Bead Sort | 1min 13s 457ms | 1min 15s 614ms | 34% |

### Array Size: 750

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Replacement Selection Sort, Cubesort, Spreadsort, Burst Sort, Flash Sort, Bucket Sort, Polyphase Merge Sort, Intro Sort, Merge Insertion Sort, Franceschini's Method, Patience Sort, Tree Sort, MSD Radix Sort, MSD Radix Sort In-Place, Hyper Quick, Shell Sort, Tim Sort, Quick Sort, LSD Radix Sort, Radix Sort, Comb Sort, I Can't Believe It Can Sort, Postman Sort, Merge Sort, Heap Sort, Block Sort, Sample Sort, Merge Sort In-Place, Strand Sort | less than a ms | less than a ms |  |
| 30th | Spaghetti Sort | 5ms | 6ms | 283% |
| 31st | Sorting Network, Library Sort | 9ms | 9ms |  |
| 33rd | Insertion Sort | 17ms | 18ms | 199% |
| 34th | Selection Sort | 18ms | 18ms | 263% |
| 35th | Tournament Sort, Pancake Sort, Exchange Sort | 24ms | 25ms |  |
| 38th | Cocktail Sort | 32ms | 34ms | 148% |
| 39th | Bubble Sort | 34ms | 36ms | 209% |
| 40th | Odd-Even Sort | 39ms | 39ms | 177% |
| 41st | Gnome Sort | 47ms | 50ms | 233% |
| 42nd | Cycle Sort | 50ms | 53ms | 145% |
| 43rd | Smooth Sort | 54ms | 51ms | 130% |
| 44th | Counting Sort | 246ms | 272ms | 85% |
| 45th | Bitonic Sort Parallel | 255ms | 218ms | 474% |
| 46th | Pigeonhole Sort | 2s 53ms | 1s 628ms | 236% |
| 47th | Sleep Sort | 2s 102ms | 2s 102ms | 5% |
| 48th | Stooge Sort | 10s 787ms | 11s 37ms | 71% |
| 49th | Bead Sort | 2min 2s 370ms | 1min 59s 429ms | 66% |

### Array Size: 1000

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Cubesort, Replacement Selection Sort, Burst Sort, Bucket Sort, Flash Sort, Polyphase Merge Sort, Spreadsort, Intro Sort, Merge Insertion Sort, MSD Radix Sort, MSD Radix Sort In-Place, Tree Sort, Patience Sort, Quick Sort, Hyper Quick, Franceschini's Method, Radix Sort, Postman Sort, LSD Radix Sort, Comb Sort, Shell Sort, I Can't Believe It Can Sort, Tim Sort, Merge Sort, Heap Sort, Block Sort, Sample Sort, Merge Sort In-Place | less than a ms | less than a ms |  |
| 29th | Strand Sort | 6ms | 6ms | 193% |
| 30th | Sorting Network | 10ms | 9ms | 520% |
| 31st | Spaghetti Sort | 11ms | 10ms | 427% |
| 32nd | Library Sort | 14ms | 13ms | 427% |
| 33rd | Insertion Sort | 28ms | 29ms | 159% |
| 34th | Selection Sort | 30ms | 31ms | 222% |
| 35th | Tournament Sort | 38ms | 38ms | 59% |
| 36th | Pancake Sort | 40ms | 42ms | 164% |
| 37th | Exchange Sort | 42ms | 43ms | 167% |
| 38th | Cocktail Sort | 53ms | 55ms | 95% |
| 39th | Bubble Sort | 56ms | 57ms | 122% |
| 40th | Odd-Even Sort | 61ms | 63ms | 137% |
| 41st | Gnome Sort | 77ms | 80ms | 105% |
| 42nd | Cycle Sort | 84ms | 87ms | 96% |
| 43rd | Smooth Sort | 120ms | 118ms | 91% |
| 44th | Bitonic Sort Parallel | 214ms | 199ms | 127% |
| 45th | Counting Sort | 231ms | 238ms | 96% |
| 46th | Pigeonhole Sort | 1s 412ms | 1s 349ms | 87% |
| 47th | Sleep Sort | 2s 163ms | 2s 162ms | 8% |
| 48th | Stooge Sort | 10s 648ms | 10s 635ms | 12% |
| 49th | Bead Sort | 2min 34s 661ms | 2min 26s 348ms | 64% |

### Array Size: 2500

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Cubesort, Replacement Selection Sort, Burst Sort, Bucket Sort, Flash Sort, Spreadsort, Polyphase Merge Sort | less than a ms | less than a ms |  |
| 8th | Intro Sort, MSD Radix Sort, MSD Radix Sort In-Place, Merge Insertion Sort, Hyper Quick, Postman Sort, Tree Sort, LSD Radix Sort, Radix Sort, Quick Sort, Franceschini's Method, Patience Sort, Comb Sort, I Can't Believe It Can Sort, Tim Sort, Shell Sort, Merge Sort, Heap Sort | 3ms | 3ms |  |
| 26th | Block Sort | 10ms | 8ms | 73% |
| 27th | Sample Sort, Merge Sort In-Place | 13ms | 11ms |  |
| 29th | Strand Sort | 20ms | 20ms | 118% |
| 30th | Sorting Network | 31ms | 29ms | 70% |
| 31st | Spaghetti Sort | 44ms | 42ms | 66% |
| 32nd | Library Sort | 63ms | 58ms | 224% |
| 33rd | Insertion Sort | 144ms | 142ms | 58% |
| 34th | Selection Sort | 146ms | 143ms | 64% |
| 35th | Bitonic Sort Parallel | 184ms | 183ms | 40% |
| 36th | Counting Sort | 190ms | 188ms | 56% |
| 37th | Tournament Sort | 192ms | 195ms | 56% |
| 38th | Pancake Sort | 207ms | 206ms | 47% |
| 39th | Exchange Sort | 221ms | 220ms | 41% |
| 40th | Cocktail Sort | 276ms | 274ms | 45% |
| 41st | Bubble Sort | 309ms | 306ms | 46% |
| 42nd | Odd-Even Sort | 316ms | 312ms | 90% |
| 43rd | Gnome Sort | 398ms | 395ms | 44% |
| 44th | Cycle Sort | 451ms | 451ms | 36% |
| 45th | Smooth Sort | 844ms | 842ms | 19% |
| 46th | Pigeonhole Sort | 1s 314ms | 1s 317ms | 58% |
| 47th | Sleep Sort | 2s 459ms | 2s 451ms | 14% |
| 48th | Stooge Sort | 3min 53s 890ms | 3min 47s 923ms | 33% |
| 49th | Bead Sort | 6min 36s 894ms | 6min 0s 978ms | 92% |

**Note:** The following algorithm were removed for this array size due to performance issues: Bead Sort (at size 2500)

### Array Size: 5000

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Cubesort, Replacement Selection Sort | 2ms | 2ms |  |
| 3rd | Burst Sort, Bucket Sort, Flash Sort, Spreadsort | 4ms | 4ms |  |
| 7th | Polyphase Merge Sort | 7ms | 6ms | 311% |
| 8th | Tree Sort | 8ms | 8ms | 84% |
| 9th | MSD Radix Sort, Intro Sort, MSD Radix Sort In-Place, Tim Sort | 10ms | 9ms |  |
| 13th | Postman Sort, LSD Radix Sort, Merge Insertion Sort, Radix Sort, Hyper Quick | 12ms | 12ms |  |
| 18th | Quick Sort, Franceschini's Method | 13ms | 13ms |  |
| 20th | I Can't Believe It Can Sort, Merge Sort, Comb Sort, Shell Sort | 16ms | 16ms |  |
| 24th | Patience Sort | 19ms | 19ms | 80% |
| 25th | Heap Sort | 21ms | 21ms | 73% |
| 26th | Block Sort | 45ms | 44ms | 93% |
| 27th | Sample Sort | 51ms | 51ms | 59% |
| 28th | Strand Sort | 55ms | 54ms | 73% |
| 29th | Merge Sort In-Place | 60ms | 61ms | 50% |
| 30th | Sorting Network | 103ms | 104ms | 32% |
| 31st | Spaghetti Sort | 258ms | 258ms | 45% |
| 32nd | Counting Sort | 287ms | 286ms | 32% |
| 33rd | Library Sort | 373ms | 342ms | 219% |
| 34th | Bitonic Sort Parallel | 577ms | 571ms | 97% |
| 35th | Tournament Sort | 712ms | 710ms | 33% |
| 36th | Selection Sort | 823ms | 823ms | 16% |
| 37th | Insertion Sort | 841ms | 839ms | 22% |
| 38th | Exchange Sort | 1s 202ms | 1s 201ms | 14% |
| 39th | Pancake Sort | 1s 228ms | 1s 228ms | 13% |
| 40th | Cocktail Sort | 1s 630ms | 1s 627ms | 17% |
| 41st | Bubble Sort | 1s 849ms | 1s 846ms | 14% |
| 42nd | Odd-Even Sort | 1s 880ms | 1s 881ms | 31% |
| 43rd | Gnome Sort | 2s 351ms | 2s 332ms | 37% |
| 44th | Cycle Sort | 2s 588ms | 2s 584ms | 18% |
| 45th | Pigeonhole Sort | 2s 745ms | 2s 724ms | 62% |
| 46th | Sleep Sort | 3s 420ms | 3s 430ms | 19% |
| 47th | Smooth Sort | 5s 928ms | 5s 926ms | 9% |
| 48th | Stooge Sort | 21min 12s 585ms | 15min 37s 135ms | 1914% |

**Note:** The following algorithm were removed for this array size due to performance issues: Stooge Sort (at size 5000)

### Array Size: 7500

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Cubesort, Replacement Selection Sort | 2ms | 2ms |  |
| 3rd | Burst Sort, Bucket Sort, Flash Sort, Spreadsort | 4ms | 4ms |  |
| 7th | Polyphase Merge Sort | 7ms | 6ms | 154% |
| 8th | MSD Radix Sort, MSD Radix Sort In-Place, Intro Sort, Postman Sort, LSD Radix Sort, Radix Sort, Merge Insertion Sort, Tree Sort, Hyper Quick, Quick Sort | 10ms | 9ms |  |
| 18th | Tim Sort, Franceschini's Method | 17ms | 16ms |  |
| 20th | I Can't Believe It Can Sort, Merge Sort | 19ms | 18ms |  |
| 22nd | Comb Sort, Shell Sort | 21ms | 20ms |  |
| 24th | Heap Sort, Patience Sort | 24ms | 23ms |  |
| 26th | Block Sort | 56ms | 55ms | 66% |
| 27th | Sample Sort | 68ms | 66ms | 64% |
| 28th | Sorting Network | 81ms | 80ms | 64% |
| 29th | Merge Sort In-Place | 88ms | 86ms | 65% |
| 30th | Strand Sort | 105ms | 103ms | 69% |
| 31st | Counting Sort | 217ms | 214ms | 54% |
| 32nd | Bitonic Sort Parallel | 298ms | 295ms | 49% |
| 33rd | Spaghetti Sort | 439ms | 438ms | 43% |
| 34th | Library Sort | 622ms | 567ms | 217% |
| 35th | Selection Sort | 1s 423ms | 1s 422ms | 25% |
| 36th | Insertion Sort | 1s 434ms | 1s 426ms | 32% |
| 37th | Pigeonhole Sort | 1s 455ms | 1s 443ms | 43% |
| 38th | Tournament Sort | 1s 599ms | 1s 596ms | 25% |
| 39th | Pancake Sort | 2s 141ms | 2s 136ms | 36% |
| 40th | Exchange Sort | 2s 144ms | 2s 144ms | 20% |
| 41st | Cocktail Sort | 2s 721ms | 2s 716ms | 27% |
| 42nd | Odd-Even Sort | 3s 160ms | 3s 118ms | 162% |
| 43rd | Bubble Sort | 3s 169ms | 3s 129ms | 30% |
| 44th | Gnome Sort | 3s 907ms | 3s 894ms | 35% |
| 45th | Sleep Sort | 4s 162ms | 4s 140ms | 10% |
| 46th | Cycle Sort | 4s 447ms | 4s 441ms | 20% |
| 47th | Smooth Sort | 16s 867ms | 16s 864ms | 8% |

### Array Size: 10,000

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Cubesort, Replacement Selection Sort | 3ms | 3ms |  |
| 3rd | Burst Sort, Bucket Sort, Flash Sort | 6ms | 5ms |  |
| 6th | Spreadsort | 8ms | 8ms | 118% |
| 7th | Polyphase Merge Sort | 10ms | 9ms | 87% |
| 8th | MSD Radix Sort | 14ms | 13ms | 84% |
| 9th | MSD Radix Sort In-Place, Intro Sort, Postman Sort, Radix Sort, LSD Radix Sort | 15ms | 14ms |  |
| 14th | Merge Insertion Sort, Hyper Quick, Quick Sort | 19ms | 19ms |  |
| 17th | Tree Sort | 22ms | 22ms | 130% |
| 18th | Franceschini's Method | 23ms | 23ms | 72% |
| 19th | I Can't Believe It Can Sort, Tim Sort, Merge Sort | 26ms | 25ms |  |
| 22nd | Comb Sort | 30ms | 29ms | 101% |
| 23rd | Shell Sort | 32ms | 31ms | 73% |
| 24th | Heap Sort | 34ms | 33ms | 63% |
| 25th | Patience Sort | 37ms | 36ms | 103% |
| 26th | Block Sort | 82ms | 81ms | 68% |
| 27th | Sample Sort | 104ms | 103ms | 61% |
| 28th | Merge Sort In-Place | 149ms | 147ms | 65% |
| 29th | Sorting Network, Strand Sort | 195ms | 192ms |  |
| 31st | Counting Sort | 217ms | 215ms | 49% |
| 32nd | Bitonic Sort Parallel | 385ms | 383ms | 59% |
| 33rd | Spaghetti Sort | 900ms | 884ms | 35% |
| 34th | Library Sort | 1s 107ms | 1s 19ms | 229% |
| 35th | Pigeonhole Sort | 1s 453ms | 1s 442ms | 54% |
| 36th | Insertion Sort | 2s 557ms | 2s 557ms | 18% |
| 37th | Selection Sort | 2s 575ms | 2s 571ms | 32% |
| 38th | Tournament Sort | 3s 384ms | 3s 371ms | 32% |
| 39th | Exchange Sort | 3s 868ms | 3s 868ms | 20% |
| 40th | Pancake Sort | 3s 915ms | 3s 905ms | 31% |
| 41st | Cocktail Sort | 4s 927ms | 4s 903ms | 21% |
| 42nd | Sleep Sort | 5s 9ms | 4s 997ms | 9% |
| 43rd | Bubble Sort | 5s 627ms | 5s 600ms | 42% |
| 44th | Odd-Even Sort | 5s 695ms | 5s 667ms | 42% |
| 45th | Gnome Sort | 7s 43ms | 7s 1ms | 38% |
| 46th | Cycle Sort | 8s 48ms | 8s 45ms | 14% |
| 47th | Smooth Sort | 39s 849ms | 39s 990ms | 18% |

### Array Size: 25,000

| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |
| ---- | ------------ | ------------ | ----------- | ------------ |
| 1st | Cubesort | 8ms | 8ms | 74% |
| 2nd | Replacement Selection Sort | 10ms | 9ms | 60% |
| 3rd | Burst Sort | 15ms | 14ms | 142% |
| 4th | Flash Sort, Bucket Sort | 18ms | 18ms |  |
| 6th | Spreadsort, Polyphase Merge Sort | 26ms | 25ms |  |
| 8th | MSD Radix Sort | 35ms | 35ms | 68% |
| 9th | MSD Radix Sort In-Place | 39ms | 38ms | 69% |
| 10th | Postman Sort, Intro Sort, Radix Sort | 42ms | 41ms |  |
| 13th | LSD Radix Sort | 44ms | 43ms | 69% |
| 14th | Merge Insertion Sort | 51ms | 49ms | 63% |
| 15th | Quick Sort | 55ms | 54ms | 59% |
| 16th | Hyper Quick | 62ms | 63ms | 69% |
| 17th | Merge Sort, Franceschini's Method | 69ms | 68ms |  |
| 19th | Tree Sort | 72ms | 70ms | 116% |
| 20th | I Can't Believe It Can Sort | 76ms | 75ms | 72% |
| 21st | Comb Sort | 88ms | 87ms | 92% |
| 22nd | Tim Sort | 94ms | 92ms | 86% |
| 23rd | Shell Sort | 97ms | 96ms | 57% |
| 24th | Heap Sort | 109ms | 109ms | 59% |
| 25th | Patience Sort | 133ms | 131ms | 67% |
| 26th | Counting Sort | 226ms | 226ms | 40% |
| 27th | Sample Sort | 383ms | 381ms | 37% |
| 28th | Block Sort | 393ms | 387ms | 43% |
| 29th | Sorting Network | 541ms | 544ms | 42% |
| 30th | Bitonic Sort Parallel | 693ms | 683ms | 64% |
| 31st | Merge Sort In-Place | 856ms | 853ms | 30% |
| 32nd | Strand Sort | 967ms | 961ms | 32% |
| 33rd | Pigeonhole Sort | 1s 420ms | 1s 408ms | 53% |
| 34th | Library Sort | 6s 529ms | 5s 902ms | 245% |
| 35th | Spaghetti Sort | 6s 887ms | 6s 908ms | 15% |
| 36th | Sleep Sort | 10s 381ms | 10s 368ms | 8% |
| 37th | Selection Sort | 16s 134ms | 16s 36ms | 19% |
| 38th | Insertion Sort | 17s 151ms | 16s 519ms | 79% |
| 39th | Tournament Sort | 24s 380ms | 24s 402ms | 17% |
| 40th | Pancake Sort | 25s 884ms | 25s 857ms | 14% |
| 41st | Exchange Sort | 26s 849ms | 26s 757ms | 36% |
| 42nd | Odd-Even Sort | 36s 46ms | 35s 947ms | 25% |
| 43rd | Cocktail Sort | 37s 161ms | 34s 327ms | 89% |
| 44th | Bubble Sort | 40s 294ms | 40s 1ms | 27% |
| 45th | Gnome Sort | 49s 198ms | 49s 74ms | 21% |
| 46th | Cycle Sort | 57s 750ms | 57s 620ms | 33% |
| 47th | Smooth Sort | 9min 16s 324ms | 9min 3s 240ms | 41% |

**Note:** The following algorithm were removed for this array size due to performance issues: Smooth Sort (at size 25,000)

