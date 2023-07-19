import tkinter as tk

root = tk.Tk()

# Create a canvas
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame to hold the labels
frame = tk.Frame(canvas)

# Add labels to the frame
for i in range(100):
    label = tk.Label(frame, text=f"Label {i}")
    label.pack()

# Add the frame to the canvas
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

root.mainloop()




