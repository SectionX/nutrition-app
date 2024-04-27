import tkinter as tk
from tkinter import ttk
import sys

from .model import connect
from .controller import Controller

import pandas as pd


class MainWindow(tk.Tk):

    def __init__(self):
        super(MainWindow, self).__init__(className=' Nutrition App ')
        self.title = "Nutrition App" 
        self.geometry('1000x700')
        self.hotkeys()

    def hotkeys(self):
        self.bind('<Alt-q>', lambda e: sys.exit(0))

    
class SearchBar(tk.Entry):
    def __init__(self, master, *args, **kwargs):
        super(SearchBar, self).__init__(master, *args, **kwargs)
        self._data_widget = None
        self.hotkeys()
        self.pack()

    def hotkeys(self):
        self.bind('<Return>', lambda e: self.search(e))
        self.bind('<comma>', lambda e: self.search(e))

    def bind_data_widget(self, widget):
        self._data_widget = widget
        return self

    def search(self, *args, **kwargs):
        if not self._data_widget:
            print('Use the bind_data_widget method to bind a widget to the search bar')
        if not hasattr(self._data_widget, 'search'):
            print('Widget needs to implement a search method to accept the text from the search bar.') 
        inp = self.get()
        self._data_widget.search(inp)

    

class DataTable(ttk.Treeview):
    def __init__(self, master, controller: Controller, *args, **kwargs):
        self.controller = controller
        self._data = controller.db
        self._current_data = controller.db
        self._columns = ['Index'] + controller.db.columns.to_list()
        self._current_selection: list
        super(DataTable, self).__init__(master, columns=self._columns)
        self['show'] = 'headings'
        self.hotkeys()
        self.pack()
        self._populate_columns()
        self._populate_table()
    
    def hotkeys(self):
        self.bind('<Control-a>', lambda e: self.select())

    def bind_output_widget(self, widget):
        self._data_widget = widget
        return self

    def reset(self, data=None):
        self._clear_table()
        self._populate_table(data)

    def _populate_columns(self):
        for column in self._columns:
            self.heading(column, text=column)

    def _populate_table(self, data=None):
        if data is None:
            data = self._data

        for i, row in data.iterrows():
            self.insert('', tk.END, values=[i] + row.to_list())

    def _clear_table(self):
        self.delete(*self.get_children())

    def select(self):
        selection = [self.item(id) for id in self.selection()]
        self._data_widget.add(selection)

    def search(self, _input: str):
        self.controller.parse('search ' + _input)
        result = self.controller.run()
        self.reset(result)
        

