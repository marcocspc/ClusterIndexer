import sys
from Tools.Dataset import Dataset
from Tools.DataNormalizer import DataNormalizer

#método principal
def main():
    method = ''
    file = ''

    #verificar se o método e o arquivo csv foram passados via linha de comando
    if '--method' in sys.argv:
        method = sys.argv[sys.argv.index('--method') + 1]
    else:
        raise Exception("No method specified! Please use 'db' or 'silhouette'")

    if '--database' in sys.argv:
        file = sys.argv[sys.argv.index('--database') + 1]
    else:
        raise Exception("No database specified! Please use some file.csv")

    #carregar conjunto de dados CSV
    dataset = Dataset(file)

    #verificar se conjunto de dados é válido
    normalizer = DataNormalizer()
    try:
        if normalizer.validate(dataset):
            dataset = normalizer.normalize(dataset)

            
    except Exception as e:
        raise e

main()
