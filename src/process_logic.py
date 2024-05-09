"""
@file main_window.py
@author Karim M. Ali <https://github.com/kmuali>
@date May 06, 2024
"""

from dataclasses import dataclass
from typing_extensions import override
from copy import deepcopy

@dataclass
class Schedule:
    process_name : str
    start : int
    duration : int


@dataclass
class Process:
    name : str
    arrival : int
    burst : int
    priority : int

EMPTY_PROCESS = Process('', 0, 0, 0)


class ProcessScheduler:
    @staticmethod
    def schedule(processes : list[Process]) -> list[Schedule]:
        answer : list[Schedule] = []
        return answer


class FCFSScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]) -> list[Schedule]:
        processes = deepcopy(processes)
        schedules : list[Schedule] = []
        current_time = -1
        while True:
            processes = [process for process in processes if process.burst > 0]
            if not processes:
                break
            current_time += 1
            possible_processes = [process for process in processes if \
                    process.arrival <= current_time]            
            if possible_processes:
                best_process = min(possible_processes, 
                                   key=lambda process: process.arrival)
                best_process.burst -= 1
            else:
                best_process = EMPTY_PROCESS
            if schedules and schedules[-1].process_name == best_process.name:
                schedules[-1].duration += 1
            else:
                schedules.append(
                        Schedule(
                            process_name=best_process.name,
                            start=current_time,
                            duration=1,
                            )
                        )
        return schedules



class LPFNonPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]) -> list[Schedule]:
        processes = deepcopy(processes)
        schedules : list[Schedule] = []
        current_time = -1
        while True:
            processes = [process for process in processes if process.burst > 0]
            if not processes:
                break
            current_time += 1
            possible_processes = [process for process in processes if \
                    process.arrival <= current_time]            
            if possible_processes:
                best_process = min(possible_processes, 
                                   key=lambda process: process.priority)
                best_process.burst -= 1
            else:
                best_process = EMPTY_PROCESS
            if schedules and schedules[-1].process_name == best_process.name:
                schedules[-1].duration += 1
            else:
                schedules.append(
                        Schedule(
                            process_name=best_process.name,
                            start=current_time,
                            duration=1,
                            )
                        )
        return schedules


class SRTFNonPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]) -> list[Schedule]:
        processes = deepcopy(processes)
        schedules : list[Schedule] = []
        current_time = -1
        while True:
            processes = [process for process in processes if process.burst > 0]
            if not processes:
                break
            current_time += 1
            possible_processes = [process for process in processes if \
                    process.arrival <= current_time]            
            if possible_processes:
                best_process = min(possible_processes, 
                                   key=lambda process: process.burst)
                best_process.burst -= 1
            else:
                best_process = EMPTY_PROCESS
            if schedules and schedules[-1].process_name == best_process.name:
                schedules[-1].duration += 1
            else:
                schedules.append(
                        Schedule(
                            process_name=best_process.name,
                            start=current_time,
                            duration=1,
                            )
                        )
        return schedules




class LPFPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]):
        # TODO:
        processes = deepcopy(processes)
        schedules : list[Schedule] = []
        return schedules


class SRTFPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]):
        # TODO:
        processes = deepcopy(processes)
        schedules : list[Schedule] = []
        return schedules


class RRScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]):
        # TODO:
        processes = deepcopy(processes)
        schedules : list[Schedule] = []
        return schedules


# TODO: Undo comment implemented classes.
PROCESS_SCHEDULERS_DICT = {
        'FCFS': FCFSScheduler(),
        'LPF-NP': LPFNonPreemptiveScheduler(),
        # 'LPF-P': LPFPreemptiveScheduler(),
        # 'SRTF-NP': SRTFNonPreemptiveScheduler(),
        # 'SRTF-P': SRTFPreemptiveScheduler(),
        # 'RR': RRScheduler(),
        }

def get_process_scheduler_key(process_scheduler : ProcessScheduler):
    for key in PROCESS_SCHEDULERS_DICT.keys():
        if process_scheduler == PROCESS_SCHEDULERS_DICT[key]:
            return key
