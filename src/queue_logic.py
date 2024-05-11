"""
@file main_window.py
@author Karim M. Ali <https://github.com/kmuali>
@date May 06, 2024
"""

from process_logic import Process, ProcessScheduler, Schedule
from typing_extensions import override
from dataclasses import dataclass
import copy


@dataclass
class ScheduleTimeline:
    name : str
    schedule_list : list[Schedule]
    context_switches : int
    avg_wait : float
    max_wait : int
    min_wait : int
    total_time : int
    def __init__(self, name : str, schedule_list : list[Schedule], 
                 processes : list[Process]):
        self.name = name
        self.schedule_list = schedule_list
        self.context_switches = len(self.schedule_list) - 1
        self.avg_wait = 0.0
        self.max_wait = 0
        self.min_wait = 1_000_000_000
        self.total_time = 0
        for process in processes:
            expected_end_time = process.arrival + process.burst
            actual_end_time = 0
            for schedule in reversed(self.schedule_list):
                if schedule.process_name == process.name:
                    actual_end_time = schedule.start + schedule.duration
                    break
            wait = actual_end_time - expected_end_time
            self.max_wait = max(self.max_wait, wait)
            self.min_wait = min(self.min_wait, wait)
            self.avg_wait += wait / len(processes)
            self.total_time = max(self.total_time, actual_end_time)


@dataclass
class Queue:
    name : str
    quantum : int
    priority : int
    slice_time : int
    processes : list[Process]
    process_scheduler : ProcessScheduler


class QueueScheduler:
    @staticmethod
    def schedule(queues : list[Queue]) -> list[ScheduleTimeline]:
        schedule_timelines = []
        return schedule_timelines


class SliceQueueScheduler(QueueScheduler):
    @staticmethod
    @override
    def schedule(queues : list[Queue]) -> list[ScheduleTimeline]:
        # TODO: Implement.
        return []


class PriorityQueueScheduler(QueueScheduler):
    @override
    @staticmethod
    def schedule(queues : list[Queue]) -> list[ScheduleTimeline]:
        # TODO: Implement.
        return [ScheduleTimeline(
            name=queue.name, 
            processes=queue.processes, 
            schedule_list=queue.process_scheduler.schedule(
                queue.processes,
                queue.quantum
                )
            ) for queue in queues]

# TODO: Undo comment implemented classes.
QUEUE_SCHEDULERS_DICT = {
        # 'Time Slice': SliceQueueScheduler(), 
        'Priority': PriorityQueueScheduler()
        }
