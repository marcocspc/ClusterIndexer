import pandas
import math

class SilhouetteStrategy:
    def executeStrategy(self, normalizedDataSet):
        self.printResult(self.calculateIndex(normalizedDataSet))

    def calculateIndex(self, normalizedDataSet):
        pandas.options.mode.chained_assignment = None
        csvData = pandas.DataFrame(data=normalizedDataSet.toDict())

        #Adicionando colunas de cálculo
        csvData["ai"] = 0
        csvData["bi"] = 0
        csvData["si"] = 0

        # #Ordenando pelo agrupamento
        # csvData = csvData.sort_values("Cluster")

        #Separando os agrupamentos
        total_clusters = csvData["Cluster"].unique()
        clusters = {}

        for c in total_clusters:
            clusters[c] = (csvData.loc[csvData["Cluster"] == c])
            #clusters[c].drop(["Cluster"], axis=1, inplace=True)

        #Cálculo para o ai
        #Itera entre os clusters
        for key, cluster in clusters.items():
            #Fixa uma linha por vez
            for fixed_index, fixed_row in cluster.iterrows():
                ai_total = []

                #Itera nas demais linhas do mesmo cluster
                for index, row in cluster.iterrows():
                    ai = 0

                    #Se a linha for a mesma da linha fixa desconsidera
                    if index == fixed_index:
                        continue

                    columns = len(row)

                    #Itera entre as colunas
                    for i in range(0, columns - 4):
                        isnumeric = str(row[i]).replace('.', '').isnumeric()

                        data = 0

                        if isnumeric:
                            data = math.pow((float(fixed_row[i]) - float(row[i])), 2)
                            ai = ai + data
                        else:
                            if fixed_row[i] == row[i]:
                                data = 0
                            else:
                                data = 1

                            ai = ai + data

                    ai = math.sqrt(ai)
                    ai_total.append(ai)

                #Seta o ai da linha fixa com a média dos ai do cluster
                if len(ai_total) > 0:
                    cluster.loc[cluster.index == fixed_index, "ai"] = sum(ai_total) / len(ai_total)

        #Cálculo do bi
        #Itera entre os clusters
        for fixed_cluster_key, fixed_cluster in clusters.items():
            #Fixando uma linha do cluster por vez
            for fixed_index, fixed_row in fixed_cluster.iterrows():
                bi_medias = []
                #Iterando entre os outros clusters
                for cluster_key, cluster in clusters.items():
                    bi_total = []
                    #Ignora o cluster fixo
                    if cluster_key == fixed_cluster_key:
                        continue

                    #Iterando entre os itens do cluster
                    for index, row in cluster.iterrows():
                        bi = 0
                        columns = len(row)

                        # Itera entre as colunas
                        for i in range(0, columns - 4):
                            isnumeric = str(row[i]).replace('.', '').isnumeric()

                            if isnumeric:
                                data = ((float(fixed_row[i]) - float(row[i])) ** 2)
                                bi = bi + data
                            else:
                                if fixed_row[i] == row[i]:
                                    data = 0
                                else:
                                    data = 1
                                bi = bi + data

                        bi = (bi ** 0.5)
                        bi_total.append(bi)

                    # Seta o ai da linha fixa com a média dos ai do cluster
                    if len(bi_total) > 0:
                        bi_medias.append(sum(bi_total) / len(bi_total))

                if len(bi_medias) > 0:
                    fixed_cluster.loc[fixed_cluster.index == fixed_index, "bi"] = min(bi_medias)

        #Cálculo do si
        for key, cluster in clusters.items():
            for index, row in cluster.iterrows():
                data = (row["bi"] - row["ai"]) / max(row["bi"], row["ai"])
                cluster.loc[cluster.index == index, "si"] = data

        #Cálculo dos sCluster
        s_clusters = {}
        for key, cluster in clusters.items():
            si_total = cluster["si"].tolist()
            if len(si_total) > 0:
                si_media = sum(si_total) / len(si_total)
                s_clusters[key] = si_media
            else:
                s_clusters[key] = 0

        #Cálculo do Silhuette Total
        return sum(s_clusters.values()) / len(s_clusters.values())




    def printResult(self, index):
        print("O índice silhouette foi: " + str(index))
