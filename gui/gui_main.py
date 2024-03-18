from tkinter import Tk, ttk, Toplevel

import plot_creation_frame
from operations_frame import OperationsFrame
from signal_info_frame import SignalInfoFrame

root = Tk()
root.title("CPS - Projekt")
root.geometry("1000x800")
notebook = ttk.Notebook(root, padding=10)
notebook.pack(fill='both', expand=True)

page1 = ttk.Frame(notebook, padding=10)
notebook.add(page1, text="Generowanie sygnału")

pcs = plot_creation_frame.PlotCreationFrame(page1)
pcs.frame.grid(column=0, row=0)


page2 = ttk.Frame(notebook, padding=10)
notebook.add(page2, text="Operacje na sygnałach")

pcs1 = plot_creation_frame.PlotCreationFrame(page2)
pcs1.frame.grid(column=0, row=0)
pcs2 = plot_creation_frame.PlotCreationFrame(page2)
pcs2.frame.grid(column=0, row=1)

of = OperationsFrame(page2, pcs1, pcs2)
of.frame.grid(column=0, row=2)

root.mainloop()