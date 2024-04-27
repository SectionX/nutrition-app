################################################################
#This software is developed by <developer name> for <development reason>
#
#It's released under <LICENSE NAME> license.

from .src.model import connect
from .src.terminal import Terminal
from .src.gui import initialize_window

from argparse import ArgumentParser

import pandas as pd

parser = ArgumentParser('Nutrition Data', description='Count calories and nutrition of various foods and recipes.')
parser.add_argument('-t', '--terminal', action='store_true', help='Launches a REPL session')
parser.add_argument('-g', '--gui', action='store_true', help='Launches a graphical interface')
parser.add_argument('-w', '--worksheet', action='store_true', help='Loads the database to a worksheet application')


def launch_worksheet(db: pd.DataFrame):
    import subprocess
    import os
    file = 'foodDB.xlsx'
    try:
        db.to_excel(file)
        stats = os.stat(file)
        process = subprocess.check_call(args=['libreoffice', './foodDB.xlsx'])
    except Exception as e:
        print(e)

def main():
    args = parser.parse_args()
    if args.terminal:
        Terminal.main_loop(connect())
    if args.gui:
        root = initialize_window()
        root.mainloop()
    if args.worksheet:
        launch_worksheet(connect())

if __name__ == '__main__':
    main()