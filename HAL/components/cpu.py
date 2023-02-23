import time
from HAL.hal import *


class CPU(HALComponent):
    """ Output only component that provides CPU related data. """
    def __init__(self, temp="", cpu="/proc/stat", mem="/proc/meminfo"):
        super(HALComponent, self).__init__()

        self._last_time = time.time()
        self._last_total = 0
        self._last_idle = 0

        self.temp = temp
        self.load = 0
        self.memory = 0

        self._temp_file = open(temp, "r")
        self._cpu_file = open(cpu, "r")
        self._mem_file = open(mem, "r")

    def refresh(self, hal):
        # Read temperature data from the sys folder
        temp_string = self._temp_file.read()
        self.temp = float(temp_string)/1000.0
        self._temp_file.seek(0)

        # Get CPU load stats
        cpu_stats = self._cpu_file.readline()
        cpu_stats_parts = cpu_stats.split()[1:]
        idle = int(cpu_stats_parts[0])
        total_stats = sum(map(lambda x: int(x), cpu_stats_parts))
        self.load = round((idle - self._last_idle) / (total_stats - self._last_total), 3)
        self._cpu_file.seek(0)
        self._last_idle = idle
        self._last_total = total_stats

        # Get RAM usage stats
        mem_total = int(self._mem_file.readline().split()[1])
        _ = self._mem_file.readline()
        mem_available = int(self._mem_file.readline().split()[1])
        self.memory = round((mem_total - mem_available)/mem_total, 3)
        self._mem_file.seek(0)