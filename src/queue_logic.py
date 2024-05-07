"""
@file main_window.py
@author Karim M. Ali <https://github.com/kmuali>
@date May 06, 2024
"""

from process_logic import Process, ProcessScheduler, Schedule
from typing_extensions import override
from dataclasses import dataclass


@dataclass
class ScheduleTimeline:
    name : str
    schedule_list : list[Schedule]
    context_switches : int
    avg_wait : float
    max_wait : int


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
        schedule_timelines = [ScheduleTimeline('',[],5,6,7)]
        return schedule_timelines


class SliceQueueScheduler(QueueScheduler):
    @staticmethod
    @override
    def schedule(queues : list[Queue]) -> list[ScheduleTimeline]:
        schedule_timelines = []
        for queue in queues:
            schedule_timeline = ScheduleTimeline(
                    queue.name, 
                    queue.process_scheduler.schedule(queue.processes),
                    0, 0, 0)
            schedule_timelines.append(schedule_timeline)
        return schedule_timelines


class PriorityQueueScheduler(QueueScheduler):
    @override
    @staticmethod
    def schedule(queues : list[Queue]) -> dict[str, list[Schedule]]:
        answer = {}
        return answer

QUEUE_SCHEDULERS_DICT = {'Time Slice': SliceQueueScheduler(), 
                         'Priority': PriorityQueueScheduler()}
