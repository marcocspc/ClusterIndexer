import argparse

class Parser():

    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="clusterindexer")

        self.subparsers = self.parser.add_subparsers(
                title="subcommands", help="DB operations on CSV files.",
                dest="command"
                )

        database_argument = {
                "dest": ("-d", "--database"),
                "help": "Path of the source database in CSV format. Multiple files can be passed.",
                "action": "store",
                "nargs": '+'
                }

        method_argument = {
                "dest": ("-m", "--method"),
                "help": "Method to use when calculating indexes.",
                "action": "store",
                "nargs": '1',
                "choices": {"daviesbouldin", "silhouette"},
                }

        output_argument = {
                "dest": ("-o", "--output"),
                "help": "Path of the output database in CSV format.",
                "action": "store",
                "nargs": 1
                }


        self.normalize_parser = self.subparsers.add_parser("normalize",
                                help="Normalize a dataset.")
        self.normalize_parser.add_argument(**database_argument)

        self.calculate_indexes_parser = self.subparsers.add_parser("calculate_indexes",
                                 help="Calculate indexes given a clusterized dataset. " +
                                 "Both Silhouette or Davies-Bouldin methods can be chosen.")
        self.calculate_indexes_parser.add_argument(**database_argument)
        self.calculate_indexes_parser.add_argument(**method_argument)
        self.calculate_indexes_parser.add_argument(**output_argument)

        self.args = self.parser.parse_args()
