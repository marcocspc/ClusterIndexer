# ClusterIndexer

This was a project I did in my Master's Degree to help me calculate the Davies-Bouldin &amp; Silhouette indexes on clusterized datasets.

In addition to this, this script is capable of normalizing datasets in order to use clustering algorithms on it. Currently, unfortunately, it is not capable of applying these algorithms to the dataset, but it will be included in the roadmap.

# How to use

- If you need to test some file.csv using Davies-Bouldin index:
`python3 ClusterIndexer.py --method daviesbouldin --database file.csv`
- If you need to test some file.csv using Silhouette index:
`python3 ClusterIndexer.py --method silhouette --database file.csv`
- If you need to compare several databases, just add multiple --compare-to options:
`python3 ClusterIndexer.py --method davesbouldin --database file.csv --compare-to file2.csv --compare-to file3.csv`
- If you need to normalize a CSV file, use the following command line:
`python3 ClusterIndexer.py --normalize --database file.csv --output file2.csv`

#Roadmap

- [] Show columns that are missing data;
- [] Show Pearson correlation between columns;
- Include support for the following clustering algorithms:
  - [] kMeans;
  - [] Hierarchical;
