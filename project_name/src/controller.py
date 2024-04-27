# terminal controller:

from .model import connect
import sys
import pandas as pd

search_keywords = ['search', 'choose']
command_keywords = ['reset', 'exit', 'help']
choice_keywords = ['choices']


class Controller:

    def __init__(self, view, model: pd.DataFrame = connect(), debug: bool=False):
        self.view = view
        self.db = model
        self.model = model.foods
        self.command: str = ''
        self.args: str = ''
        self.debug = debug

    def parse(self, user_input):
        model_keywords = ['search', 'choose', 'reset', 'choices']
        view_keywords = ['reset', 'exit', 'help']

        if not user_input:
            self.command = ''
            self.query = ''
            return

        tokens = user_input.split(" ")
        if tokens[0] in model_keywords + view_keywords:
            command = tokens[0]
            if len(tokens) > 1:
                args = " ".join(tokens[1:])
            else:
                args = ''
        else:
            command = 'search'
            args = user_input
        
        if self.debug:
            print(command, args, user_input)
        self.command = command
        self.query = args

    def run(self):
        if not self.command: return ''
        function: callable
        function = getattr(self, self.command)
        return function(self.query)

    def search(self, query, *args, **kwargs):
        return self.model.search(query)

    def choose(self, query, *args, **kwargs):
        return self.model.choose(query)

    def choices(self, *args, **kwargs):
        return self.model.choices

    def reset(self, *args, **kwargs):
        return self.model.reset()

    def help(self, *args, **kwargs):
        return self.view.help()

    def exit(self, *args, **kwargs):
        # Various operations
        sys.exit(0)

    def _(*args, **kwargs):
        return ''

    