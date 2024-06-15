# GUI setup
import tkinter
from tkinter import Tk, ttk

from zad4.api.correlation_distance_meter import CorrelationDistanceMeter

root = Tk()
root.title("CPS - Zadanie 3 | Correlation distance meter")
main_frame = ttk.Frame(root, padding="10")

# receiver parameters
ttk.Label(main_frame, text="Receiver").pack()
ttk.Label(main_frame, text="Signal period").pack()
receiver_signal_period_entry = ttk.Entry(main_frame)
receiver_signal_period_entry.insert(0, "1")
receiver_signal_period_entry.pack()

ttk.Label(main_frame, text="Sampling frequency").pack()
receiver_sampling_frequency_entry = ttk.Entry(main_frame)
receiver_sampling_frequency_entry.insert(0, "100")
receiver_sampling_frequency_entry.pack()

ttk.Label(main_frame, text="Buffers length").pack()
receiver_buffers_length_entry = ttk.Entry(main_frame)
receiver_buffers_length_entry.insert(0, "200")
receiver_buffers_length_entry.pack()

ttk.Label(main_frame, text="Report period").pack()
receiver_report_period_entry = ttk.Entry(main_frame)
receiver_report_period_entry.insert(0, "0.5")
receiver_report_period_entry.pack()

ttk.Separator(main_frame, orient='horizontal').pack(fill='x')

# transmitter parameters
ttk.Label(main_frame, text="Transmitter").pack()
ttk.Label(main_frame, text="Measurments no").pack()
transmitter_measurments_no_entry = ttk.Entry(main_frame)
transmitter_measurments_no_entry.insert(0, "10")
transmitter_measurments_no_entry.pack()

ttk.Label(main_frame, text="Time unit").pack()
transmitter_time_unit_entry = ttk.Entry(main_frame)
transmitter_time_unit_entry.insert(0, "0.01")
transmitter_time_unit_entry.pack()

ttk.Label(main_frame, text="Real object speed").pack()
transmitter_real_object_speed_entry = ttk.Entry(main_frame)
transmitter_real_object_speed_entry.insert(0, "0.75")
transmitter_real_object_speed_entry.pack()

ttk.Label(main_frame, text="Signal speed abstract").pack()
transmitter_signal_speed_abstract_entry = ttk.Entry(main_frame)
transmitter_signal_speed_abstract_entry.insert(0, "100")
transmitter_signal_speed_abstract_entry.pack()

ttk.Separator(main_frame, orient='horizontal').pack(fill='x')

# distance meter
def start_distance_meter():
    data_table.delete(*data_table.get_children())
    transmitter_measurments_no = int(transmitter_measurments_no_entry.get())
    transmitter_time_unit = float(transmitter_time_unit_entry.get())
    transmitter_real_object_speed = float(transmitter_real_object_speed_entry.get())
    transmitter_signal_speed_abstract = float(transmitter_signal_speed_abstract_entry.get())
    receiver_signal_period = float(receiver_signal_period_entry.get())
    receiver_sampling_frequency = float(receiver_sampling_frequency_entry.get())
    receiver_buffers_length = float(receiver_buffers_length_entry.get())
    receiver_report_period = float(receiver_report_period_entry.get())

    distance_meter = CorrelationDistanceMeter(transmitter_measurments_no, transmitter_time_unit,
                                              transmitter_real_object_speed, transmitter_signal_speed_abstract,
                                              receiver_signal_period, receiver_sampling_frequency,
                                              receiver_buffers_length, receiver_report_period)

    original_distances = distance_meter.original_distances()
    receiver_distances = distance_meter.receiver_distances()
    t_values = distance_meter.get_receiver_t_values()
    for i in range(transmitter_measurments_no):
        data_table.insert("", "end", values=(t_values[i], original_distances[i], receiver_distances[i], abs(original_distances[i] - receiver_distances[i])))

    print("Completed")

btnStart = ttk.Button(main_frame, text="Start", command=lambda: start_distance_meter())
btnStart.pack()

ttk.Separator(main_frame, orient='horizontal').pack(fill='x')

# data table

ttk.Label(main_frame, text="Transmitter & Receiver data").pack()

data_table = ttk.Treeview(main_frame)
data_table["columns"] = ("Time", "Transmitter distance", "Receiver distance", "Error")
data_table.column("#0", width=0, stretch=tkinter.NO)
data_table.column("Time", anchor=tkinter.W, width=50)
data_table.column("Transmitter distance", anchor=tkinter.W, width=150)
data_table.column("Receiver distance", anchor=tkinter.W, width=150)
data_table.column("Error", anchor=tkinter.W, width=150)

data_table.heading("#0", text="", anchor=tkinter.W)
data_table.heading("Time", text="Time [s]", anchor=tkinter.W)
data_table.heading("Transmitter distance", text="Transmitter distance", anchor=tkinter.W)
data_table.heading("Receiver distance", text="Receiver distance", anchor=tkinter.W)
data_table.heading("Error", text="Error", anchor=tkinter.W)

data_table.pack()


########################################

main_frame.pack()
root.mainloop()