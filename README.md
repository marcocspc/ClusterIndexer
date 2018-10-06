# ClusterIndexer
Davies-Bouldin &amp; Silhouette Indexes calculator

#How to use

- If you need to test some file.csv using Davies-Bouldin index:
`python3 ClusterIndexer.py --method daviesbouldin --database file.csv`
- If you need to test some file.csv using Silhouette index:
`python3 ClusterIndexer.py --method silhouette --database file.csv`
- If you need to compare several databases, just add multiple --compare-to options:
`python3 ClusterIndexer.py --method davesbouldin --database file.csv --compare-to file2.csv --compare-to file3.csv`
- If you need to normalize a CSV file, use the following command line:
`python3 ClusterIndexer.py --normalize --database file.csv --output file2.csv`
