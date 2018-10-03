import math

class DaviesBouldinStrategy:
    def executeStrategy(self, normalizedDataSet):
        self.printResult(self.calculateIndex(normalizedDataSet), normalizedDataSet)

    def calculateIndex(self, normalizedDataSet):
        clusters = normalizedDataSet.toClusteredDict()
        centroids = self.getCentroids(clusters)
        es = self.es(clusters, centroids)
        dist = self.distEntreCentroids(centroids)
        rs = self.rs(es, dist)
        mrs = self.mrs(rs)
        return self.db_index(mrs)

    def printResult(self, index, normalizedDataSet):
        print("O índice Davies-Bouldin para o Conjunto de Dados " +
        normalizedDataSet.filename + " foi: " + str(index))

    def getCentroids(self, pclusters):
        clusters = pclusters
        centroids = {}
        for cluster in clusters.keys():
            centroids[cluster] = []
            for i in range(len(clusters[cluster][0]) - 1):
                mediaCol = 0
                for instance in clusters[cluster]:
                    mediaCol += float(instance[i])
                centroids[cluster].append(mediaCol/len(clusters[cluster]))
        return centroids

    def es(self, pclusters, centroids):
        clusters = pclusters
        es = {}

        for cluster in clusters.keys():
            listaMedias = []
            for instance in clusters[cluster]:
                mediaAtual = 0
                for i in range(len(clusters[cluster][0]) - 1):
                    mediaAtual += math.fabs(float(centroids[cluster][i]) - float(instance[i]))
                mediaAutal = math.pow(mediaAtual,2)
                listaMedias.append(mediaAtual)
            es[cluster] = sum(listaMedias)/len(listaMedias)

        return es

    def distEntreCentroids(self, centroids):
        dist = {}
        ckeys = list(centroids.keys())

        for i in range(len(centroids) - 1):
            for j in range(len(centroids)):
                j = i + 1
                label = "[" + str(i + 1) + ", " + str(j + 1) + "]"
                soma = 0
                for x in range(len(centroids[ckeys[i]])):
                    soma += math.fabs(centroids[ckeys[i]][x] - centroids[ckeys[j]][x])
                dist[label] = soma

        return dist

    def rs(self, es, distEntCen):
        rss = {}
        esvalues = list(es.values())

        for i in range(len(es) - 1):
            for j in range(len(es)):
                j = i + 1
                label = "[" + str(i + 1) + ", " + str(j + 1) + "]"
                rss[label] = (float(esvalues[i]) + float(esvalues[j])) / float(distEntCen[label])

        return rss

    def mrs(self, rs):
        mrs = []
        rsvalues = list(rs.values())

        for i in range(len(rs) - 1):
            for j in range(len(rs)):
                mrs.append(max(rsvalues[i], rsvalues[j]))

        return mrs

    def db_index(self, mrs):
        return sum(mrs)/len(mrs)
