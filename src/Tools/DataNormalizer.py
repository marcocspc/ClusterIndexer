class DataNormalizer:
    def validate(self, dataset):
        result = False

        if 'Cluster' in dataset.columnsLabels:
            result = True
            for line in dataset.data:
                if len(line) != len(dataset.columnsLabels):
                    result = False
                    break
        else:
            raise Exception("This database does not contain Cluster column.")

        if result:
            return result
        else:
            raise Exception("Number of columns doesn't match on every line of"
            + "database!")


    def normalize(self, dataset):
        i = 0
        while i < len(dataset.columnsLabels):
            if not self.isNormalized(dataset, i):
                if self.comlumnType(dataset, i) == 'string':
                    values = []
                    columnLabel = dataset.columnsLabels[i]
                    columnLabelIndex = dataset.columnsLabels.index(columnLabel)

                    for line in dataset.data:
                        if (line[i] not in values and
                        columnLabel + '_' + line[i] + '_cat' not in values):
                            values.append(columnLabel + '_' + line[i] + '_cat')

                    dataset.columnsLabels[i+1:i+1] = values.copy()
                    dataset.columnsLabels.pop(i)

                    for line in dataset.data:
                        auxlist = [0.0] * len(values)
                        auxlist[values.index(columnLabel + '_' + line[i] + '_cat')] = 1.0
                        line[i+1:i+1] = auxlist
                        line.pop(i)

                    i += len(values) - 1
                    continue
                elif self.comlumnType(dataset, i) == 'digit':
                    min = float(dataset.data[0][i])
                    max = float(dataset.data[0][i])

                    for line in dataset.data:
                        value = float(line[i])
                        if value < min:
                            min = value
                        elif value > max:
                            max = value

                    for line in dataset.data:
                        value = float(line[i])
                        value = (value - min) / (max - min)
                        line[i] = value
            i += 1

        return dataset

    def comlumnType(self, dataset, columnNumber):
        if not dataset.columnsLabels[columnNumber] == 'Cluster':
            for line in dataset.data:
                if not line[columnNumber].replace('.','',1).isdigit():
                    return 'string'
            return 'digit'
        else:
            return 'Cluster'

    def isNormalized(self, dataset, columnNumber):
        for line in dataset.data:
            if not isinstance(line[columnNumber], float):
                if not line[columnNumber].replace('.','',1).isdigit():
                    return False
                else:
                    value = float(line[columnNumber])
                    if value < 0 or value > 1:
                        return False
        return True
