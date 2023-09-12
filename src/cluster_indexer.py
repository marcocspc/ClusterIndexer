import sys
from tools.dataset import Dataset
from tools.data_normalizer import DataNormalizer
from tools.indexer_strategy import IndexerStrategy

#método principal
def main():
    method = ''
    files = []

    #verificar se o método e o arquivo csv foram passados via linha de comando
    if '--normalize' not in sys.argv:
        if '--method' in sys.argv:
            method = sys.argv[sys.argv.index('--method') + 1]
        else:
            raise Exception("No method specified! Please use 'daviesbouldin' or 'silhouette'")

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

        if method == 'daviesbouldin':
            print("Para o índice Davies-Bouldin, quanto o menor o valor, " +
            "mais bem distribuídas estão as instâncias dos agrupamentos.")
        elif method == 'silhouette':
            print("Para o índice Silhouette, quanto mais próximo de 1 o valor, " +
            "mais bem distribuídas estão as instâncias dos agrupamentos.")
    else:
        if '--database' in sys.argv:
            files.append(sys.argv[sys.argv.index('--database') + 1])
        else:
            raise Exception("No database specified! Please use some file.csv")

        try:
            if '--normalize' in sys.argv:
                if '--output' in sys.argv:
                    with open(sys.argv[sys.argv.index('--output') + 1], 'w') as output:
                        #carregar conjunto de dados CSV
                        dataset = Dataset(files[0])

                        #verificar se conjunto de dados é válido
                        normalizer = DataNormalizer()

                        normalizer.validate(dataset)
                        dataset = normalizer.normalize(dataset)

                        output.write(dataset.getCSVText())
                else:
                    raise Exception("Cannot normlize data without '--output' specified!")
        except Exception as e:
            raise e


main()
