#imports all necessary packages
import yfinance as yf
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog

#a new class for the actual results of the scan
results_open = False
class Results:

    def __init__(self):
        #read file with stocks and industries on it
        file = pd.read_csv(r'C:\Users\colea\Downloads\Sectors\NN_Sectors.csv')
        #create tk object and initialize values
        global results_open
        results_open = True
        self.root = tk.Tk()
        self.root.geometry("1200x675")
        self.root.title("Stocks")

        #this is the main grid frame
        self.grid = tk.Frame(self.root, bd = 1, relief =  'solid', background = '#454545')
        self.grid.columnconfigure(0, weight = 1)
        self.grid.bind("<MouseWheel>", self.scrollbar)

        #this is the first canvas that holds the scrollbar
        self.canvas1 = tk.Canvas(self.grid, background = '#454545', width = 1200, height = 670)
        self.canvas1.bind("<MouseWheel>", self.scrollbar)

        #initialize the scrollbar
        self.scroll = tk.Scrollbar(self.grid, orient = tk.VERTICAL, command = self.canvas1.yview)
        self.canvas1.configure(yscrollcommand = self.scroll.set)

        #this is the second canvas that holds the labels of the stock stats
        self.canvas2 = tk.Canvas(self.canvas1, background = '#454545')
        self.canvas2.bind("<MouseWheel>", self.scrollbar)

        #puts the second canvas in the first
        self.canvas1.create_window((0, 0), window = self.canvas2)

        #puts all the stocks in the selected industries in a list
        global finalStocks
        finalStocks = []
        for industry in added:
            filtered = file[file['Sectors'] == industry]
            stocks = filtered['Stocks'].tolist()
            finalStocks += stocks

        #adds the labels for the stock stats
        self.ticker = tk.Label(self.canvas2, text = "Ticker", font = ('Arial', '14'), width = 9)
        self.ticker.grid(row = 0, column = 0)
        self.indusName = tk.Label(self.canvas2, text = "Sector", font = ('Arial', '14'), width = 20)
        self.indusName.grid(row = 0, column = 1, pady = 1, padx = 1)

        global options
        options = ["Price", "Change", "% Change", "PE Ratio", "Volume", "Other"]
        self.option = ttk.Combobox(self.canvas2, values = options, width = 9, font = ('Arial', '14'))
        self.option.grid(row = 0, column = 2, padx = 1, pady = 1)

        self.option.bind("<KeyRelease>", self.addColumn)

        #automates ticker and industry labels
        global y
        y = 2
        x = 1
        for i in finalStocks:
            #labels for the stock ticker
            self.label = tk.Label(self.canvas2, text = i, font = ('Arial', '14'), width = 9)
            self.label.grid(row = x, column = 0, pady = 1, padx = 1)
            self.label.bind("<MouseWheel>", self.scrollbar)

            row = file[file['Stocks'] == i]
            final = (row['Sectors'].tolist())

            #labels for the stock's industry
            self.label2 = tk.Label(self.canvas2, text = final[0], font = ('Arial', '14'), width = 20)
            self.label2.grid(row = x, column = 1, pady = 1, padx = 1)
            self.label2.bind("<MouseWheel>", self.scrollbar)

            x += 1

        #adds the scroll functionality
        self.canvas2.bind("<Configure>", lambda event: self.canvas1.configure(scrollregion = self.canvas1.bbox("all")))

        #adds all the elements to the screen
        self.grid.pack()
        self.canvas1.grid(row=0, column=0, sticky="nsew", padx = 1, pady = 1)
        self.scroll.grid(row=0, column=99, sticky="ns")

        #sets results_open variable to false on closing
        self.root.protocol("WM_DELETE_WINDOW", self.exitWindow)

        #tells the user how many results there are
        #messagebox.askokcancel(title = "Results:", message = f"There are {finalStocks.__len__()} stocks that fit your search.")

        #brings the window back into focus after the message box
        #self.root.lift()

        self.root.mainloop()

    #makes the scrolling appear on the screen
    def scrollbar(self, e):
            self.canvas1.yview_scroll(int(-1 * (e.delta / 120)), "units")

    #makes the window openable again after closing
    def exitWindow(self):
        global results_open
        results_open = False
        self.root.destroy()

    #function for adding a column
    def addColumn(self, e):
        if e.keysym == "Return":
            global y
            x = 1
            #when the user picks other
            if self.option.get() == "Other":
                #asks the user for their desired stat
                value = simpledialog.askstring("New Value", "What value do you want displayed? (Must be part of yfinance library)")
                if yf.Ticker('AAPL').info.get(value) != yf.Ticker('AAPL').info.get('g'):
                        for i in finalStocks:
                            stock = yf.Ticker(i)
                            #adding labels for new stats
                            self.label3 = tk.Label(self.canvas2, text = stock.info.get(value), font = ('Arial', '14'), width = 11)
                            self.label3.grid(row = x, column = y, pady = 1, padx = 1)
                            self.label3.bind("<MouseWheel>", self.scrollbar)
                            x += 1
                            #adding a delay so that the window doesn't freeze
                            self.root.update()
                            self.root.after(50)
                        #moving new things to the next column
                        self.option.grid(row = 0, column = y+1, padx = 1, pady = 1)
                        self.newLabel = tk.Label(self.canvas2, text = value.upper(), font = ('Arial', '14'), width = 11)
                        self.newLabel.grid(row = 0, column = y, padx = 1, pady = 1)
            #when the user picks price
            elif self.option.get() == "Price":
                for i in finalStocks:
                    stock = yf.Ticker(i)
                    #this finds the middle between the bid and ask to determine an accurate price
                    #adding new labels
                    try:
                        self.label3 = tk.Label(self.canvas2, text = round(stock.info.get('bid') + stock.info.get('ask'), 2) / 2, font = ('Arial', '14'), width = 11)
                    except:
                        self.label3 = tk.Label(self.canvas2, text = "N/A", font = ('Arial', 14), width = 11)
                    self.label3.grid(row = x, column = y, pady = 1, padx = 1)
                    self.label3.bind("<MouseWheel>", self.scrollbar)
                    x += 1
                    #adding a delay so that the window doesn't freeze
                    self.root.update()
                    self.root.after(50)
                #moving new things to next column
                self.option.grid(row = 0, column = y+1, padx = 1, pady = 1)
                self.newLabel = tk.Label(self.canvas2, text = "Price", font = ('Arial', '14'), width = 11)
                self.newLabel.grid(row = 0, column = y, padx = 1, pady = 1)
                y += 1
                #taking price out of the drop down menu
                try:
                    options.pop(options.index("Price"))
                    self.option['values'] = options
                except:
                    messagebox.askokcancel(title = "Recurring Value", message = "Price is already on the screen. It will be added again.")
            #when the user picks change
            elif self.option.get() == "Change":
                for i in finalStocks:
                    stock = yf.Ticker(i)
                    #subtracting the open from the price
                    open = stock.info.get('open')
                    try:
                        price = (stock.info.get('bid') + stock.info.get('ask')) / 2
                        change2 = round((open - price), 2)
                        #determining the color of the text based on if the stock is up or down
                        if change2 > 0:
                            color = "green"
                        elif change2 < 0:
                            color = "red"
                        else:
                            color = "black"
                    except:
                        change2 = "N/A"
                        color = "black"
                    #adding labels
                    try:
                        self.label3 = tk.Label(self.canvas2, text = change2, font = ('Arial', '14'), width = 11, fg = color)
                    except:
                        self.label3 = tk.Label(self.canvas2, text = "N/A", font = ('Arial', 14), width = 11)
                    self.label3.grid(row = x, column = y, pady = 1, padx = 1)
                    self.label3.bind("<MouseWheel>", self.scrollbar)
                    x += 1
                    #adding a delay so that the window doesn't freeze
                    self.root.update()
                    self.root.after(50)

                #moving new things to the next column
                self.option.grid(row = 0, column = y+1, padx = 1, pady = 1)
                self.newLabel = tk.Label(self.canvas2, text = "Change", font = ('Arial', '14'), width = 11)
                self.newLabel.grid(row = 0, column = y, padx = 1, pady = 1)
                y += 1
                #taking change out of the drop down menu
                try:
                    options.pop(options.index("Change"))
                    self.option['values'] = options
                except:
                    messagebox.askokcancel(title = "Recurring Value", message = "Change is already on the screen. It will be added again.")
            #when the user picks %change
            elif self.option.get() == "% Change":
                for i in finalStocks:
                    stock = yf.Ticker(i)
                    #finding the percentage of change so far for the day
                    open = stock.info.get('open')
                    try:
                        price = (stock.info.get('bid') + stock.info.get('ask')) / 2
                        change = round((open - price) / price, 2)
                        #determining the color of the text based on if the stock is up or down
                        if change > 0:
                            color = "green"
                        elif change < 0:
                            color = "red"
                        else:
                            color = "black"
                    except:
                        change = "N/A"
                        color = "black"
                    #adding labels
                    try:
                        self.label3 = tk.Label(self.canvas2, text = f"{change} %", font = ('Arial', '14'), width = 11, fg = color)
                    except:
                        self.label3 = tk.Label(self.canvas2, text = "N/A", font = ('Arial', 14), width = 11)
                    self.label3.grid(row = x, column = y, pady = 1, padx = 1)
                    self.label3.bind("<MouseWheel>", self.scrollbar)
                    x += 1
                    #adding a delay so that the window doesn't freeze
                    self.root.update()
                    self.root.after(50)
                #moving new things to the next column
                self.option.grid(row = 0, column = y+1, padx = 1, pady = 1)
                self.newLabel = tk.Label(self.canvas2, text = "% Change", font = ('Arial', '14'), width = 11)
                self.newLabel.grid(row = 0, column = y, padx = 1, pady = 1)
                y += 1
                #removing % change from the drop down menu
                try:
                    options.pop(options.index("% Change"))
                    self.option['values'] = options
                except:
                    messagebox.askokcancel(title = "Recurring Value", message = "% Change is already on the screen. It will be added again.")
            #when the user picks PE Ratio
            elif self.option.get() == "PE Ratio":
                for i in finalStocks:
                    stock = yf.Ticker(i)
                    #adding new labels
                    try:
                        self.label3 = tk.Label(self.canvas2, text = round(stock.info.get('forwardPE'), 2), font = ('Arial', '14'), width = 11)
                    except:
                        self.label3 = tk.Label(self.canvas2, text = "N/A", font = ('Arial', 14), width = 11)
                    self.label3.grid(row = x, column = y, pady = 1, padx = 1)
                    self.label3.bind("<MouseWheel>", self.scrollbar)
                    x += 1
                    #adding a delay so that the window doesn't freeze
                    self.root.update()
                    self.root.after(50)
                #moving new things to the next column
                self.option.grid(row = 0, column = y+1, padx = 1, pady = 1)
                self.newLabel = tk.Label(self.canvas2, text = "PE Ratio", font = ('Arial', '14'), width = 11)
                self.newLabel.grid(row = 0, column = y, padx = 1, pady = 1)
                y += 1
                #removing PE Ratio from the drop down menu
                try:
                    options.pop(options.index("PE Ratio"))
                    self.option['values'] = options
                except:
                    messagebox.askokcancel(title = "Recurring Value", message = "PE Ratio is already on the screen. It will be added again.")
            #when the user selects volume
            elif self.option.get() == "Volume":
                for i in finalStocks:
                    stock = yf.Ticker(i)
                    #adding new labels
                    try:
                        self.label3 = tk.Label(self.canvas2, text = round(stock.info.get('volume'), 2), font = ('Arial', '14'), width = 11)
                    except:
                        self.label3 = tk.Label(self.canvas2, text = "N/A", font = ('Arial', 14), width = 11)
                    self.label3.grid(row = x, column = y, pady = 1, padx = 1)
                    self.label3.bind("<MouseWheel>", self.scrollbar)
                    x += 1
                    #adding a delay so that the window doesn't freeze
                    self.root.update()
                    self.root.after(50)
                #moving new things over
                self.option.grid(row = 0, column = y+1, padx = 1, pady = 1)
                self.newLabel = tk.Label(self.canvas2, text = "Volume", font = ('Arial', '14'), width = 11)
                self.newLabel.grid(row = 0, column = y, padx = 1, pady = 1)
                y += 1
                #removing volume from the drop down menu
                try:
                    options.pop(options.index("Volume"))
                    self.option['values'] = options
                except:
                    messagebox.askokcancel(title = "Recurring Value", message = "Volume is already on the screen. It will be added again.")
            #when the user enters something unavailable in the drop down menu
            else:
                messagebox.askokcancel(title = "Error", message = f'{self.option.get()} is not an option. Try using "Other"')

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



