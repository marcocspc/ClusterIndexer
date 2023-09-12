import sys
import logging as logger
from tools.dataset import Dataset
from tools.data_normalizer import DataNormalizer
from tools.indexer_strategy import IndexerStrategy
from tools.parser import Parser


#old main method
def old_main():
    method = ''
    files = []

    #verificar se o método e o arquivo csv foram passados via linha de comando
    if '--normalize' not in sys.argv:
        # here is where the index calculation is done
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
        #here is where normalization is done
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

#new main method
def main():
    #check if we are going to normalize or calculate indexes
    parser = Parser()
    args = parser.args

    if args.command is None:
        parser.parser.print_help()
        exit(0)

    if args.command == "normalize":
        #here is where normalization is done

        if args.database is None:
            logger.error("No database specified! Please use some file.csv")
            exit(1)

        if args.output is None:
            logger.error("Cannot normlize data without '--output' specified!")
            exit(1)

        try:
            with open(args.output, 'w') as output:
                #load CSV
                dataset = Dataset(args.database)

                #check if CSV is valid
                #throws an exception if not
                normalizer = DataNormalizer()
                normalizer.validate(dataset)

                #normalize dataset
                dataset = normalizer.normalize(dataset)

                #save normalized
                output.write(dataset.getCSVText())
        except Exception as e:
            logger.error(e)
            logger.debug(e, exc_info=1)
            exit(1)

        exit(0)

    if args.command == "calculate_indexes":
        # here is where the index calculation is done

        if args.method is None:
            logger.error("No method specified! Please use daviesbouldin or silhouette.")
            exit(1)

        if args.database is None:
            logger.error("No database specified! Please use at least one file.csv")
            exit(1)

        for file in args.database:
            #carregar conjunto de dados CSV
            dataset = Dataset(file)

            #verificar se conjunto de dados é válido
            normalizer = DataNormalizer()
            try:
                normalizer.validate(dataset)
                dataset = normalizer.normalize(dataset)
                indexer = IndexerStrategy()
                indexer.chooseStrategy(dataset, method)

                if method == 'daviesbouldin':
                    print("In Davies-Bouldin index the lesser the result value is, " +
                    "more well distributed are the instances in the clusters.")
                elif method == 'silhouette':
                    print("In Silhouette index the closer to 1 the result value is, " +
                    "more well distributed are the instances in the clusters.")
            except Exception as e:
                logger.error(e)
                logger.debug(e, exc_info=1)
                exit(1)

        exit(0)


main()
