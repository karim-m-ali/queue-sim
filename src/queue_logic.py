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

    @staticmethod
    def set_status(processes : list[Process], timeline : ScheduleTimeline):
        timeline.context_switches = len(timeline.schedule_list) - 1
        timeline.max_wait = 0
        timeline.avg_wait = 0.0
        for process in processes:
            expected_end_time = process.arrival + process.burst
            actual_end_time = 0
            for schedule in reversed(timeline.schedule_list):
                if schedule.process_name == process.name:
                    actual_end_time = schedule.start + schedule.duration
                    break
            wait = actual_end_time - expected_end_time
            timeline.max_wait = max(timeline.max_wait, wait)
            timeline.avg_wait += wait 
        timeline.avg_wait /= len(processes)

    @staticmethod
    def get_schedule_timelines(queues : list[Queue]) -> list[ScheduleTimeline]:
        schedule_timelines = []
        for queue in queues:
            if len(queue.processes):
                schedule_timeline = ScheduleTimeline(
                        queue.name, 
                        queue.process_scheduler.schedule(queue.processes),
                        0, 0, 0)
                QueueScheduler.set_status(queue.processes, schedule_timeline)
                schedule_timelines.append(schedule_timeline)
        return schedule_timelines


class SliceQueueScheduler(QueueScheduler):
    @staticmethod
    @override
    def schedule(queues : list[Queue]) -> list[ScheduleTimeline]:
        # TODO: Implement.
        schedule_timelines = QueueScheduler.get_schedule_timelines(queues)
        return schedule_timelines


class PriorityQueueScheduler(QueueScheduler):
    @override
    @staticmethod
    def schedule(queues : list[Queue]) -> list[ScheduleTimeline]:
        schedule_timelines = QueueScheduler.get_schedule_timelines(queues)

        cpu_timeline = ScheduleTimeline(name='CPU', schedule_list=[],            
                                        context_switches=0, avg_wait=0, 
                                        max_wait=0)
        current_time = 0
        for timeline in schedule_timelines:
            for schedule in timeline.schedule_list:
                cpu_timeline.schedule_list.append(
                        Schedule(
                            process_name=schedule.process_name,
                            start=current_time, 
                            duration=schedule.duration)
                        )
                current_time += schedule.duration

        all_processes = []
        for queue in queues:
            all_processes += queue.processes
        QueueScheduler.set_status(all_processes, cpu_timeline)

        print('medo')
        return [cpu_timeline] + schedule_timelines


# TODO: Undo comment implemented classes.
QUEUE_SCHEDULERS_DICT = {
        # 'Time Slice': SliceQueueScheduler(), 
        'Priority': PriorityQueueScheduler()
        }
