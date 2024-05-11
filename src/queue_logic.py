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
    def __hash__(self) -> int:
        return self.name.__hash__()


class QueueScheduler:
    @staticmethod
    def schedule(queues : list[Queue]) -> list[ScheduleTimeline]:
        schedule_timelines = []
        return schedule_timelines

    @staticmethod
    def schedule_pre(queues : list[Queue]) -> dict[Queue, list[Schedule]]:
        return {
                queue: queue.process_scheduler.schedule(
                    queue.processes, 
                    queue.quantum
                    ) for queue in queues
                }

    @staticmethod
    def all_processes(queues : list[Queue]) -> list[Process]:
        ls = []
        for queue in queues:
            ls.extend(queue.processes)
        return ls

    @staticmethod
    def schedules_post(cpu_schedules : list[Schedule], 
                       cpu_processes : list[Process],
                       queues : list[Queue], 
                       schedules_dict : dict[Queue, list[Schedule]]
                       ) -> list[ScheduleTimeline]:
        cpu_timeline = ScheduleTimeline(
                name='CPU',
                processes=cpu_processes,
                schedule_list=cpu_schedules
                )
        ## Preparing other queues
        timelines = [
                ScheduleTimeline(
                    name=f'Isolated {queue.name}', 
                    processes=queue.processes, 
                    schedule_list=schedules_dict[queue]
                    ) for queue in queues
                ]
        timelines.insert(0, cpu_timeline)
        return timelines


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
        schedules_dict = QueueScheduler.schedule_pre(queues)

        tmp_schedules_dict = copy.deepcopy(schedules_dict)
        cpu_processes = QueueScheduler.all_processes(queues)
        cpu_schedules : list[Schedule] = []

        current_time = 0
        while True:
            possible_queues_dict = {queue: schedules for queue, schedules in 
                                    tmp_schedules_dict.items() if schedules}
            if not possible_queues_dict:
                break
            ready_queues_dict = {queue: schedules for queue, schedules in 
                                    possible_queues_dict.items() if 
                                 schedules[0].start <= current_time}
            if not ready_queues_dict:
                current_time += 1
                continue
            best_queue = min(ready_queues_dict.keys(), 
                             key=lambda queue: queue.priority)
            best_schedule = ready_queues_dict[best_queue][0]
            if cpu_schedules and cpu_schedules[-1].process_name == \
                    best_schedule.process_name:
                cpu_schedules[-1].duration += 1
            else:
                cpu_schedules.append(Schedule(
                    process_name=best_schedule.process_name,
                    start=current_time,
                    duration=1,
                    ))
            best_schedule.duration -= 1
            if best_schedule.duration == 0:
                ready_queues_dict[best_queue].remove(best_schedule)
            current_time += 1

        return QueueScheduler.schedules_post(cpu_schedules=cpu_schedules, 
                                             cpu_processes=cpu_processes,
                                             queues=queues, 
                                             schedules_dict=schedules_dict)

# TODO: Undo comment implemented classes.
QUEUE_SCHEDULERS_DICT = {
        # 'Time Slice': SliceQueueScheduler(), 
        'Priority': PriorityQueueScheduler()
        }
