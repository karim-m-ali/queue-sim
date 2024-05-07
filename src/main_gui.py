"""
@file main_window.py
@author Karim M. Ali <https://github.com/kmuali>
@date May 07, 2024
"""
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from typing import Iterable
import queue_logic as ql
import process_logic as pl


RED_BG_ARGS = dict(bg='#d9a3a3', activebackground='#fbc5c5')
GREEN_BG_ARGS = dict(bg='#a9d3a3', activebackground='#cbf5c5')
BLUE_BG_ARGS = dict(bg='#a9a3d3', activebackground='#cbc5f5')
PAD_ARGS = dict(padx=8, pady=8)
LABEL_PAD_ARGS = dict(padx=(8, 0), pady=8)
PROCESS_FG = '#fff'
PROCESS_BG_DICT = {
        'P1':  'darkmagenta',
        'P2':  'darkcyan',
        'P3':  'darkorange',
        'P4':  'darkblue',
        'P5':  'darkred',
        'P6':  'darkgreen',
        'P7':  'magenta',
        'P8':  'mediumaquamarine',
        'P9':  'orange',
        'P10': 'steelblue',
        'P11': 'tomato',
        'P12': 'green',

}

class MainWindow(tk.Tk):
    def __init__(self, external_simulate):
        super().__init__()

        self.external_simulate = external_simulate

        self.title('QueueSim - Main')
        self.minsize(1280, 800) # WXGA - wide

        font.nametofont("TkDefaultFont").configure(size=10)
        font.nametofont("TkTextFont").configure(size=12)

        self.header_frame = HeaderFrame(self)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Separator(self, orient='horizontal').pack(side=tk.TOP, fill=tk.X)

        self.queue_table_frame = QueueTableFrame(self)
        self.queue_table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, **PAD_ARGS)

        self.process_table_frame = ProcessTableFrame(self)
        self.process_table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, **PAD_ARGS)

        self.add_queue()
        self.add_process()
        self.add_process()
        self.add_process()

    def validate_queue_host_comboxes(self):
        queue_names = [queue.name for queue in 
                       self.queue_table_frame.queue_objects]
        for process_frame in self.process_table_frame.process_frames:
            process_frame.host_queue_combobox.configure(values=queue_names)
            if process_frame.host_queue_var.get() not in queue_names:
                process_frame.host_queue_var.set(queue_names[-1])

    def add_queue(self):
        self.queue_table_frame.add_queue()
        self.validate_queue_host_comboxes()

    def add_process(self):
        self.process_table_frame.add_process()
        self.validate_queue_host_comboxes()

    def remove_queue(self):
        self.queue_table_frame.remove_queue()
        self.validate_queue_host_comboxes()

    def remove_process(self):
        self.process_table_frame.remove_process()
        self.validate_queue_host_comboxes()

    def simulate(self, queue_scheduler : ql.QueueScheduler):
        queue_objects : Iterable[ql.Queue] = self.queue_table_frame.queue_objects

        for queue_object in queue_objects:
            queue_object.processes.clear()

        process_frames : Iterable[ProcessFrame] = \
                self.process_table_frame.process_frames

        for process_frame in process_frames:
            for queue_object in queue_objects:
                if queue_object.name == process_frame.last_valid_host_queue:
                    queue_object.processes.append(process_frame.process_object)
                    break

        self.external_simulate(queue_objects, queue_scheduler)


