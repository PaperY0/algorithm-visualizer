public static void radixSort(int[] a) {
    int max = Arrays.stream(a).max().getAsInt();
    for (int exp = 1; max / exp > 0; exp *= 10) {
        countingSortByDigit(a, exp);
    }
}

private static void countingSortByDigit(int[] a, int exp) {
    int n = a.length;
    int[] output = new int[n];
    int[] count = new int[10];

    for (int i = 0; i < n; i++) {
        count[(a[i] / exp) % 10]++;
    }
    for (int i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }
    for (int i = n - 1; i >= 0; i--) {
        output[count[(a[i] / exp) % 10] - 1] = a[i];
        count[(a[i] / exp) % 10]--;
    }
    System.arraycopy(output, 0, a, 0, n);
}
