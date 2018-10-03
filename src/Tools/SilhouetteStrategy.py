import math

class SilhouetteStrategy:
    def executeStrategy(self, normalizedDataSet):
        self.printResult(self.calculateIndex(normalizedDataSet), normalizedDataSet)

    def calculateIndex(self, normalizedDataSet):
        clusters = normalizedDataSet.toClusteredDict()
        sis = {}
        for cluster in clusters.keys():
            sis[cluster] = []
            for instance in clusters[cluster]:
                sis[cluster].append(self.s(instance, cluster, clusters))

        scs = []
        for cluster in sis.keys():
            scs.append(sum(sis[cluster])/len(sis[cluster]))

        return sum(scs)/len(scs)

    def printResult(self, index, normalizedDataSet):
        print("O índice Silhouette para o Conjunto de Dados " +
        normalizedDataSet.filename + " foi: " + str(index))

    def b(self, i, icluster, clusteredDataset):
        listaDeMedias = []
        for cluster in clusteredDataset.keys():
            media = 0.0
            cont = 0.0
            if cluster != icluster:
                for instance in clusteredDataset[cluster]:
                    eucl = 0.0
                    for x in range(len(i)):
                        eucl += math.pow(float(i[x]) - float(instance[x]), 2)
                    eucl = math.sqrt(eucl)
                    media += eucl
                    cont += 1
                listaDeMedias.append(media/cont)
        return min(listaDeMedias)

    def a(self, i, icluster, clusteredDataset):
        if len(clusteredDataset[icluster]) == 1:
            return 1
        else:
            media = 0.0
            cont = 0.0
            for instance in clusteredDataset[icluster]:
                if instance is not i:
                    eucl = 0.0
                    for x in range(len(i)):
                        eucl += math.pow(float(i[x]) - float(instance[x]), 2)
                    eucl = math.sqrt(eucl)
                    media += eucl
                    cont += 1
            return media/cont

    def s(self, i, icluster, clusteredDataset):
        bi = self.b(i, icluster, clusteredDataset)
        ai = self.a(i, icluster, clusteredDataset)
        return (bi - ai)/max([bi, ai])
