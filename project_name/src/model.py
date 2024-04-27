import pandas as pd
import pathlib

APP_PATH = pathlib.Path(__file__).parents[1]
DB_PATH = APP_PATH / "data" / "food.csv"

def connect():
    return pd.read_csv(DB_PATH)

@pd.api.extensions.register_dataframe_accessor("foods")
class FoodDB:

    pd = pd
    verbose: bool
    choices: list
    temp_choices: list
    log: list

    def __init__(self, pandas_obj, verbose = True):
        self.verbose = verbose
        self.choices = []
        self.temp_choices = []
        self.log = []
        self._obj: pd.DataFrame = pandas_obj

    def play_log(self):
        if self.verbose:
            print(self.log[-1])

    def add_log(self, log: str):
        self.log.append(log)

    def search(self, query):
        # checks on query
        if query:
            return self.simple_search(query)
        else:
            return self._obj

    def simple_search(self, query):
        description_search = 'Description.str.contains("{}")'
        query_string = ' and '.join([description_search.format(item.strip().upper()) for item in query.split(',')])
        return self._obj.query(query_string)
    

    def choose(self, query: str):
        query = query.strip()
        if query.isnumeric():
            choice = self._obj.loc[int(query)]
            self.choices.append(choice)
            self.add_log(f'Added choice {choice} in list')
            self.play_log()
        else:
            print("Choice must be a number.")


    def reset(self):
        self.temp_choices = self.choices
        self.choices.clear()
        self.add_log("List of choices is empty.")
        self.play_log()
        

if __name__ == '__main__':
    pass


