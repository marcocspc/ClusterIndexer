import sys
from Tools.Dataset import Dataset
from Tools.DataNormalizer import DataNormalizer
from Tools.IndexerStrategy import IndexerStrategy

#método principal
def main():
    method = ''
    files = []

    #verificar se o método e o arquivo csv foram passados via linha de comando
    if '--method' in sys.argv:
        method = sys.argv[sys.argv.index('--method') + 1]
    else:
        raise Exception("No method specified! Please use 'db' or 'silhouette'")

    if '--database' in sys.argv:
        files.append(sys.argv[sys.argv.index('--database') + 1])
    else:
        raise Exception("No database specified! Please use some file.csv")

    while '--compare-to' in sys.argv:
        files.append(sys.argv.pop(sys.argv.index('--compare-to') + 1))
        sys.argv.pop(sys.argv.index('--compare-to'))

    for file in files:
        #carregar conjunto de dados CSV
        dataset = Dataset(file)

        #verificar se conjunto de dados é válido
        normalizer = DataNormalizer()
        try:
            normalizer.validate(dataset)
            dataset = normalizer.normalize(dataset)
            indexer = IndexerStrategy()
            indexer.chooseStrategy(dataset, method)
        except Exception as e:
            raise e

main()
