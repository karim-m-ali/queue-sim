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
from main_gui import RED_BG_ARGS, GREEN_BG_ARGS, BLUE_BG_ARGS, PAD_ARGS, \
        LABEL_PAD_ARGS, PROCESS_FG, PROCESS_BG_DICT

class ResultsWindow(tk.Tk):
    def __init__(self, schedule_timeline : ql.ScheduleTimeline):
        super().__init__()

        self.schedule_timeline = schedule_timeline

        self.title('QueueSim - Results')
        self.minsize(1280, 800) # WXGA - wide

        font.nametofont("TkDefaultFont").configure(size=10)
        font.nametofont("TkTextFont").configure(size=12)

        ttk.Separator(self, orient='horizontal').pack(side=tk.TOP, fill=tk.X)


class ScheduleTimeline:
