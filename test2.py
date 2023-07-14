import tkinter as tk

root = tk.Tk()

# Create labels in a grid
label1 = tk.Label(root, text="Label 1")
label2 = tk.Label(root, text="Label 2")
label3 = tk.Label(root, text="Label 3")

# Add labels to the grid
label1.grid(row=0, column=0)
label2.grid(row=1, column=0)
label3.grid(row=2, column=0)

# Create frames for each row
frame1 = tk.Frame(root, relief="solid", borderwidth=1)
frame2 = tk.Frame(root, relief="solid", borderwidth=1)
frame3 = tk.Frame(root, relief="solid", borderwidth=1)

# Add frames to the grid
frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=1, column=0, sticky="nsew")
frame3.grid(row=2, column=0, sticky="nsew")

root.mainloop()




