package org.example.sorting;

public class andreyAstrelinInplaceMergeSort implements org.example.SortingAlgorithm {

    @Override
    public void sort(int[] arr) {
        // Implementation of Andrei Astrelin's in-place merge sort algorithm
        int[] buffer = new int[arr.length];
        mergeSort(arr, buffer, 0, arr.length - 1);
    }

    private void mergeSort(int[] arr, int[] buffer, int left, int right) {
        if (left >= right) {
            return;
        }

        int middle = (left + right) / 2;

        mergeSort(arr, buffer, left, middle);
        mergeSort(arr, buffer, middle + 1, right);
        merge(arr, buffer, left, middle, right);
    }

    private void merge(int[] arr, int[] buffer, int left, int middle, int right) {
        int leftIndex = left;
        int rightIndex = middle + 1;
        int bufferIndex = left;

        while (leftIndex <= middle && rightIndex <= right) {
            if (arr[leftIndex] <= arr[rightIndex]) {
                buffer[bufferIndex++] = arr[leftIndex++];
            } else {
                buffer[bufferIndex++] = arr[rightIndex++];
            }
        }

        while (leftIndex <= middle) {
            buffer[bufferIndex++] = arr[leftIndex++];
        }

        while (rightIndex <= right) {
            buffer[bufferIndex++] = arr[rightIndex++];
        }

        if (right + 1 - left >= 0) {
            System.arraycopy(buffer, left, arr, left, right + 1 - left);
        }
    }
}

