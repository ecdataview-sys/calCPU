class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = float(arrival_time)
        self.burst_time = int(burst_time)
        self.priority = int(priority)
        self.reset()

    def reset(self):
        self.remaining_time = int(self.burst_time)
        self.start_time = -1
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0


class GanttEntry:
    def __init__(self, pid, start_time, end_time):
        self.pid = pid
        self.start_time = start_time
        self.end_time = end_time
