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
                sis[cluster].append(self.s(instance, cluster, clusters, normalizedDataSet.columnsLabels))
        scs = []
        for cluster in sis.keys():
            scs.append(sum(sis[cluster])/len(sis[cluster]))

        return sum(scs)/len(scs)

    def printResult(self, index, normalizedDataSet):
        print("O índice Silhouette para o Conjunto de Dados " +
        normalizedDataSet.filename + " foi: " + str(index))

    def b(self, i, icluster, clusteredDataset, columnsLabels):
        listaDeMediasPorCluster = {}
        listaDeMedias = []
        for cluster in clusteredDataset.keys():
            media = 0.0
            cont = 0.0
            if cluster != icluster:
                listaDeMediasPorCluster[cluster] = []
                for instance in clusteredDataset[cluster]:
                    eucl = 0.0
                    x = 0
                    while x < len(i):
                        if 'cat' in columnsLabels[x]:
                            catName = columnsLabels[x][0:columnsLabels[x].find('_')]
                            aux = x
                            y = 0
                            while (catName in columnsLabels[aux]):
                                y+=1
                                aux+=1

                            for k in range(y):
                                if float(i[x + k]) == 1.0:
                                    if float(i[x + k]) != float(instance[x + k]):
                                        eucl += 1
                                        k = y
                                    else:
                                        k = y
                            x += y
                        else:
                            eucl += math.pow(float(i[x]) - float(instance[x]), 2)
                            x+=1
                    eucl = math.sqrt(eucl)
                    listaDeMediasPorCluster[cluster].append(eucl)
            if (cluster in listaDeMediasPorCluster.keys()):
                listaDeMedias.append(sum(listaDeMediasPorCluster[cluster])/len(listaDeMediasPorCluster[cluster]))
        return min(listaDeMedias)

    def a(self, i, icluster, clusteredDataset, columnsLabels):
        if len(clusteredDataset[icluster]) == 1:
            return 1
        else:
            media = 0.0
            cont = 0.0
            for instance in clusteredDataset[icluster]:
                if instance is not i:
                    eucl = 0.0
                    x = 0
                    while x < len(i):
                        if 'cat' in columnsLabels[x]:
                            catName = columnsLabels[x][0:columnsLabels[x].find('_')]
                            aux = x
                            y = 0
                            while (catName in columnsLabels[aux]):
                                y+=1
                                aux+=1

                            for k in range(y):
                                if float(i[x + k]) == 1.0:
                                    if float(i[x + k]) != float(instance[x + k]):
                                        eucl += 1
                                        k = y
                                    else:
                                        k = y
                            x += y
                        else:
                            eucl += math.pow(float(i[x]) - float(instance[x]), 2)
                            x+=1
                    eucl = math.sqrt(eucl)
                    media += eucl
                    cont += 1
            return media/cont

    def s(self, i, icluster, clusteredDataset, columnsLabels):
        bi = self.b(i, icluster, clusteredDataset, columnsLabels)
        ai = self.a(i, icluster, clusteredDataset, columnsLabels)
        return (bi - ai)/max([bi, ai])
