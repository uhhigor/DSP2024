from tkinter import Tk, ttk

import plot_creation_frame
from operations_frame import OperationsFrame

root = Tk()
root.title("CPS - Projekt")
notebook = ttk.Notebook(root, padding=10)
notebook.pack(fill='both', expand=True)

page1 = ttk.Frame(notebook, padding=10)
notebook.add(page1, text="Generowanie sygnału")

pcs = plot_creation_frame.PlotCreationFrame(page1, "Sygnał")
pcs.frame.grid(column=0, row=0)

page2 = ttk.Frame(notebook, padding=10)
notebook.add(page2, text="Operacje na sygnałach")

pcs1 = plot_creation_frame.PlotCreationFrame(page2, "Sygnał 1")
pcs1.frame.grid(column=0, row=0)
pcs2 = plot_creation_frame.PlotCreationFrame(page2, "Sygnał 2")
pcs2.frame.grid(column=0, row=1)

of = OperationsFrame(page2, pcs1, pcs2)
of.frame.grid(column=0, row=2)

page3 = ttk.Frame(notebook, padding=10)
notebook.add(page3, text="Konwersja")

pcs3 = plot_creation_frame.PlotCreationFrame(page3, "Sygnał")
pcs3.frame.grid(column=0, row=0)

root.mainloop()
