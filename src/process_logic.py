"""
@file main_window.py
@author Karim M. Ali <https://github.com/kmuali>
@date May 06, 2024
"""

from dataclasses import dataclass
from typing_extensions import override

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


class RRScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]):
        answer : list[Schedule] = []
        return answer


class LPFNonPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]):
        answer : list[Schedule] = []
        return answer


class LPFPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]):
        answer : list[Schedule] = []
        return answer


class SRTFNonPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]):
        answer : list[Schedule] = []
        return answer


class SRTFPreemptiveScheduler(ProcessScheduler):
    @staticmethod
    @override
    def schedule(processes : list[Process]):
        answer : list[Schedule] = []
        return answer


PROCESS_SCHEDULERS_DICT = {
        'FCFS': FCFSScheduler(),
        'RR': RRScheduler(),
        'LPF-NP': LPFNonPreemptiveScheduler(),
        'LPF-P': LPFPreemptiveScheduler(),
        'SRTF-NP': SRTFNonPreemptiveScheduler(),
        'SRTF-P': SRTFPreemptiveScheduler(),
        }

def get_process_scheduler_key(process_scheduler : ProcessScheduler):
    for key in PROCESS_SCHEDULERS_DICT.keys():
        if process_scheduler == PROCESS_SCHEDULERS_DICT[key]:
            return key
