import os

class Dataset:
    def __init__(self, csvfile):
        #atributos
        self.filename = os.path.basename(csvfile)
        self.columnsLabels = []
        self.data = []

        #preparar arquivo passado como parametro
        try:
            self.prepareLabelsAndData(csvfile)
            self.removeEmptyLists()
        except IOError:
            raise


    def prepareLabelsAndData(self, csvfile):
        try:
            with open(csvfile) as filecont:
                set = filecont.read()
                set = set.split('\n')
                self.columnsLabels = set.pop(0).split(',')
                for line in set:
                    self.data.append(line.split(','))
        except IOError:
            raise

    def removeEmptyLists(self):
        newlist = [x for x in self.columnsLabels if len(x) > 1]
        self.columnsLabels = newlist
        newlist = [x for x in self.data if len(x) > 1]
        self.data = newlist

    def print(self):
        print('\t'.join([str(cell) for cell in self.columnsLabels]))
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.data]))

    def getCSVText(self):
        text = (','.join([str(cell) for cell in self.columnsLabels]))
        text += '\n'
        text += ('\n'.join([','.join([str(cell) for cell in row]) for row in self.data]))
        return text

    def toClusteredDict(self):
        dict = {}

        for line in self.data:

            try:
                cluster = line.pop(self.columnsLabels.index('Cluster'))
            except ValueError:
                cluster = line.pop(self.columnsLabels.index('cluster'))

            if cluster not in dict.keys():
                dict[cluster] = []
                dict[cluster].append(line)
            else:
                dict[cluster].append(line)

        return dict