class QueueFrame(tk.LabelFrame):
    def __init__(self, container, queue_object : ql.Queue):
        super().__init__(container)

        self.queue_object = queue_object

        self.name_var = tk.StringVar(value=self.queue_object.name)
        self.process_scheduler_var = tk.StringVar(value=
                                                  pl.get_process_scheduler_key(
                                          self.queue_object.process_scheduler))
        self.priority_var = tk.IntVar(value=self.queue_object.priority)
        self.quantum_var = tk.IntVar(value=self.queue_object.quantum)
        self.slice_time_var = tk.IntVar(value=self.queue_object.slice_time)

        self.name_var.trace_add("write", lambda *_: self.validate_queue_object())
        self.process_scheduler_var.trace_add("write", lambda *_: self.validate_queue_object())
        self.priority_var.trace_add("write", lambda *_: self.validate_queue_object())
        self.quantum_var.trace_add("write", lambda *_: self.validate_queue_object())
        self.slice_time_var.trace_add("write", lambda *_: self.validate_queue_object())

        # Queue Name
        self.name_entry = tk.Entry(self, textvariable=self.name_var,
                                   state='readonly', width=3)
        self.name_entry.pack(side=tk.LEFT, **PAD_ARGS)

        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y,
                                                     expand=True)

        # Process Scheduler Options
        tk.Label(self, text='Process Scheduler:').pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.process_scheduler_combobox = ttk.Combobox(self,
                               values=list(pl.PROCESS_SCHEDULERS_DICT.keys()),
                                textvariable=self.process_scheduler_var, width=8)
        self.process_scheduler_combobox.pack(side=tk.LEFT, **PAD_ARGS)

        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y,
                                                     expand=True)

        # Priority options
        tk.Label(self, text='Priority:').pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.priority_spinbox = tk.Spinbox(self, width=3, from_=0, 
                                           to=999, wrap=True, 
                                           textvariable=self.priority_var)
        self.priority_spinbox.pack(side=tk.LEFT, **PAD_ARGS)

        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y,
                                                     expand=True)

        # Slice options
        tk.Label(self, text='Slice:').pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.slice_time_spinbox = tk.Spinbox(self, width=3, from_=0, 
                                           to=999, wrap=True, 
                                             textvariable=self.slice_time_var)
        self.slice_time_spinbox.pack(side=tk.LEFT, **PAD_ARGS)

        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y,
                                                     expand=True)

        # Quantum options
        tk.Label(self, text='Quantum:').pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.quantum_spinbox = tk.Spinbox(self, width=3, from_=0, 
                                           to=999, wrap=True,
                                          textvariable=self.quantum_var)
        self.quantum_spinbox.pack(side=tk.LEFT, **PAD_ARGS)

    def validate_queue_object(self):
        if self.process_scheduler_var.get() in \
                pl.PROCESS_SCHEDULERS_DICT.keys():
            self.queue_object.process_scheduler = pl.PROCESS_SCHEDULERS_DICT[
                self.process_scheduler_var.get()]
        else:
            self.process_scheduler_var.set(str(pl.get_process_scheduler_key(
                self.queue_object.process_scheduler)))

        try:
            if 0 <= self.priority_var.get() <= 999:
                self.queue_object.priority = self.priority_var.get()
            else:
                self.priority_var.set(self.queue_object.priority)
        except:
            self.priority_var.set(self.queue_object.priority)

        try:
            if 0 <= self.quantum_var.get() <= 999:
                self.queue_object.quantum = self.quantum_var.get()
            else:
                self.quantum_var.set(self.queue_object.quantum)
        except:
            self.quantum_var.set(self.queue_object.quantum)

        try:
            if 0 <= self.slice_time_var.get() <= 999:
                self.queue_object.slice_time = self.slice_time_var.get()
            else:
                self.slice_time_var.set(self.queue_object.slice_time)
        except:
            self.slice_time_var.set(self.queue_object.slice_time)


class ProcessFrame(tk.LabelFrame):
    def __init__(self, container, process_object : pl.Process):
        super().__init__(container)

        self.process_object = process_object

        self.name_var = tk.StringVar(value=self.process_object.name)
        self.host_queue_var = tk.StringVar()
        self.arrival_var = tk.IntVar(value=self.process_object.arrival)
        self.burst_var = tk.IntVar(value=self.process_object.burst)
        self.priority_var = tk.IntVar(value=self.process_object.priority)

        self.name_var.trace_add("write", lambda *_: self.validate_process_object())
        self.host_queue_var.trace_add("write", lambda *_: self.validate_process_object())
        self.arrival_var.trace_add("write", lambda *_: self.validate_process_object())
        self.burst_var.trace_add("write", lambda *_: self.validate_process_object())
        self.priority_var.trace_add("write", lambda *_: self.validate_process_object())

        # Process Name
        self.name_entry = tk.Entry(self, textvariable=self.name_var,
                                   readonlybackground=PROCESS_BG_DICT[self.process_object.name],
                                   fg=PROCESS_FG, 
                                   state='readonly', width=3)
        self.name_entry.pack(side=tk.LEFT, **PAD_ARGS)

        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y,
                                                     expand=True)

        # Host Queue Options
        tk.Label(self, text='Host:').pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.host_queue_combobox = ttk.Combobox(self,
                                textvariable=self.host_queue_var, width=3)
        self.host_queue_combobox.pack(side=tk.LEFT, **PAD_ARGS)

        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y,
                                                     expand=True)

        # Arrival options
        tk.Label(self, text='Arrival:').pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.arrival_spinbox = tk.Spinbox(self, width=3, from_=0, 
                                           to=999, wrap=True, 
                                           textvariable=self.arrival_var)
        self.arrival_spinbox.pack(side=tk.LEFT, **PAD_ARGS)

        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y,
                                                     expand=True)

        # Burst options
        tk.Label(self, text='Burst:').pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.burst_spinbox = tk.Spinbox(self, width=3, from_=0, 
                                           to=999, wrap=True, 
                                             textvariable=self.burst_var)
        self.burst_spinbox.pack(side=tk.LEFT, **PAD_ARGS)

        # Separator
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y,
                                                     expand=True)

        # Priority options
        tk.Label(self, text='Priority:').pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.priority_spinbox = tk.Spinbox(self, width=3, from_=0, 
                                           to=999, wrap=True,
                                          textvariable=self.priority_var)
        self.priority_spinbox.pack(side=tk.LEFT, **PAD_ARGS)

        self.last_valid_host_queue : str = self.host_queue_var.get()

    def validate_process_object(self):
        if self.host_queue_var.get() not in self.host_queue_combobox['values']:
            self.host_queue_var.set(self.last_valid_host_queue)
        else:
            self.last_valid_host_queue = self.host_queue_var.get()

        try:
            if 0 <= self.arrival_var.get() <= 999:
                self.process_object.arrival = self.arrival_var.get()
            else:
                self.arrival_var.set(self.process_object.arrival)
        except:
            self.arrival_var.set(self.process_object.arrival)

        try:
            if 0 <= self.burst_var.get() <= 999:
                self.process_object.burst = self.burst_var.get()
            else:
                self.burst_var.set(self.process_object.burst)
        except:
            self.burst_var.set(self.process_object.burst)

        try:
            if 0 <= self.priority_var.get() <= 999:
                self.process_object.priority = self.priority_var.get()
            else:
                self.priority_var.set(self.process_object.priority)
        except:
            self.priority_var.set(self.process_object.priority)






