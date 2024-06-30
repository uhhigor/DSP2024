# GUI setup
import tkinter
from tkinter import Tk, ttk

from zad3.api.correlation_distance_meter import CorrelationDistanceMeter

root = Tk()
root.title("CPS - Zadanie 3 | Correlation distance meter")
main_frame = ttk.Frame(root, padding="10")

# receiver parameters
ttk.Label(main_frame, text="Receiver").pack()
ttk.Label(main_frame, text="Signal period").pack()
receiver_signal_period_entry = ttk.Entry(main_frame)
receiver_signal_period_entry.insert(0, "1")
receiver_signal_period_entry.pack()
freq_label = ttk.Label(main_frame, text="Frequency: " + str(1 / float(receiver_signal_period_entry.get())) + " Hz")
freq_label.pack()
# update frequency label when signal period changes
receiver_signal_period_entry.bind("<FocusOut>", lambda e: freq_label.config(
    text="Frequency: " + str(1 / float(receiver_signal_period_entry.get())) + " Hz"))
ttk.Label(main_frame, text="Amplitude: 1").pack()

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

ttk.Label(main_frame, text="Real object speed").pack()
transmitter_real_object_speed_entry = ttk.Entry(main_frame)
transmitter_real_object_speed_entry.insert(0, "0.75")
transmitter_real_object_speed_entry.pack()

ttk.Label(main_frame, text="Signal speed abstract").pack()
transmitter_signal_speed_abstract_entry = ttk.Entry(main_frame)
transmitter_signal_speed_abstract_entry.insert(0, "100")
transmitter_signal_speed_abstract_entry.pack()

ttk.Separator(main_frame, orient='horizontal').pack(fill='x')

distance_meter = None


# distance meter
def start_distance_meter():
    global distance_meter, playing

    data_table.delete(*data_table.get_children())
    transmitter_measurments_no = int(transmitter_measurments_no_entry.get())
    transmitter_real_object_speed = float(transmitter_real_object_speed_entry.get())
    transmitter_signal_speed_abstract = float(transmitter_signal_speed_abstract_entry.get())
    receiver_signal_period = float(receiver_signal_period_entry.get())
    receiver_sampling_frequency = float(receiver_sampling_frequency_entry.get())
    receiver_buffers_length = float(receiver_buffers_length_entry.get())
    receiver_report_period = float(receiver_report_period_entry.get())

    if distance_meter is not None:
        distance_meter.__del__()
        playing = True
        btnAnim.config(text="STOP ANIMATION")

    distance_meter = CorrelationDistanceMeter(transmitter_measurments_no,
                                              transmitter_real_object_speed, transmitter_signal_speed_abstract,
                                              receiver_signal_period, receiver_sampling_frequency,
                                              receiver_buffers_length, receiver_report_period,
                                              fixed_time_checkbox.get())

    original_values, received_values, t_values, diff, shifts, speed = distance_meter.calculate()
    for i in range(len(t_values)):
        data_table.insert("", "end", values=(t_values[i], original_values[i], received_values[i], diff[i], shifts[i]))

    speedLabel.config(text="Calculated average speed: " + str(round(speed, 2)))


btnStart = ttk.Button(main_frame, text="Start", command=lambda: start_distance_meter())
btnStart.pack()

ttk.Separator(main_frame, orient='horizontal').pack(fill='x')

# data table

data_table = ttk.Treeview(main_frame)
data_table["columns"] = ("Time", "Real distance", "Calculated distance", "Error", "Shift")
data_table.column("#0", width=0, stretch=tkinter.NO)
data_table.column("Time", anchor=tkinter.W, width=50)
data_table.column("Real distance", anchor=tkinter.W, width=150)
data_table.column("Calculated distance", anchor=tkinter.W, width=150)
data_table.column("Error", anchor=tkinter.W, width=150)
data_table.column("Shift", anchor=tkinter.W, width=150)

data_table.heading("#0", text="", anchor=tkinter.W)
data_table.heading("Time", text="Time [s]", anchor=tkinter.W)
data_table.heading("Real distance", text="Real distance", anchor=tkinter.W)
data_table.heading("Calculated distance", text="Calculated distance", anchor=tkinter.W)
data_table.heading("Error", text="Error", anchor=tkinter.W)
data_table.heading("Shift", text="Shift", anchor=tkinter.W)

data_table.pack()

speedLabel = ttk.Label(main_frame, text="Calculated average speed: ")
speedLabel.pack()

########################################
# play button
playing = True


def switch_anim():
    global playing
    if distance_meter is not None:
        if playing:
            distance_meter.anim.event_source.stop()
            playing = False
            btnAnim.config(text="PLAY ANIMATION")
        else:
            distance_meter.anim.event_source.start()
            playing = True
            btnAnim.config(text="STOP ANIMATION")


btnAnim = ttk.Button(main_frame, text="STOP ANIMATION", command=lambda: switch_anim())
btnAnim.pack()

fixed_time_checkbox = tkinter.BooleanVar()
fixed_time_checkbox.set(True)
checkbox = ttk.Checkbutton(main_frame, text="FIXED TIME", variable=fixed_time_checkbox)
checkbox.pack()

main_frame.pack()
root.mainloop()
