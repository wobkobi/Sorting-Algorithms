package org.example.sorting;

import java.util.Random;

public class BogoSort implements org.example.SortingAlgorithm {
    @Override
    public void sort(int[] arr) {
        while (!isSorted(arr)) {
            shuffle(arr);
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

    static void shuffle(int[] arr) {
        Random random = new Random();
        for (int i = 0; i < arr.length; i++) {
            int randomIndex = random.nextInt(arr.length);
            int temp = arr[i];
            arr[i] = arr[randomIndex];
            arr[randomIndex] = temp;
        }
    }
}
