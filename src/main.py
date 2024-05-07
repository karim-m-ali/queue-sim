"""
@file queue_sim.py
@author Karim M. Ali <https://github.com/kmuali>
@date May 06, 2024
"""

from typing import Iterable
import main_gui
import results_gui
import queue_logic as ql
import process_logic as pl


class QueueSim:
    def __init__(self):
        self.main_window = main_gui.MainWindow(self.simulate)
        self.main_window.mainloop()

    def simulate(self, queues : list[ql.Queue], 
                 queue_scheduler : ql.QueueScheduler):
        new_window = results_gui.ResultsTopLevel(self.main_window,
                                                 queue_scheduler.schedule(queues))
        new_window.mainloop()


if __name__ == '__main__':
    QueueSim()
