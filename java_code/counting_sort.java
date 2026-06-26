public static void countingSort(int[] a) {
    int n = a.length;
    int max = Arrays.stream(a).max().getAsInt();
    int min = Arrays.stream(a).min().getAsInt();
    int range = max - min + 1;
    int[] count = new int[range];
    int[] output = new int[n];

    for (int i = 0; i < n; i++) {
        count[a[i] - min]++;
    }
    for (int i = 1; i < range; i++) {
        count[i] += count[i - 1];
    }
    for (int i = n - 1; i >= 0; i--) {
        output[count[a[i] - min] - 1] = a[i];
        count[a[i] - min]--;
    }
    System.arraycopy(output, 0, a, 0, n);
}
