from tools.davies_bouldin_strategy import DaviesBouldinStrategy
from tools.silhouette_strategy import SilhouetteStrategy

class IndexerStrategy:
    def chooseStrategy(self, normalizedDataSet, method):
        #aqui será feita a escolha entre utilizar DaviesBouldinStrategy
        #ou SilhouetteStrategy, dependendo do valor de method
        dbs = DaviesBouldinStrategy()
        sils = SilhouetteStrategy()

        if method == 'daviesbouldin':
            dbs.executeStrategy(normalizedDataSet)
        elif method == 'silhouette':
            sils.executeStrategy(normalizedDataSet)
        else:
            raise Exception("Method not recognized: " + method)
