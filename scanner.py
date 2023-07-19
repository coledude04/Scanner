#imports all necessary packages
import yfinance as yf
import pandas as pd
import tkinter as tk
from tkinter import messagebox

#a new class for the actual results of the scan
results_open = False
class Results:

    def __init__(self):
        #create tk object and initialize values
        global results_open
        results_open = True
        self.root = tk.Tk()
        self.root.geometry("1200x675")
        self.root.title("Stocks")

        self.grid = tk.Frame(self.root, bd = 1, relief =  'solid', background = '#454545')
        self.grid.columnconfigure(0, weight = 1)

        self.stock1 = tk.Label(self.grid, text = "Stock 1", font = ('Arial', '14'))
        self.stock1.grid(row = 0, column = 0, pady = 1, padx = 1)
        self.stock2 = tk.Label(self.grid, text = "Stock 2", font = ('Arial', '14'))
        self.stock2.grid(row = 1, column = 0, pady = 1, padx = 1)
        self.stock3 = tk.Label(self.grid, text = "Stock 3", font = ('Arial', '14'))
        self.stock3.grid(row = 2, column = 0, pady = 1, padx = 1)

        self.indus1 = tk.Label(self.grid, text = "Industry 1", font = ('Arial', '14'))
        self.indus1.grid(row = 0, column = 1, pady = 1, padx = 1)
        self.indus2 = tk.Label(self.grid, text = "Industry 2", font = ('Arial', '14'))
        self.indus2.grid(row = 1, column = 1, pady = 1, padx = 1)
        self.indus3 = tk.Label(self.grid, text = "Industry 3", font = ('Arial', '14'))
        self.indus3.grid(row = 2, column = 1, pady = 1, padx = 1)

        self.grid.pack()

class StartGUI:

    def __init__(self):
        #create tk object and initialize values
        self.root = tk.Tk()
        self.root.geometry("800x450")
        self.root.title("Scanner")

        #create label
        self.welcome = tk.Label(self.root, text = "Stock Scanner", font = ('Arial', '22'))
        self.welcome.pack(pady = (5, 0))

        #create title
        self.mainTitle = tk.Label(self.root, text = "Industries", font = ('Arial', "18"), width = '40')
        self.mainTitle.pack(pady = 5)

        #create textbox
        self.search = tk.Entry(self.root, font = ('Arial', '16'),)
        self.search.pack(pady = (5, 0))

        #function to update the listbox
        global update
        def update(data):
            #clear searchbox
            self.searchFill.delete(0, tk.END)
            #add all items to searchbox
            for item in data:
                self.searchFill.insert(tk.END, item)

        self.searchFill = tk.Listbox(self.root, width = '40')
        self.searchFill.pack(pady = 5)

        #a list with all the industries
        global industries
        industries = ["Healthcare", "Basic Materials", "Financial Services", "Industrials", "Consumer Cyclical", "Real Estate", 
                      "Consumer Defensive", "Technology", "Utilities", "Energy", "Communication Services", "Industrial Goods", "Financial"]

        #add industries to listbox
        update(industries)

        #bind listbox to searchbox
        self.searchFill.bind("<<ListboxSelect>>", self.fillout)

        #create the searchbox bindings
        self.search.bind("<KeyRelease>", self.shortcut)
        self.search.bind("<KeyRelease>", self.check, add = "+")

        #create a list of added industries
        self.add_indus = tk.Label(self.root, font = ('Arial', 8), width = 80)
        self.add_indus.pack(pady = 5)

        #create the button to add a search parameter
        self.addBtn = tk.Button(self.root, text = "Add Parameter", font = ('Arial', '14'), height = '1', command = self.addVar)
        self.addBtn.pack(pady =(0, 10))

        # Create a frame to hold the buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        #create the final search button
        self.searchBtn = tk.Button(self.frame, text = "Search", font = ('Arial', '18'), height = '1', command = self.searcher)
        self.searchBtn.pack(side = tk.LEFT, padx = (0, 2))

        #create the clear search button
        self.clearSearch = tk.Button(self.frame, text = "Clear Search", font = ('Arial', '18'), height = '1', command = self.clearer)
        self.clearSearch.pack(side = tk.LEFT, padx = (2, 0))

        #confirm that the user wants to quit the program
        self.root.protocol("WM_DELETE_WINDOW", self.exitWindow)

        #create the list of all the added industries
        global added
        added = []

        self.root.mainloop()

    #function to check entry vs listbox
    def check(self, e):
        #gets search box entry
        typed = self.search.get()
        if typed == '':
            #sets listbox to all industries if the nothing is typed
            data = industries
        else:
            data = []
            #cycles through industries that match what is typed
            for item in industries:
                if typed.lower() in item.lower():
                    data.append(item)
        update(data)

    #fill out the searchbox
    def fillout(self, e):
        self.search.delete(0, tk.END)
        self.search.insert(0, self.searchFill.get(tk.ANCHOR))

    #runs the addVar if enter is pressed
    def shortcut(self, e):
        if e.keysym == "Return":
            self.addVar()
       
    #function on quitting window
    def exitWindow(self):
        if messagebox.askyesno(title = "Quit", message = "Are you sure you want to quit?"):
            self.root.destroy()

    #function for adding a search parameter
    def addVar(self):
        add = self.search.get()
        if add in industries and not add in added:
            added.append(add)
            global txt
            txt = "Added Industries: "
            self.search.delete(0, tk.END)
        #this part adds industries to a list that is displayed for the user to see
        try:
            for name in added:
                txt += name + ", "
            txt = txt[:-2]
            self.add_indus.config(text = txt)
        except:
            messagebox.askokcancel(title = "Error", message = "Not an option")

    #function for when the user wants to clear their search categories
    def clearer(self):
        global added
        added = []
        global txt
        txt = ""
        self.add_indus.config(text = txt)

    #function for searching after all parameters are added
    def searcher(self):
        if not results_open:
            Results()
        else:
            messagebox.askokcancel(title = "Error", message = "Already open")
#starts the program
StartGUI()



