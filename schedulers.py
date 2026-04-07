from collections import deque
from models import Process, GanttEntry


class Scheduler:
    def __call__(self, procs, mode, quantum=2):
        for p in procs:
            p.reset()

        procs.sort(key=lambda x: (x.arrival_time, x.pid))
        # initialize
        gantt = []
        log = []
        ready_queue = deque() if mode == 'RR' else []
        not_arrived = list(procs)
        current_proc = None
        time = 0
        time_in_quantum = 0
        
        # 未到
        while not_arrived or ready_queue or current_proc:
            arrivals = []
            for p in not_arrived[:]:
                if p.arrival_time <= time:
                    not_arrived.remove(p)
                    ready_queue.append(p)
                    arrivals.append(p.pid)
            if arrivals:
                log.append((time, 'Arrival', '-', str(arrivals)))

            if mode != 'RR' and ready_queue:
                if mode == 'FCFS':
                    ready_queue.sort(key=lambda x: (x.arrival_time, x.pid))
                elif mode == 'SJF_NP' and current_proc is None:
                    ready_queue.sort(key=lambda x: (x.burst_time, x.arrival_time, x.pid))
                elif mode == 'SRTF':
                    ready_queue.sort(key=lambda x: (x.remaining_time, x.arrival_time, x.pid))
                elif mode == 'PRIORITY_NP' and current_proc is None:
                    ready_queue.sort(key=lambda x: (x.priority, x.arrival_time, x.pid))
                elif mode == 'PRIORITY_P':
                    ready_queue.sort(key=lambda x: (x.priority, x.arrival_time, x.pid))

            if current_proc and ready_queue:
                preempt = False
                if mode == 'SRTF' and ready_queue[0].remaining_time < current_proc.remaining_time:
                    preempt = True
                elif mode == 'PRIORITY_P' and ready_queue[0].priority < current_proc.priority:
                    preempt = True
                elif mode == 'RR' and time_in_quantum >= quantum:
                    preempt = True

                if preempt:
                    ready_queue.append(current_proc)
                    log.append((time, 'Preemption', f'P{current_proc.pid}', str([p.pid for p in ready_queue])))
                    current_proc = None
                    time_in_quantum = 0
                    if mode != 'RR' and ready_queue:
                        if mode == 'SRTF':
                            ready_queue.sort(key=lambda x: (x.remaining_time, x.arrival_time, x.pid))
                        elif mode == 'PRIORITY_P':
                            ready_queue.sort(key=lambda x: (x.priority, x.arrival_time, x.pid))

            if current_proc is None and ready_queue:
                current_proc = ready_queue.popleft() if mode == 'RR' else ready_queue.pop(0)
                time_in_quantum = 0
                if current_proc.start_time == -1:
                    current_proc.start_time = time
                    current_proc.response_time = current_proc.start_time - current_proc.arrival_time
                log.append((time, 'Execution Start', f'P{current_proc.pid}', str([p.pid for p in ready_queue])))

            if current_proc:
                gantt.append(GanttEntry(current_proc.pid, time, time + 1))
                current_proc.remaining_time -= 1
                time_in_quantum += 1
                if current_proc.remaining_time <= 0:
                    current_proc.remaining_time = 0
                    current_proc.completion_time = time + 1
                    current_proc.turnaround_time = current_proc.completion_time - current_proc.arrival_time
                    current_proc.waiting_time = current_proc.turnaround_time - current_proc.burst_time
                    log.append((time + 1, 'Completion', f'P{current_proc.pid}', str([p.pid for p in ready_queue])))
                    current_proc = None
                    time_in_quantum = 0
            else:
                gantt.append(GanttEntry(-1, time, time + 1))

            time += 1

        # Merge consecutive same-pid entries
        merged_gantt = []
        if gantt:
            curr = GanttEntry(gantt[0].pid, gantt[0].start_time, gantt[0].end_time)
            for entry in gantt[1:]:
                if entry.pid == curr.pid:
                    curr.end_time = entry.end_time
                else:
                    merged_gantt.append(curr)
                    curr = GanttEntry(entry.pid, entry.start_time, entry.end_time)
            merged_gantt.append(curr)

        n = len(procs)
        avg_wt = sum(p.waiting_time for p in procs) / n
        avg_rt = sum(p.response_time for p in procs) / n
        avg_tat = sum(p.turnaround_time for p in procs) / n

        first_arrival = min(p.arrival_time for p in procs) if procs else 0
        last_completion = max(p.completion_time for p in procs) if procs else 0
        busy_time = sum((entry.end_time - entry.start_time) for entry in merged_gantt if entry.pid != -1)
        idle_time = sum((entry.end_time - entry.start_time) for entry in merged_gantt if entry.pid == -1 and entry.start_time >= first_arrival)
        active_span = busy_time + idle_time

        utilization = (busy_time / active_span) * 100 if active_span > 0 else 0
        throughput = n / active_span if active_span > 0 else 0

        return {
            'procs': procs,
            'gantt': merged_gantt,
            'log': log,
            'atat': avg_tat,
            'awt': avg_wt,
            'art': avg_rt,
            'util': utilization,
            'thr': throughput,
            'busy_time': busy_time,
            'idle_time': idle_time,
            'active_span': active_span,
            'first_arrival': first_arrival,
            'last_completion': last_completion,
            'total_time': last_completion
        }
