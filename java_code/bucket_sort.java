public static void bucketSort(int[] a) {
    int n = a.length;
    int max = Arrays.stream(a).max().getAsInt();
    int min = Arrays.stream(a).min().getAsInt();
    int bucketCount = (max - min) / n + 1;
    List<List<Integer>> buckets = new ArrayList<>();
    for (int i = 0; i < bucketCount; i++) {
        buckets.add(new ArrayList<>());
    }
    for (int i = 0; i < n; i++) {
        int idx = (a[i] - min) / n;
        buckets.get(idx).add(a[i]);
    }
    int index = 0;
    for (List<Integer> bucket : buckets) {
        Collections.sort(bucket);
        for (int val : bucket) {
            a[index++] = val;
        }
    }
}
