package org.example.sorting;

import java.util.Arrays;

public class BogoBogoSort implements org.example.SortingAlgorithm {
    @Override
    public void sort(int[] arr) {
        for (int i = 1; i <= arr.length; i++) {
            int[] sublist = Arrays.copyOf(arr, i);
            while (!isSorted(sublist)) {
                BogoSort.shuffle(sublist);
            }
            System.arraycopy(sublist, 0, arr, 0, i);
        }
    }

    private boolean isSorted(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i] > arr[i + 1]) {
                return false;
            }
        }
        return true;
    }


}
