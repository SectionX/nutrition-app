from .controller import Controller

class Terminal:

    @staticmethod
    def parse(user_input: str):
        search_keywords = ['search', 'choose']
        command_keywords = ['reset', 'exit', 'help']
        choice_keywords = ['choices']

        tokens = user_input.split(" ")
        if tokens[0] in search_keywords:
            command = tokens[0]
            args = " ".join(tokens[1:])
        elif tokens[0] in command_keywords:
            command = tokens[0]
            args = ''
        elif tokens[0] in choice_keywords:
            command = tokens[0]
            args = ''
        else:
            command = 'search'
            args = user_input
        
        return command, args

    @staticmethod
    def main_loop(db):
        result = db
        run = True
        controller = Controller(Terminal)
        while run:
            user_input = input('> ')
            controller.parse(user_input)
            result = controller.run()
            if type(result) == str and not result:
                pass
            else:
                print(result)