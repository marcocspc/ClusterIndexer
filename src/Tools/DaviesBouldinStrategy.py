import math

class DaviesBouldinStrategy:

    def executeStrategy(self, normalizedDataSet):
        """Executa classificação

        Args:
            normalizedDataSet: Objeto da classe DataNormalizer.

        Returns:
            string: Indices calculados.
        """

        self.printResult(self.calculateIndex(normalizedDataSet), normalizedDataSet)

    def calculateIndex(self, normalizedDataSet):
        """Cálcula indices

        Args:
            normalizedDataSet: Objeto da classe DataNormalizer.

        Returns:
            number: Média da lista MRS.

        Workflow:
            1 - Separa clusters;
            2 - Cálcula centroids;
            3 - Encontra ES;
            4 - Cálcula distancia euclidiana;
            5 - Encontra RS;
            6 - Encontra MRS;
        """

        clusters = normalizedDataSet.toClusteredDict()
        centroids = self.getCentroids(clusters, normalizedDataSet)
        es = self.es(clusters, centroids)
        dist = self.distEntreCentroids(centroids)
        rs = self.rs(es, dist)
        mrs = self.mrs(rs)
        return self.db_index(mrs)

    def printResult(self, index, normalizedDataSet):
        """Mensagem de retorno para o usuário

        Args:
            index: Indice calculado com base no DataNormalizer.
            normalizedDataSet: Objeto da classe DataSet normalizado.
        """

        print("O índice Davies-Bouldin para o Conjunto de Dados " +
        normalizedDataSet.filename + " foi: " + str(index))

    def getCentroids(self, pclusters, normalizedDataSet):
        """Cálculo de centroids do cluster

        Args:
            pclusters: Clusters para cálculo dos centroids.
            normalizedDataSet: Dataset normalizado.

        Returns:
            dict: Médias calculadas.

        Workflow:
            1 - Varre o cluster;
            2 - Cálcula médianas;
        """

        clusters = pclusters
        centroids = {}
        columnsLabels = normalizedDataSet.columnsLabels
        for cluster in clusters.keys():
            centroids[cluster] = []
            i = 0
            while i < len(clusters[cluster][0]) - 1:
                if 'cat' in columnsLabels[i]:
                    catName = columnsLabels[i][0:columnsLabels[i].find('_')]
                    aux = i
                    j = 0
                    while (catName in columnsLabels[aux]):
                        j+=1
                        aux+=1
                    indColMod = 0
                    maior = 0
                    for k in range(j):
                        cont = 0
                        for instance in clusters[cluster]:
                            if instance[i + k] == 1:
                                cont+=1
                        if cont > maior:
                            indColMod = k
                            maior = cont
                    for k in range(j):
                        if k == indColMod:
                            centroids[cluster].append(1.0)
                        else:
                            centroids[cluster].append(0.0)
                    i+=j
                else:
                    mediaCol = 0
                    for instance in clusters[cluster]:
                        mediaCol += float(instance[i])
                    centroids[cluster].append(mediaCol/len(clusters[cluster]))
                    i+=1
        return centroids

    def es(self, pclusters, centroids):
        """Encontra ES's do cluster

        Args:
            pclusters: Clusters para cálculo.
            centroids: Centroids já previamente calculados.

        Returns:
            dict: Médias calculadas.
        """

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
        """Cálculo da distancia entre centroids

        Args:
            centroids: Centroids já previamente calculados.

        Returns:
            dict: Distâncias euclidianas calculadas.
        """

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
        """Encontra RS's

        Args:
            es: ES's já previamente calculados.
            distEntCen: Distâncias já previamente calculados.

        Returns:
            dict: RS's.
        """

        rss = {}
        esvalues = list(es.values())

        for i in range(len(es) - 1):
            for j in range(len(es)):
                j = i + 1
                label = "[" + str(i + 1) + ", " + str(j + 1) + "]"
                rss[label] = (float(esvalues[i]) + float(esvalues[j])) / float(distEntCen[label])

        return rss

    def mrs(self, rs):
        """Encontra MRS's

        Args:
            rs: RS's já previamente calculados.

        Returns:
            array: Valores máximos calculados.
        """

        mrs = []
        rsvalues = list(rs.values())

        for i in range(len(rs) - 1):
            for j in range(len(rs)):
                mrs.append(max(rsvalues[i], rsvalues[j]))

        return mrs

    def db_index(self, mrs):
        """Encontra média de um MRS

        Args:
            mrs: MRS já previamente calculados.

        Returns:
            number: Cálculo de média.
        """

        return sum(mrs)/len(mrs)