class Selection(tk.Frame):

    DESCRIPTION = 2
    CALORIES = 12
    PROTEIN = 18
    CARBS = 8
    FAT = 29
    GRAMS = -1
    PROTEIN_CALS = 4
    CARBS_CALS = 4
    FAT_CALS = 9

    def __init__(self, master):
        super(Selection, self).__init__(master)
        button_frame = tk.Frame(master)
        self.button_reset = tk.Button(button_frame, command=self.destroy, text='Reset')
        self.button_reset.grid(row=0, column=0)
        self.button_calculate = tk.Button(button_frame, command=self.calculate, text='Calculate')
        self.button_calculate.grid(row=0, column=1)
        button_frame.pack()
        self.result_frame = None
        self._row = 0
        self._column = 0
        self._items = []
        self.hotkeys()
        self.pack()

    def hotkeys(self):
        self.bind('<Control-d>', lambda e: self.destroy())

    def calculate(self):
        if self.result_frame: self.result_frame.destroy()
        data = {
        'cals' : 0,
        'protein' : 0,
        'carbs' : 0,
        'fat' : 0,
        'grams': 0,
        }


        _items = [item['values'] for item in self._items]
        grams = [v.get() or 0 for k, v in self.children.items() if k.startswith('grams_')]
        items = [a + [b] for a, b in zip(_items, grams)]
        
        for item in items:
            grams = float(item[self.GRAMS])
            data['grams'] += grams
            data['cals'] += float(item[self.CALORIES]) * (grams/100)
            data['protein'] += float(item[self.PROTEIN]) * (grams/100)
            data['carbs'] += float(item[self.CARBS]) * (grams/100)
            data['fat'] += float(item[self.FAT]) * (grams/100)

        data['protein_cals'] = data['protein'] * self.PROTEIN_CALS
        data['protein_%'] = data['protein_cals'] / data['cals']
        data['carbs_cals'] = data['carbs'] * self.CARBS_CALS
        data['carbs_%'] = data['carbs_cals'] / data['cals']
        data['fat_cals'] = data['fat'] * self.FAT_CALS
        data['fat_%'] = data['fat_cals'] / data['cals']

        self.result_frame = tk.Frame(self.master, name='result-frame')
        grams = tk.Label(self.result_frame, text=f"Grams: {data['grams']}")
        grams.grid(row=0, column=0)
        calories = tk.Label(self.result_frame, text=f"Calories: {data['cals']} g")
        calories.grid(row=0, column=1)
        protein = tk.Label(self.result_frame, text=f"Protein: {data['protein']} g")
        protein.grid(row=1, column=0)
        protein_cals = tk.Label(self.result_frame, text=f"{data['protein_cals']} kcal")
        protein_cals.grid(row=1, column=1)
        protein_percent = tk.Label(self.result_frame, text=f"{data['protein_%'] * 100:.2f}%")
        protein_percent.grid(row=1, column=2)
        carbs = tk.Label(self.result_frame, text=f"Carbs: {data['carbs']} g")
        carbs.grid(row=2, column=0)
        carbs_cals = tk.Label(self.result_frame, text=f"{data['carbs_cals']} kcal")
        carbs_cals.grid(row=2, column=1)
        carbs_percent = tk.Label(self.result_frame, text=f"{data['carbs_%'] * 100:.2f}%")
        carbs_percent.grid(row=2, column=2)
        fat = tk.Label(self.result_frame, text=f"Fat: {data['fat']} g")
        fat.grid(row=3, column=0)
        fat_cals = tk.Label(self.result_frame, text=f"{data['fat_cals']} kcal")
        fat_cals.grid(row=3, column=1)
        fat_percent = tk.Label(self.result_frame, text=f"{data['fat_%'] * 100:.2f}%")
        fat_percent.grid(row=3, column=2)
        self.result_frame.pack()


    def destroy(self):
        if self.result_frame:
            self.result_frame.destroy()
        while self.children:
            item = self.children.popitem()
            item[1].destroy()
            self._row=0

    def _remove(self, row):
        def remove(self=self, row=row):
            del self._items[row]
            self.destroy()
            self.add(self._items, reset=True)
            print(len(self._items))
        return remove


    def add(self, items: list, reset=False):
        if not reset:
            self._items.extend(items)
        if reset:
            self._row = 0
        for item in items:
            if item == None: 
                continue
            self._column = 0
            item_frame = tk.Frame(self, name=f'data_{self._row}')
            label_description = tk.Label(item_frame, name='description', text=item['values'][self.DESCRIPTION], justify='left')
            label_description.grid(row=0, column=0)
            label_calories = tk.Label(item_frame, name='calories', text=item['values'][self.CALORIES], justify='left')
            label_calories.grid(row=0, column=1)
            label_protein = tk.Label(item_frame, name='protein', text=item['values'][self.PROTEIN], justify='left')
            label_protein.grid(row=0, column=2)
            label_carbs = tk.Label(item_frame, name='carbs', text=item['values'][self.CARBS], justify='left')
            label_carbs.grid(row=0, column=3)
            label_fat = tk.Label(item_frame, name='fat', text=item['values'][self.FAT], justify='left')
            label_fat.grid(row=0, column=4)

            entry = tk.Entry(self, name=f'grams_{self._row}')
            entry.insert(tk.END, '100')
            callback = self._remove(self._row)
            button = tk.Button(self, text='X', command=callback)
            button.grid(row=self._row, column=self._column)
            self._column += 2
            item_frame.grid(row=self._row, column=self._column)
            self._column += 1
            entry.grid(row=self._row, column=self._column)
            self._column += 1
            self._row += 1
            



def initialize_window():

    root = MainWindow()
    search_bar = SearchBar(root)
    table = DataTable(root, Controller('gui'))
    selection = Selection(root)

    table.bind_output_widget(selection)
    search_bar.bind_data_widget(table)
    search_bar.focus()
    return root


    

    







def old():
    controller = Controller(debug=True)



    root = tk.Tk(className=' Nutrition Data ')
    root.title = 'Nutrition'
    root.geometry('1000x700')


    # treeview and add button
    def select(): 
        items = [tv.item(id)['values'] for id in tv.selection()]
        print(*items)
        return items

    def populate(data: pd.DataFrame):
        for i, row in data.iterrows():
            row = row.to_list()
            tv.insert('', tk.END, values=[i]+row)


    current_search_view = controller.db
    def search(event = '', view: pd.DataFrame = current_search_view):
        global current_search_view
        global events

        print(event)
        query = search_bar.get()
        print(query)

        print(f"Searching among {len(current_search_view)} entries.")

        if not query:
            current_search_view = controller.db
            result = current_search_view

        else:
            result = controller.search(query)
            current_search_view = result

        tv.delete(*tv.get_children())
        for i, row in result.iterrows():
            row = row.to_list()
            tv.insert('', tk.END, values=[i]+row)


    button_populate = tk.Button(root, text="Search", command=lambda: search('bypass'))
    button_populate.pack()

    search_bar = tk.Entry(root)
    search_bar.pack()

    columns = ['index'] + controller.db.columns.to_list()
    tv = ttk.Treeview(root, columns=columns)
    tv['show'] = 'headings'
    for column in columns:
        tv.heading(column, text=column)
    tv.pack()
    populate(controller.db)

    button_add = tk.Button(root, text="Add", command=select)
    button_add.pack()

    search_bar.bind('<comma>', lambda e: search(e))
    search_bar.bind('<Return>', lambda e: search(e))
    search_bar.focus()