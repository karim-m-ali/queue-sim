"""
@file main_window.py
@author Karim M. Ali <https://github.com/kmuali>
@date May 07, 2024
"""
from copy import deepcopy
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
import queue_logic as ql
import process_logic as pl
from main_gui import RED_BG_ARGS, GREEN_BG_ARGS, BLUE_BG_ARGS, PAD_ARGS, \
        LABEL_PAD_ARGS, PROCESS_FG, PROCESS_BG_DICT, PROCESS_BG_BLANK

class ResultsTopLevel(tk.Toplevel):
    def __init__(self, main_window, 
                 schedule_timelines : list[ql.ScheduleTimeline]):
        super().__init__(main_window)

        self.title('QueueSim - Results')
        self.minsize(1280, 800) # WXGA - wide

        font.nametofont("TkDefaultFont").configure(size=10)
        font.nametofont("TkTextFont").configure(size=12)

        total_time = max(map(lambda tl: tl.total_time, schedule_timelines))

        self.schedule_timeline_frames = [
                ScheduleTimelineFrame(self, schedule_timeline, total_time) for 
                schedule_timeline in schedule_timelines
                ]
        for schedule_timeline_frame in self.schedule_timeline_frames:
            schedule_timeline_frame.pack(side=tk.TOP, fill=tk.X, **PAD_ARGS)


class HeaderFrame(tk.Frame):
    def __init__(self, container, schedule_timeline : ql.ScheduleTimeline):
        super().__init__(container)

        self.name_entry = tk.Entry(self, width=3)
        self.name_entry.insert(0, schedule_timeline.name)
        self.name_entry.configure(state='readonly')
        self.name_entry.pack(side=tk.LEFT, **PAD_ARGS)

        if schedule_timeline.name == 'CPU':
            self.name_entry.configure(
                    width=4, 
                    readonlybackground='#222',
                    fg='#fff',
                    )

        if not schedule_timeline.schedule_list:
            ttk.Separator(self, orient='vertical').pack(side=tk.LEFT, fill=tk.Y)
            tk.Label(self, text=f'No processes').pack(side=tk.LEFT, **PAD_ARGS)
            return

        ttk.Separator(self, orient='vertical').pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(self, text=f'Context Switches: {schedule_timeline.context_switches}'
                 ).pack(side=tk.LEFT, **PAD_ARGS)

        ttk.Separator(self, orient='vertical').pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(self, text=f'Average Waiting Time: {schedule_timeline.avg_wait:.5}'
                 ).pack(side=tk.LEFT, **PAD_ARGS)

        ttk.Separator(self, orient='vertical').pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(self, text=f'Maximum Waiting Time: {schedule_timeline.max_wait}'
                 ).pack(side=tk.LEFT, **PAD_ARGS)

        ttk.Separator(self, orient='vertical').pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(self, text=f'Minimum Waiting Time: {schedule_timeline.min_wait}'
                 ).pack(side=tk.LEFT, **PAD_ARGS)


class ScheduleFrame(tk.Frame):
    def __init__(self, container, schedule : ql.Schedule):
        super().__init__(container)

        self.name_entry = tk.Entry(self, width=3,
                                   fg='#fff',
                    readonlybackground=PROCESS_BG_DICT[schedule.process_name] \
                            if schedule.process_name in PROCESS_BG_DICT else \
                            PROCESS_BG_BLANK)
        self.name_entry.insert(0, schedule.process_name)
        self.name_entry.configure(state='readonly')
        self.name_entry.pack(side=tk.TOP, fill=tk.X)

        tk.Label(self, text=str(schedule.start)).pack(side=tk.LEFT, fill=tk.X)


class SchedulesFrame(tk.Frame):
    def __init__(self, container, schedules : list[pl.Schedule],
                 total_time : int):
        super().__init__(container)

        # Creating temporary schedules and filling gaps
        tmp_schedules = []
        current_time = 0
        for schedule in deepcopy(schedules):
            if schedule.start > current_time:
                tmp_schedules.append(pl.Schedule('', current_time, 
                                                 schedule.start - current_time))
            tmp_schedules.append(schedule)
            current_time = schedule.start + schedule.duration

        if not tmp_schedules:
            tmp_schedules.append(pl.Schedule('', 0, total_time))

        end_time = tmp_schedules[-1].start + tmp_schedules[-1].duration
        if end_time < total_time:
            tmp_schedules.append(pl.Schedule('', end_time, 
                                             total_time - end_time))

        # Creating frames
        for index, schedule in enumerate(tmp_schedules):
            frame = ScheduleFrame(self, schedule)
            weight = schedule.duration * 1000 // total_time
            self.columnconfigure(index=index, weight=weight)
            frame.grid(row=0, column=index, sticky=tk.EW)

        tk.Label(self, text=str(total_time)).grid(row=0, 
                                                  column=len(tmp_schedules), 
                                                  sticky=tk.S)


class ScheduleTimelineFrame(tk.LabelFrame):
    def __init__(self, container, schedule_timeline : ql.ScheduleTimeline,
                 total_time : int):
        super().__init__(container)

        self.header_frame = HeaderFrame(self, schedule_timeline)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Separator(self, orient='horizontal').pack(side=tk.TOP, fill=tk.X)

        self.schedules_frame = SchedulesFrame(self, 
                                              schedule_timeline.schedule_list,
                                              total_time)
        self.schedules_frame.pack(side=tk.TOP, fill=tk.X, **PAD_ARGS)
