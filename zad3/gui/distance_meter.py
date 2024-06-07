# GUI setup
import tkinter
from tkinter import Tk, ttk

import numpy as np

from zad3.api import signal_conversion, operations
from zad3.gui.filter_creator import filter_creator_frame
from zad3.gui.signal_frame import SignalGenerator

operations_window = None
zad3_window = None

root = Tk()
root.title("CPS - Zadanie 3 | Correlation distance meter")
main_frame = ttk.Frame(root, padding="10")



########################################

main_frame.pack()
root.mainloop()
