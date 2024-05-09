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
        processes = sorted(processes, key=lambda process: process.arrival)
        schedules : list[Schedule] = []
        current_time = 0
        for process in processes:
            schedules.append(Schedule(
                process.name, 
                start=current_time, 
                duration=process.burst
                ))
            current_time += process.burst
        return schedules


class LPFNonPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]) -> list[Schedule]:
        processes = deepcopy(processes)
        processes = sorted(processes, key=lambda process: process.priority)
        schedules : list[Schedule] = []
        current_time = 0
        for process in processes:
            schedules.append(Schedule(
                process.name, 
                start=current_time, 
                duration=process.burst
                ))
            current_time += process.burst
        return schedules


class SRTFNonPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]) -> list[Schedule]:
        processes = deepcopy(processes)
        processes = sorted(processes, key=lambda process: process.burst)
        schedules : list[Schedule] = []
        current_time = 0
        for process in processes:
            schedules.append(Schedule(
                process.name, 
                start=current_time, 
                duration=process.burst
                ))
            current_time += process.burst
        return schedules


class LPFPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]):
        # TODO:
        answer : list[Schedule] = []
        return answer


class SRTFPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]):
        # TODO:
        answer : list[Schedule] = []
        return answer


class RRScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]):
        # TODO:
        answer : list[Schedule] = []
        return answer


# TODO: Undo comment implemented classes.
PROCESS_SCHEDULERS_DICT = {
        'FCFS': FCFSScheduler(),
        'LPF-NP': LPFNonPreemptiveScheduler(),
        # 'LPF-P': LPFPreemptiveScheduler(),
        'SRTF-NP': SRTFNonPreemptiveScheduler(),
        # 'SRTF-P': SRTFPreemptiveScheduler(),
        # 'RR': RRScheduler(),
        }

def get_process_scheduler_key(process_scheduler : ProcessScheduler):
    for key in PROCESS_SCHEDULERS_DICT.keys():
        if process_scheduler == PROCESS_SCHEDULERS_DICT[key]:
            return key
