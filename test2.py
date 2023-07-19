import tkinter as tk
import pandas as pd

#a new class for the actual results of the scan
results_open = False
class Results:

    def __init__(self):
        industries = ['Utilities', "Energy"]
        file = pd.read_csv(r'C:\Users\colea\Downloads\Sectors\NN_Sectors.csv')
        #create tk object and initialize values
        global results_open
        results_open = True
        self.root = tk.Tk()
        self.root.geometry("1200x675")
        self.root.title("Stocks")

        self.grid = tk.Frame(self.root, bd = 1, relief =  'solid', background = '#454545')
        self.grid.columnconfigure(0, weight = 1)

        for industry in industries:
            filtered = file[file['Sectors'] == industry]
            stocks = filtered['Stocks'].tolist()
        x = 0
        for i in stocks:
            self.label = tk.Label(self.grid, text = i, font = ('Arial', '14'), width = 7)
            self.label.grid(row = x, column = 0, pady = 1, padx = 1)

            row = file[file['Stocks'] == i]
            final = (row['Sectors'].tolist())

            self.label2 = tk.Label(self.grid, text = final[0], font = ('Arial', '14'), width = 7)
            self.label2.grid(row = x, column = 1, pady = 1, padx = 1)
            x += 1

        self.grid.pack()

        self.root.mainloop()


Results()




