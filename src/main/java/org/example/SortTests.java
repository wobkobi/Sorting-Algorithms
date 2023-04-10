package org.example;


import org.example.sorting.*;

import java.util.*;

public class SortTests {
	public static void main(String[] args) {
		int[] arr = {64, 34, 25, 12, 22, 11, 90};
		List<SortingAlgorithm> algorithms = new ArrayList<>();
		algorithms.add(new BubbleSort());
		algorithms.add(new OptimizedBubbleSort());
		algorithms.add(new CocktailShakerSort());
		algorithms.add(new OptimizedCocktailShakerSort());
		algorithms.add(new OddEvenSort());
		algorithms.add(new GnomeSort());
		algorithms.add(new OptimizedGnomeSort());
		algorithms.add(new OptimizedGnomeSortWithBinarySearch());
		algorithms.add(new CombSort());
		algorithms.add(new CircleSort());
		algorithms.add(new QuickSortWithLeftLeftPointers());
		algorithms.add(new QuickSortWithLeftRightPointers());
		algorithms.add(new DualPivotQuickSort());
		algorithms.add(new SelectionSort());
		algorithms.add(new DoubleSelectionSort());
		algorithms.add(new CycleSort());
		algorithms.add(new MaxHeapSort());
		algorithms.add(new MinHeapSort());
		algorithms.add(new FlippedMinHeapSort());
		algorithms.add(new WeakHeapSort());
		algorithms.add(new TernaryHeapSort());
		algorithms.add(new PoplarHeapSort());
		algorithms.add(new TournamentSort());
		algorithms.add(new InsertionSort());
		algorithms.add(new BinaryInsertionSort());
		algorithms.add(new ShellSort());
		algorithms.add(new PatienceSort());
		algorithms.add(new UnbalancedTreeSort());
		algorithms.add(new MergeSort());
		algorithms.add(new BottomUpMergeSort());
		algorithms.add(new InPlaceMergeSort());
		algorithms.add(new AndreiAstrelinsInPlaceMergeSort());
		algorithms.add(new LazyStableSort());
		algorithms.add(new RotateMergeSort());
		algorithms.add(new CountingSort());
		algorithms.add(new PigeonholeSort());
		algorithms.add(new GravitySort());
		algorithms.add(new AmericanFlagSort128Buckets());
		algorithms.add(new LSDRadixSortBase4());
		algorithms.add(new InPlaceLSDRadixSortBase10());
		algorithms.add(new MSDRadixSortBase4());
		algorithms.add(new FlashSort());
		algorithms.add(new IterativeBinaryQuickSort());
		algorithms.add(new RecursiveBinaryQuickSort());
		algorithms.add(new ShatterSort());
		algorithms.add(new SimpleShatterSort());
		algorithms.add(new TimeSortMul10());
		algorithms.add(new BatcherBitonicSort());
		algorithms.add(new BatcherOddEvenMergeSort());
		algorithms.add(new RecursivePairwiseSortingNetwork());
		algorithms.add(new IterativeBitonicSort());
		algorithms.add(new IterativeOddEvenMergeSort());
		algorithms.add(new IterativePairwiseSortingNetwork());
		algorithms.add(new HybridCombSort());
		algorithms.add(new IntrospectiveCircleSort());
		algorithms.add(new BinaryMergeSort());
		algorithms.add(new WeaveMergeSort());
		algorithms.add(new TimSort());
		algorithms.add(new CocktailMergeSort());
		algorithms.add(new WikiSort());
		algorithms.add(new GrailSort());
		algorithms.add(new SqrtSort());
		algorithms.add(new IntrospectiveSort());
		algorithms.add(new STDSort());
		algorithms.add(new OptimizedBottomUpMergeSort());
		algorithms.add(new OptimizedDualPivotQuickSort());
		algorithms.add(new PatternDefeatingQuickSort());
		algorithms.add(new BranchlessPatternDefeatingQuickSort());
		algorithms.add(new PancakeSort());
		algorithms.add(new BadSort());
		algorithms.add(new StoogeSort());
		algorithms.add(new SillySort());
		algorithms.add(new SlowSort());
		algorithms.add(new ExchangeBogoSort());
		algorithms.add(new BubbleBogoSort());
		algorithms.add(new LessBogoSort());
		algorithms.add(new CocktailBogoSort());
		algorithms.add(new bogoBogoSort());

		// Run each algorithm and record the time taken
		Map<String, Long> times = new HashMap<>();
		for (SortingAlgorithm algorithm : algorithms) {
			int[] copy = Arrays.copyOf(arr, arr.length);
			long startTime = System.nanoTime();
			algorithm.sort(copy);
			long endTime = System.nanoTime();
			long timeTaken = endTime - startTime;
			times.put(algorithm.getClass().getSimpleName(), timeTaken);
		}

		// Sort the algorithms by their time taken
		List<Map.Entry<String, Long>> sortedTimes = new ArrayList<>(times.entrySet());
		sortedTimes.sort(Map.Entry.comparingByValue());

		// Print the results
		System.out.println("Results (sorted by time taken):");
		for (Map.Entry<String, Long> entry : sortedTimes) {
			String algorithmName = entry.getKey();
			long timeTaken = entry.getValue();
			System.out.println(algorithmName + ": " + timeTaken + " nanoseconds");
		}
	}
}


