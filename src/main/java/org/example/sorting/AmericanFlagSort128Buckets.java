package org.example.sorting;

import org.example.SortingAlgorithm;

public class AmericanFlagSort128Buckets implements SortingAlgorithm {
    @Override
    public void sort(int[] arr) {
        int len = arr.length;
        int h = 1;
        while (h < len / 3) {
            h = 3 * h + 1;
        }
        while (h > 0) {
            for (int i = h; i < len; i++) {
                int j = i;
                int tmp = arr[i];
                while (j >= h && arr[j - h] > tmp) {
                    arr[j] = arr[j - h];
                    j -= h;
                }
                arr[j] = tmp;
            }
            h /= 3;
        }
    }
}

