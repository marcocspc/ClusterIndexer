from Tools.DaviesBouldinStrategy import DaviesBouldinStrategy
from Tools.SilhouetteStrategy import SilhouetteStrategy

class IndexerStrategy:
    def chooseStrategy(self, normalizedDataSet, method):
        #aqui será feita a escolha entre utilizar DaviesBouldinStrategy
        #ou SilhouetteStrategy, dependendo do valor de method
        dbs = DaviesBouldinStrategy()
        sils = SilhouetteStrategy()

        if method == 'davesbouldin':
            dbs.executeStrategy(normalizedDataSet)
        elif method == 'silhouette':
            sils.executeStrategy(normalizedDataSet)