class QueueTableFrame(tk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text='List of Queues')
        self.queue_objects = []
        self.queue_frames = []

    def add_queue(self):
        if len(self.queue_objects) == len(PROCESS_BG_DICT):
            return
        queue_object = ql.Queue(
                name=f'Q{1 + len(self.queue_objects)}', 
                quantum=8, 
                priority=0,
                slice_time=10,
                processes=[],
                process_scheduler=list(pl.PROCESS_SCHEDULERS_DICT.values())[0],
                )
        frame_object = QueueFrame(self, queue_object)
        frame_object.pack(side=tk.TOP, fill=tk.X, **PAD_ARGS)
        self.queue_objects.append(queue_object)
        self.queue_frames.append(frame_object)

    def remove_queue(self):
        if len(self.queue_objects) <= 1:
            return
        self.queue_frames.pop().destroy()
        self.queue_objects.pop()


class ProcessTableFrame(tk.LabelFrame):
    def __init__(self, container):
        super().__init__(container, text='List of Processes')
        self.process_objects = []
        self.process_frames = []

    def add_process(self):
        if len(self.process_objects) == len(PROCESS_BG_DICT):
            return
        process_object = pl.Process(
                name=f'P{1 + len(self.process_objects)}', 
                arrival=0, 
                burst=5,
                priority=0,
                )
        frame_object = ProcessFrame(self, process_object)
        frame_object.pack(side=tk.TOP, fill=tk.X, **PAD_ARGS)
        self.process_objects.append(process_object)
        self.process_frames.append(frame_object)

    def remove_process(self):
        if len(self.process_objects) <= 1:
            return
        self.process_frames.pop().destroy()
        self.process_objects.pop()


class HeaderFrame(tk.Frame):
    def __init__(self, container : MainWindow):
        super().__init__(container)

        self.main_window = container

        # Queue Options
        self.queue_option_label = tk.Label(self, text='Queue:')
        self.queue_option_label.pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.add_queue_button = tk.Button(self, text='Add', 
                                         **BLUE_BG_ARGS,
                                         command=self.main_window.add_queue)
        self.add_queue_button.pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.remove_queue_button = tk.Button(self, text='Remove', 
                                         **RED_BG_ARGS,
                                        command=self.main_window.remove_queue)
        self.remove_queue_button.pack(side=tk.LEFT, **LABEL_PAD_ARGS)

        # Separator
        ttk.Separator(self, orient='vertical').pack(side=tk.LEFT, fill=tk.Y,
                                                      expand=True)

        # Process Options
        self.process_option_label = tk.Label(self, text='Process:')
        self.process_option_label.pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.add_process_button = tk.Button(self, text='Add', 
                                       **BLUE_BG_ARGS,
                                        command=self.main_window.add_process)
        self.add_process_button.pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.remove_process_button = tk.Button(self, text='Remove', 
                                       **RED_BG_ARGS,
                                        command=self.main_window.remove_process)
        self.remove_process_button.pack(side=tk.LEFT, **LABEL_PAD_ARGS)

        # Separator
        ttk.Separator(self, orient='vertical').pack(side=tk.LEFT, fill=tk.Y,
                                                    expand=True)

        # Queue Scheduler Options
        self.queue_scheduler_label = tk.Label(self, text='Multilevel Queue Scheduler:')
        self.queue_scheduler_label.pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        self.queue_scheduler_var = tk.StringVar(
                value=list(ql.QUEUE_SCHEDULERS_DICT.keys())[0])
        for key in ql.QUEUE_SCHEDULERS_DICT.keys():
            radio = tk.Radiobutton(self, value=key, text=key,
                                   variable=self.queue_scheduler_var)
            radio.pack(side=tk.LEFT, **LABEL_PAD_ARGS)
        
        # Separator
        ttk.Separator(self, orient='vertical').pack(side=tk.LEFT, fill=tk.Y,
                                                      expand=True)

        # Simulate Button
        self.simulate_button = tk.Button(
                self, text='Simulate', **GREEN_BG_ARGS,
                command=lambda: self.main_window.simulate(
                    ql.QUEUE_SCHEDULERS_DICT[self.queue_scheduler_var.get()]
                    )
                )
        self.simulate_button.pack(side=tk.LEFT, **PAD_ARGS)
