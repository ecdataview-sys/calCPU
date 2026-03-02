import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import deque
import threading

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = 0
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0
        self.executed = False
        self.first_execution = True
        self.arrival_order = 0

class GanttEntry:
    def __init__(self, pid, start_time, end_time):
        self.pid = pid
        self.start_time = start_time
        self.end_time = end_time

class TimelineEvent:
    def __init__(self, time, event_type, process_id, queue_state, remaining_times, current_process=None):
        self.time = time
        self.event_type = event_type
        self.process_id = process_id
        self.queue_state = queue_state.copy() if queue_state else []
        self.remaining_times = remaining_times.copy() if remaining_times else {}
        self.current_process = current_process

class SchedulingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Algorithms Simulator")
        self.root.geometry("1600x900")
        
        # Process list
        self.processes = []
        self.next_pid = 1
        self.selected_pid = None
        self.selected_process = None
        self.arrival_counter = 0
        
        # Store results for each algorithm
        self.algorithm_results = {
            'FCFS': {'processes': [], 'gantt': [], 'timeline': []},
            'SJF_NP': {'processes': [], 'gantt': [], 'timeline': []},
            'SJF_P': {'processes': [], 'gantt': [], 'timeline': []},
            'RR': {'processes': [], 'gantt': [], 'timeline': []},
            'PRIORITY_ID': {'processes': [], 'gantt': [], 'timeline': []},
            'PRIORITY_AGE': {'processes': [], 'gantt': [], 'timeline': []}
        }
        
        # Current displayed algorithm
        self.current_display = "FCFS"
        self.last_rr_quantum = 2
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Create main horizontal paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left Panel - Settings
        left_frame = ttk.Frame(main_paned, width=400)
        main_paned.add(left_frame, weight=1)
        
        # Right Panel - Display
        right_frame = ttk.Frame(main_paned, width=1200)
        main_paned.add(right_frame, weight=3)
        
        self.setup_left_panel(left_frame)
        self.setup_right_panel(right_frame)
        
    def setup_left_panel(self, parent):
        # Process Input Frame
        input_frame = ttk.LabelFrame(parent, text="Process Input", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Arrival Time:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.arrival_entry = ttk.Entry(input_frame, width=15)
        self.arrival_entry.grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(input_frame, text="Burst Time:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.burst_entry = ttk.Entry(input_frame, width=15)
        self.burst_entry.grid(row=1, column=1, pady=2, padx=5)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(button_frame, text="Add Process", command=self.add_process).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Clear All", command=self.clear_processes).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(input_frame, text="Process List:", font=('Arial', 10, 'bold')).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Treeview for processes with selection binding
        columns = ('PID', 'Arrival', 'Burst')
        self.process_tree = ttk.Treeview(input_frame, columns=columns, show='headings', height=6)
        self.process_tree.heading('PID', text='PID')
        self.process_tree.heading('Arrival', text='Arrival')
        self.process_tree.heading('Burst', text='Burst')
        self.process_tree.column('PID', width=50, anchor='center')
        self.process_tree.column('Arrival', width=70, anchor='center')
        self.process_tree.column('Burst', width=70, anchor='center')
        self.process_tree.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Bind selection event
        self.process_tree.bind('<<TreeviewSelect>>', self.on_process_select)
        
        # Edit buttons frame
        edit_frame = ttk.Frame(input_frame)
        edit_frame.grid(row=5, column=0, columnspan=2, pady=5)
        
        ttk.Button(edit_frame, text="Load Selected", command=self.load_selected_process).pack(side=tk.LEFT, padx=2)
        ttk.Button(edit_frame, text="Update Process", command=self.update_process).pack(side=tk.LEFT, padx=2)
        ttk.Button(edit_frame, text="Delete Selected", command=self.delete_process).pack(side=tk.LEFT, padx=2)
        
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        
        # Algorithm Selection Frame
        algo_frame = ttk.LabelFrame(parent, text="Algorithm Selection", padding="10")
        algo_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.algo_vars = {}
        
        # Basic algorithms
        self.algo_vars['FCFS'] = tk.BooleanVar(value=True)
        ttk.Checkbutton(algo_frame, text="First Come First Serve (FCFS)", 
                       variable=self.algo_vars['FCFS']).pack(anchor=tk.W, pady=2)
        
        self.algo_vars['SJF_NP'] = tk.BooleanVar(value=True)
        ttk.Checkbutton(algo_frame, text="Non-Preemptive Shortest Job First (SJF)", 
                       variable=self.algo_vars['SJF_NP']).pack(anchor=tk.W, pady=2)
        
        self.algo_vars['SJF_P'] = tk.BooleanVar(value=True)
        ttk.Checkbutton(algo_frame, text="Preemptive Shortest Job First (SRTF)", 
                       variable=self.algo_vars['SJF_P']).pack(anchor=tk.W, pady=2)
        
        # Round Robin
        rr_frame = ttk.Frame(algo_frame)
        rr_frame.pack(anchor=tk.W, pady=2, fill=tk.X)
        
        self.algo_vars['RR'] = tk.BooleanVar(value=True)
        ttk.Checkbutton(rr_frame, text="Round Robin", 
                       variable=self.algo_vars['RR']).pack(side=tk.LEFT)
        
        ttk.Label(rr_frame, text="Quantum:").pack(side=tk.LEFT, padx=(10,2))
        self.rr_quantum_entry = ttk.Entry(rr_frame, width=8)
        self.rr_quantum_entry.pack(side=tk.LEFT)
        self.rr_quantum_entry.insert(0, "2")
        
        self.multiple_rr_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(algo_frame, text="Compare multiple RR quanta", 
                       variable=self.multiple_rr_var, command=self.toggle_rr_quanta_entry).pack(anchor=tk.W, pady=2)
        
        quanta_frame = ttk.Frame(algo_frame)
        quanta_frame.pack(anchor=tk.W, pady=2, fill=tk.X, padx=(20,0))
        
        ttk.Label(quanta_frame, text="Quanta (comma-separated):").pack(side=tk.LEFT)
        self.rr_quanta_entry = ttk.Entry(quanta_frame, width=20)
        self.rr_quanta_entry.pack(side=tk.LEFT, padx=5)
        self.rr_quanta_entry.insert(0, "1,2,4")
        self.rr_quanta_entry.config(state='disabled')
        
        # Priority Scheduling Options
        priority_sep = ttk.Separator(algo_frame, orient='horizontal')
        priority_sep.pack(fill=tk.X, pady=10)
        
        ttk.Label(algo_frame, text="Priority Scheduling", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=2)
        
        self.algo_vars['PRIORITY_ID'] = tk.BooleanVar(value=False)
        ttk.Checkbutton(algo_frame, text="Priority by Process ID (smaller ID = higher priority)", 
                       variable=self.algo_vars['PRIORITY_ID']).pack(anchor=tk.W, pady=2)
        
        self.algo_vars['PRIORITY_AGE'] = tk.BooleanVar(value=False)
        ttk.Checkbutton(algo_frame, text="Priority by Age (only for same arrival time, newer = higher priority)", 
                       variable=self.algo_vars['PRIORITY_AGE']).pack(anchor=tk.W, pady=2)
        
        ttk.Button(algo_frame, text="Run Selected Algorithms", 
                  command=self.run_algorithms, style='Accent.TButton').pack(pady=20)
        
        self.progress = ttk.Progressbar(algo_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # Algorithm selection for display - using Listbox
        ttk.Label(algo_frame, text="Show details for:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10,2))
        
        # Create frame for listbox and scrollbar
        listbox_frame = ttk.Frame(algo_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create listbox
        self.display_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                                          selectmode=tk.SINGLE, height=7,
                                          font=('Arial', 10))
        self.display_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=self.display_listbox.yview)
        
        # Add items to listbox
        items = ['FCFS', 'SJF (NP)', 'SJF (P)', 'RR', 
                 'Priority (ID)', 'Priority (Age)', 'RR Comparison']
        for item in items:
            self.display_listbox.insert(tk.END, item)
        
        # Select first item by default
        self.display_listbox.selection_set(0)
        self.display_listbox.bind('<<ListboxSelect>>', self.on_display_select)
        
    def setup_right_panel(self, parent):
        right_paned = ttk.PanedWindow(parent, orient=tk.VERTICAL)
        right_paned.pack(fill=tk.BOTH, expand=True)
        
        # Gantt Chart Frame
        gantt_frame = ttk.LabelFrame(right_paned, text="Gantt Chart", padding="5")
        right_paned.add(gantt_frame, weight=2)
        
        self.fig, self.ax = plt.subplots(figsize=(14, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=gantt_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.ax.set_xlabel('Time Units', fontsize=10)
        self.ax.set_ylabel('Process', fontsize=10)
        self.ax.set_title('Gantt Chart', fontsize=12)
        self.ax.grid(True, alpha=0.3, axis='x')
        self.ax.set_yticks([])
        self.ax.xaxis.set_major_locator(plt.MultipleLocator(1))
        self.ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
        self.canvas.draw()
        
        # Timeline Frame
        timeline_frame = ttk.LabelFrame(right_paned, text="Timeline Breakdown (per time unit)", padding="5")
        right_paned.add(timeline_frame, weight=1)
        
        # Create text widget for timeline
        self.timeline_text = tk.Text(timeline_frame, wrap=tk.NONE, font=('Courier', 9), height=10)
        y_scroll = ttk.Scrollbar(timeline_frame, orient=tk.VERTICAL, command=self.timeline_text.yview)
        x_scroll = ttk.Scrollbar(timeline_frame, orient=tk.HORIZONTAL, command=self.timeline_text.xview)
        self.timeline_text.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Pack layout
        self.timeline_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Results Frame
        results_frame = ttk.LabelFrame(right_paned, text="Results", padding="5")
        right_paned.add(results_frame, weight=2)
        
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)
        
        self.results_texts = {}
        algorithms = [
            ('FCFS', 'FCFS'), 
            ('SJF_NP', 'SJF (NP)'),
            ('SJF_P', 'SJF (P)'),
            ('RR', 'Round Robin'),
            ('PRIORITY_ID', 'Priority (ID)'),
            ('PRIORITY_AGE', 'Priority (Age)'),
            ('RR_Comparison', 'RR Comparison')
        ]
        
        for algo_key, algo_name in algorithms:
            frame = ttk.Frame(self.results_notebook)
            self.results_notebook.add(frame, text=algo_name)
            
            text_widget = tk.Text(frame, wrap=tk.NONE, font=('Courier', 9))
            y_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
            x_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=text_widget.xview)
            text_widget.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
            
            text_widget.grid(row=0, column=0, sticky='nsew')
            y_scroll.grid(row=0, column=1, sticky='ns')
            x_scroll.grid(row=1, column=0, sticky='ew')
            
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            
            self.results_texts[algo_key] = text_widget
    
    # Process management methods
    def on_process_select(self, event):
        """Handle process selection in treeview"""
        selected = self.process_tree.selection()
        if selected:
            item = self.process_tree.item(selected[0])
            self.selected_pid = item['values'][0]
            self.selected_process = next((p for p in self.processes if p.pid == self.selected_pid), None)
    
    def load_selected_process(self):
        """Load selected process data into entry fields for editing"""
        if self.selected_pid is None:
            messagebox.showwarning("Warning", "Please select a process to load")
            return
        
        process = next((p for p in self.processes if p.pid == self.selected_pid), None)
        if process:
            self.arrival_entry.delete(0, tk.END)
            self.arrival_entry.insert(0, str(process.arrival_time))
            self.burst_entry.delete(0, tk.END)
            self.burst_entry.insert(0, str(process.burst_time))
    
    def update_process(self):
        """Update selected process with new values"""
        if self.selected_pid is None:
            messagebox.showwarning("Warning", "Please select a process to update")
            return
        
        try:
            new_arrival = float(self.arrival_entry.get())
            new_burst = float(self.burst_entry.get())
            
            if new_burst <= 0:
                messagebox.showerror("Error", "Burst time must be positive")
                return
            
            # Find and update the process
            for process in self.processes:
                if process.pid == self.selected_pid:
                    process.arrival_time = new_arrival
                    process.burst_time = new_burst
                    process.remaining_time = new_burst
                    break
            
            # Update treeview
            for item in self.process_tree.get_children():
                if self.process_tree.item(item)['values'][0] == self.selected_pid:
                    self.process_tree.item(item, values=(self.selected_pid, f"{new_arrival:.1f}", f"{new_burst:.1f}"))
                    break
            
            # Clear entries
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.selected_pid = None
            self.selected_process = None
            
            messagebox.showinfo("Success", f"Process P{self.selected_pid} updated successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def toggle_rr_quanta_entry(self):
        if self.multiple_rr_var.get():
            self.rr_quanta_entry.config(state='normal')
        else:
            self.rr_quanta_entry.config(state='disabled')
    
    def on_display_select(self, event):
        """Handle display selection from listbox"""
        selection = self.display_listbox.curselection()
        if selection:
            self.current_display = self.display_listbox.get(selection[0])
            self.update_display()
    
    def add_process(self):
        try:
            arrival = float(self.arrival_entry.get())
            burst = float(self.burst_entry.get())
            
            if burst <= 0:
                messagebox.showerror("Error", "Burst time must be positive")
                return
            
            self.arrival_counter += 1
            process = Process(self.next_pid, arrival, burst)
            process.arrival_order = self.arrival_counter
            self.processes.append(process)
            self.process_tree.insert('', 'end', values=(process.pid, f"{arrival:.1f}", f"{burst:.1f}"))
            self.next_pid += 1
            
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def delete_process(self):
        if self.selected_pid:
            self.processes = [p for p in self.processes if p.pid != self.selected_pid]
            for item in self.process_tree.get_children():
                if self.process_tree.item(item)['values'][0] == self.selected_pid:
                    self.process_tree.delete(item)
                    break
            self.selected_pid = None
            self.selected_process = None
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
    
    def clear_processes(self):
        self.processes = []
        self.next_pid = 1
        self.arrival_counter = 0
        self.selected_pid = None
        self.selected_process = None
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        self.arrival_entry.delete(0, tk.END)
        self.burst_entry.delete(0, tk.END)
    
    def get_remaining_dict(self, processes):
        return {p.pid: p.remaining_time for p in processes}
    
    def record_state(self, time, processes, ready_queue, current_process, timeline, event_type="State"):
        """Record the state at a specific time"""
        remaining = self.get_remaining_dict(processes)
        queue_pids = [p.pid for p in ready_queue] if ready_queue else []
        timeline.append(TimelineEvent(
            time, event_type, -1, queue_pids, remaining, 
            current_process.pid if current_process else None
        ))
    
    def fcfs_scheduling(self, processes):
        """FCFS with per-time-unit timeline"""
        processes = sorted(processes, key=lambda x: x.arrival_time)
        gantt_entries = []
        timeline = []
        ready_queue = deque()
        not_arrived = list(processes)
        current_process = None
        
        max_time = max(p.arrival_time for p in processes) + sum(p.burst_time for p in processes)
        
        for t in range(int(max_time) + 1):
            time = float(t)
            
            # Check for arrivals at this time
            for p in not_arrived[:]:
                if p.arrival_time <= time:
                    not_arrived.remove(p)
                    ready_queue.append(p)
                    self.record_state(time, processes, ready_queue, current_process, 
                                    timeline, f"P{p.pid} arrives")
            
            # If no process running and queue not empty, start next
            if not current_process and ready_queue:
                current_process = ready_queue.popleft()
                if current_process.first_execution:
                    current_process.start_time = time
                    current_process.response_time = time - current_process.arrival_time
                    current_process.first_execution = False
                self.record_state(time, processes, ready_queue, current_process,
                                timeline, f"P{current_process.pid} starts")
            
            # Record state at this time
            if current_process:
                self.record_state(time, processes, ready_queue, current_process,
                                timeline, f"P{current_process.pid} running")
                gantt_entries.append(GanttEntry(current_process.pid, time, time + 1))
                
                # Update remaining time
                current_process.remaining_time -= 1
                
                # Check if process completed
                if current_process.remaining_time == 0:
                    current_process.completion_time = time + 1
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    self.record_state(time + 1, processes, ready_queue, None,
                                    timeline, f"P{current_process.pid} completes")
                    current_process = None
            else:
                if not_arrived:
                    self.record_state(time, processes, ready_queue, None,
                                    timeline, "CPU Idle")
                    gantt_entries.append(GanttEntry(-1, time, time + 1))
        
        return sorted(processes, key=lambda x: x.pid), gantt_entries, timeline
    
    def non_preemptive_sjf(self, processes):
        """Non-preemptive SJF with per-time-unit timeline"""
        processes = sorted(processes, key=lambda x: x.arrival_time)
        gantt_entries = []
        timeline = []
        ready_queue = []
        not_arrived = list(processes)
        current_process = None
        
        max_time = max(p.arrival_time for p in processes) + sum(p.burst_time for p in processes)
        
        for t in range(int(max_time) + 1):
            time = float(t)
            
            # Check for arrivals at this time
            for p in not_arrived[:]:
                if p.arrival_time <= time:
                    not_arrived.remove(p)
                    ready_queue.append(p)
                    # Sort ready queue by burst time (shortest first)
                    ready_queue.sort(key=lambda x: x.burst_time)
                    self.record_state(time, processes, ready_queue, current_process,
                                    timeline, f"P{p.pid} arrives")
            
            # If no process running and queue not empty, start next (shortest job)
            if not current_process and ready_queue:
                current_process = ready_queue.pop(0)  # Take shortest job
                if current_process.first_execution:
                    current_process.start_time = time
                    current_process.response_time = time - current_process.arrival_time
                    current_process.first_execution = False
                self.record_state(time, processes, ready_queue, current_process,
                                timeline, f"P{current_process.pid} starts (burst={current_process.burst_time})")
            
            # Record state at this time
            if current_process:
                self.record_state(time, processes, ready_queue, current_process,
                                timeline, f"P{current_process.pid} running")
                gantt_entries.append(GanttEntry(current_process.pid, time, time + 1))
                
                # Update remaining time
                current_process.remaining_time -= 1
                
                # Check if process completed
                if current_process.remaining_time == 0:
                    current_process.completion_time = time + 1
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    self.record_state(time + 1, processes, ready_queue, None,
                                    timeline, f"P{current_process.pid} completes")
                    current_process = None
            else:
                if not_arrived:
                    self.record_state(time, processes, ready_queue, None,
                                    timeline, "CPU Idle")
                    gantt_entries.append(GanttEntry(-1, time, time + 1))
        
        return sorted(processes, key=lambda x: x.pid), gantt_entries, timeline
    
    def preemptive_sjf(self, processes):
        """Preemptive SJF (SRTF) with per-time-unit timeline"""
        processes = sorted(processes, key=lambda x: x.arrival_time)
        gantt_entries = []
        timeline = []
        ready_queue = []
        not_arrived = list(processes)
        current_process = None
        last_process = None
        
        max_time = max(p.arrival_time for p in processes) + sum(p.burst_time for p in processes)
        
        for t in range(int(max_time) + 1):
            time = float(t)
            
            # Check for arrivals at this time
            for p in not_arrived[:]:
                if p.arrival_time <= time:
                    not_arrived.remove(p)
                    ready_queue.append(p)
                    # Sort ready queue by remaining time
                    ready_queue.sort(key=lambda x: x.remaining_time)
                    self.record_state(time, processes, ready_queue, current_process,
                                    timeline, f"P{p.pid} arrives")
            
            # Select shortest remaining time process
            if ready_queue:
                next_process = ready_queue[0]
                if current_process != next_process:
                    if current_process:
                        self.record_state(time, processes, ready_queue, next_process,
                                        timeline, f"P{current_process.pid} preempted (rem={current_process.remaining_time})")
                    current_process = next_process
                    if current_process.first_execution:
                        current_process.start_time = time
                        current_process.response_time = time - current_process.arrival_time
                        current_process.first_execution = False
                        self.record_state(time, processes, 
                                        [p for p in ready_queue if p != current_process], 
                                        current_process, timeline, f"P{current_process.pid} starts (rem={current_process.remaining_time})")
            
            # Record state at this time
            if current_process:
                self.record_state(time, processes, 
                                [p for p in ready_queue if p != current_process], 
                                current_process, timeline, f"P{current_process.pid} running")
                gantt_entries.append(GanttEntry(current_process.pid, time, time + 1))
                
                # Update remaining time
                current_process.remaining_time -= 1
                
                # Check if process completed
                if current_process.remaining_time == 0:
                    ready_queue.remove(current_process)
                    current_process.completion_time = time + 1
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    self.record_state(time + 1, processes, ready_queue, None,
                                    timeline, f"P{current_process.pid} completes")
                    current_process = None
            else:
                if not_arrived:
                    self.record_state(time, processes, ready_queue, None,
                                    timeline, "CPU Idle")
                    gantt_entries.append(GanttEntry(-1, time, time + 1))
        
        return sorted(processes, key=lambda x: x.pid), gantt_entries, timeline
    
    def round_robin(self, processes, time_quantum):
        """Round Robin with per-time-unit timeline"""
        processes = sorted(processes, key=lambda x: x.arrival_time)
        gantt_entries = []
        timeline = []
        ready_queue = deque()
        not_arrived = list(processes)
        current_process = None
        time_in_quantum = 0
        
        max_time = max(p.arrival_time for p in processes) + sum(p.burst_time for p in processes)
        
        for t in range(int(max_time) + 1):
            time = float(t)
            
            # Check for arrivals at this time
            for p in not_arrived[:]:
                if p.arrival_time <= time:
                    not_arrived.remove(p)
                    ready_queue.append(p)
                    queue_list = list(ready_queue)
                    if current_process and current_process.remaining_time > 0:
                        queue_list = [current_process] + queue_list
                    self.record_state(time, processes, [q for q in queue_list if q != p], 
                                    current_process, timeline, f"P{p.pid} arrives (queued at end)")
            
            # If no process running and queue not empty, start next
            if not current_process and ready_queue:
                current_process = ready_queue.popleft()
                time_in_quantum = 0
                if current_process.first_execution:
                    current_process.start_time = time
                    current_process.response_time = time - current_process.arrival_time
                    current_process.first_execution = False
                    self.record_state(time, processes, list(ready_queue), current_process,
                                    timeline, f"P{current_process.pid} starts (first time)")
                else:
                    self.record_state(time, processes, list(ready_queue), current_process,
                                    timeline, f"P{current_process.pid} resumes")
            
            # Record state at this time
            if current_process:
                self.record_state(time, processes, list(ready_queue), current_process,
                                timeline, f"P{current_process.pid} running")
                gantt_entries.append(GanttEntry(current_process.pid, time, time + 1))
                
                # Update remaining time and quantum counter
                current_process.remaining_time -= 1
                time_in_quantum += 1
                
                # Check if process completed
                if current_process.remaining_time == 0:
                    current_process.completion_time = time + 1
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    self.record_state(time + 1, processes, list(ready_queue), None,
                                    timeline, f"P{current_process.pid} completes")
                    current_process = None
                    time_in_quantum = 0
                # Check if quantum expired
                elif time_in_quantum >= time_quantum:
                    if current_process.remaining_time > 0:
                        ready_queue.append(current_process)
                        self.record_state(time + 1, processes, list(ready_queue), None,
                                        timeline, f"P{current_process.pid} preempted - moved to end")
                    current_process = None
                    time_in_quantum = 0
            else:
                if not_arrived:
                    self.record_state(time, processes, list(ready_queue), None,
                                    timeline, "CPU Idle")
                    gantt_entries.append(GanttEntry(-1, time, time + 1))
        
        return sorted(processes, key=lambda x: x.pid), gantt_entries, timeline
    
    def priority_by_id_scheduling(self, processes):
        """Priority scheduling by ID (smaller ID = higher priority) with per-time-unit timeline"""
        processes = sorted(processes, key=lambda x: x.arrival_time)
        gantt_entries = []
        timeline = []
        ready_queue = []
        not_arrived = list(processes)
        current_process = None
        
        max_time = max(p.arrival_time for p in processes) + sum(p.burst_time for p in processes)
        
        for t in range(int(max_time) + 1):
            time = float(t)
            
            # Check for arrivals at this time
            for p in not_arrived[:]:
                if p.arrival_time <= time:
                    not_arrived.remove(p)
                    ready_queue.append(p)
                    # Sort by priority (smaller PID = higher priority)
                    ready_queue.sort(key=lambda x: x.pid)
                    self.record_state(time, processes, ready_queue, current_process,
                                    timeline, f"P{p.pid} arrives (priority={p.pid})")
            
            # Select highest priority process (smallest PID)
            if ready_queue:
                next_process = ready_queue[0]
                if current_process != next_process:
                    if current_process:
                        self.record_state(time, processes, ready_queue, next_process,
                                        timeline, f"P{current_process.pid} preempted by higher priority P{next_process.pid}")
                    current_process = next_process
                    if current_process.first_execution:
                        current_process.start_time = time
                        current_process.response_time = time - current_process.arrival_time
                        current_process.first_execution = False
                        self.record_state(time, processes, 
                                        [p for p in ready_queue if p != current_process], 
                                        current_process, timeline, f"P{current_process.pid} starts (priority={current_process.pid})")
            
            # Record state at this time
            if current_process:
                self.record_state(time, processes, 
                                [p for p in ready_queue if p != current_process], 
                                current_process, timeline, f"P{current_process.pid} running")
                gantt_entries.append(GanttEntry(current_process.pid, time, time + 1))
                
                # Update remaining time
                current_process.remaining_time -= 1
                
                # Check if process completed
                if current_process.remaining_time == 0:
                    ready_queue.remove(current_process)
                    current_process.completion_time = time + 1
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    self.record_state(time + 1, processes, ready_queue, None,
                                    timeline, f"P{current_process.pid} completes")
                    current_process = None
            else:
                if not_arrived:
                    self.record_state(time, processes, ready_queue, None,
                                    timeline, "CPU Idle")
                    gantt_entries.append(GanttEntry(-1, time, time + 1))
        
        return sorted(processes, key=lambda x: x.pid), gantt_entries, timeline
    
    def priority_by_age_scheduling(self, processes):
        """Priority scheduling by age - only affects ties in arrival time
           Newer processes (later arrival order) have higher priority ONLY when arrival times are equal
           Otherwise, follows FCFS order
        """
        processes = sorted(processes, key=lambda x: x.arrival_time)
        gantt_entries = []
        timeline = []
        ready_queue = []
        not_arrived = list(processes)
        current_process = None
        
        max_time = max(p.arrival_time for p in processes) + sum(p.burst_time for p in processes)
        
        for t in range(int(max_time) + 1):
            time = float(t)
            
            # Check for arrivals at this time
            arrivals_at_time = []
            for p in not_arrived[:]:
                if p.arrival_time <= time:
                    not_arrived.remove(p)
                    arrivals_at_time.append(p)
            
            # Sort arrivals by arrival order (later = higher priority for ties)
            if arrivals_at_time:
                # Sort by arrival order (higher number = later arrival)
                arrivals_at_time.sort(key=lambda x: x.arrival_order)
                for p in arrivals_at_time:
                    ready_queue.append(p)
                    self.record_state(time, processes, ready_queue, current_process,
                                    timeline, f"P{p.pid} arrives (order={p.arrival_order})")
            
            # For priority by age, we only reorder when there's a tie in arrival time
            # Group processes by arrival time
            arrival_time_groups = {}
            for p in ready_queue:
                if p.arrival_time not in arrival_time_groups:
                    arrival_time_groups[p.arrival_time] = []
                arrival_time_groups[p.arrival_time].append(p)
            
            # Rebuild ready queue: FCFS order, but within same arrival time, newer first
            new_ready_queue = []
            # Sort by arrival time (FCFS)
            sorted_times = sorted(arrival_time_groups.keys())
            for at in sorted_times:
                # For same arrival time, sort by arrival order (newer first = higher order number)
                same_time_procs = sorted(arrival_time_groups[at], key=lambda x: -x.arrival_order)
                new_ready_queue.extend(same_time_procs)
            
            ready_queue = new_ready_queue
            
            # Select next process (first in queue)
            if ready_queue:
                next_process = ready_queue[0]
                if current_process != next_process:
                    if current_process:
                        # Check if preemption is needed (only if next process has higher priority)
                        # Higher priority means: earlier arrival time, or same arrival time but newer
                        current_priority = (current_process.arrival_time, -current_process.arrival_order)
                        next_priority = (next_process.arrival_time, -next_process.arrival_order)
                        
                        if next_priority < current_priority:  # Next has higher priority
                            self.record_state(time, processes, ready_queue, next_process,
                                            timeline, f"P{current_process.pid} preempted by newer P{next_process.pid}")
                            current_process = next_process
                            ready_queue.pop(0)
                            if current_process.first_execution:
                                current_process.start_time = time
                                current_process.response_time = time - current_process.arrival_time
                                current_process.first_execution = False
                                self.record_state(time, processes, 
                                                [p for p in ready_queue if p != current_process], 
                                                current_process, timeline, 
                                                f"P{current_process.pid} starts (arr={current_process.arrival_time}, order={current_process.arrival_order})")
                    else:
                        # No current process, start the next one
                        current_process = next_process
                        ready_queue.pop(0)
                        if current_process.first_execution:
                            current_process.start_time = time
                            current_process.response_time = time - current_process.arrival_time
                            current_process.first_execution = False
                            self.record_state(time, processes, 
                                            [p for p in ready_queue if p != current_process], 
                                            current_process, timeline, 
                                            f"P{current_process.pid} starts (arr={current_process.arrival_time}, order={current_process.arrival_order})")
            
            # Record state at this time
            if current_process:
                self.record_state(time, processes, 
                                [p for p in ready_queue if p != current_process], 
                                current_process, timeline, f"P{current_process.pid} running")
                gantt_entries.append(GanttEntry(current_process.pid, time, time + 1))
                
                # Update remaining time
                current_process.remaining_time -= 1
                
                # Check if process completed
                if current_process.remaining_time == 0:
                    if current_process in ready_queue:
                        ready_queue.remove(current_process)
                    current_process.completion_time = time + 1
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                    self.record_state(time + 1, processes, ready_queue, None,
                                    timeline, f"P{current_process.pid} completes")
                    current_process = None
            else:
                if not_arrived or ready_queue:
                    self.record_state(time, processes, ready_queue, None,
                                    timeline, "CPU Idle")
                    gantt_entries.append(GanttEntry(-1, time, time + 1))
        
        return sorted(processes, key=lambda x: x.pid), gantt_entries, timeline
    
    def format_timeline(self, timeline_events):
        """Format timeline events for display"""
        if not timeline_events:
            return "No timeline data available"
        
        result = "\n" + "="*160 + "\n"
        result += "TIMELINE BREAKDOWN (per time unit)\n"
        result += "="*160 + "\n\n"
        
        result += f"{'Time':<8} {'Event':<70} {'Running':<8} {'Queue':<35} {'Remaining'}\n"
        result += "-" * 160 + "\n"
        
        for event in timeline_events:
            time_str = f"t={event.time:.1f}"
            
            # Format running process
            running_str = f"P{event.current_process}" if event.current_process else "None"
            
            # Format queue state
            if event.queue_state:
                queue_str = "[" + ", ".join([f"P{p}" for p in event.queue_state]) + "]"
            else:
                queue_str = "[]"
            
            # Format remaining times
            remaining_str = ""
            for pid, rem in sorted(event.remaining_times.items()):
                if rem > 0:
                    remaining_str += f"P{pid}:{rem:.1f} "
            
            result += f"{time_str:<8} {event.event_type:<70} {running_str:<8} {queue_str:<35} {remaining_str}\n"
        
        result += "-" * 160 + "\n"
        return result
    
    def format_results(self, processes, algorithm_name):
        result = f"\n{'='*90}\n"
        result += f"{algorithm_name} Results\n"
        result += f"{'='*90}\n\n"
        
        result += f"{'Process':<10} {'Arrival':<10} {'Burst':<10} {'Start':<10} "
        result += f"{'Completion':<12} {'Turnaround':<12} {'Waiting':<10} {'Response':<10}\n"
        result += "-" * 94 + "\n"
        
        total_tat = total_wt = total_rt = 0
        
        for p in sorted(processes, key=lambda x: x.pid):
            result += f"P{p.pid:<9} {p.arrival_time:<10.2f} {p.burst_time:<10.2f} "
            result += f"{p.start_time:<10.2f} {p.completion_time:<12.2f} "
            result += f"{p.turnaround_time:<12.2f} {p.waiting_time:<10.2f} {p.response_time:<10.2f}\n"
            total_tat += p.turnaround_time
            total_wt += p.waiting_time
            total_rt += p.response_time
        
        n = len(processes)
        result += "-" * 94 + "\n"
        result += f"\n{'Average Turnaround Time:':<30} {total_tat/n:.2f}\n"
        result += f"{'Average Waiting Time:':<30} {total_wt/n:.2f}\n"
        result += f"{'Average Response Time:':<30} {total_rt/n:.2f}\n"
        
        return result
    
    def plot_gantt_chart(self, gantt_entries, title):
        self.ax.clear()
        
        if not gantt_entries:
            self.ax.text(0.5, 0.5, 'No Gantt chart data available', 
                        ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return
        
        colors = plt.cm.Set3(np.linspace(0, 1, 10))
        color_map = {-1: 'lightgray'}
        
        y_pos = 1
        max_time = 0
        
        # Group consecutive same PID entries
        grouped_entries = []
        for entry in gantt_entries:
            if not grouped_entries or grouped_entries[-1].pid != entry.pid:
                grouped_entries.append(GanttEntry(entry.pid, entry.start_time, entry.end_time))
            else:
                grouped_entries[-1].end_time = entry.end_time
        
        for entry in grouped_entries:
            if entry.pid not in color_map:
                color_map[entry.pid] = colors[entry.pid % 10]
            
            duration = entry.end_time - entry.start_time
            max_time = max(max_time, entry.end_time)
            
            self.ax.barh(y_pos, duration, left=entry.start_time, height=0.5,
                        color=color_map[entry.pid], edgecolor='black', linewidth=1)
            
            label = f"P{entry.pid}" if entry.pid != -1 else "IDLE"
            if duration >= 0.5:
                self.ax.text(entry.start_time + duration/2, y_pos, label, 
                            ha='center', va='center', fontsize=9, fontweight='bold')
        
        self.ax.set_ylim(0.5, 1.5)
        self.ax.set_xlim(0, max_time)
        self.ax.set_xlabel('Time Units', fontsize=10)
        self.ax.set_title(title, fontsize=12)
        self.ax.grid(True, alpha=0.3, axis='x')
        self.ax.set_yticks([])
        self.ax.xaxis.set_major_locator(plt.MultipleLocator(1))
        
        self.canvas.draw()
    
    def update_display(self):
        """Update display based on current selection"""
        selected = self.current_display
        
        if selected == 'FCFS' and self.algorithm_results['FCFS']['gantt']:
            self.plot_gantt_chart(self.algorithm_results['FCFS']['gantt'], "FCFS Gantt Chart")
            self.timeline_text.delete(1.0, tk.END)
            self.timeline_text.insert(tk.END, self.format_timeline(self.algorithm_results['FCFS']['timeline']))
            
        elif selected == 'SJF (NP)' and self.algorithm_results['SJF_NP']['gantt']:
            self.plot_gantt_chart(self.algorithm_results['SJF_NP']['gantt'], "Non-preemptive SJF Gantt Chart")
            self.timeline_text.delete(1.0, tk.END)
            self.timeline_text.insert(tk.END, self.format_timeline(self.algorithm_results['SJF_NP']['timeline']))
            
        elif selected == 'SJF (P)' and self.algorithm_results['SJF_P']['gantt']:
            self.plot_gantt_chart(self.algorithm_results['SJF_P']['gantt'], "Preemptive SJF (SRTF) Gantt Chart")
            self.timeline_text.delete(1.0, tk.END)
            self.timeline_text.insert(tk.END, self.format_timeline(self.algorithm_results['SJF_P']['timeline']))
            
        elif selected == 'RR' and self.algorithm_results['RR']['gantt']:
            self.plot_gantt_chart(self.algorithm_results['RR']['gantt'], 
                                 f"Round Robin (Q={self.last_rr_quantum}) Gantt Chart")
            self.timeline_text.delete(1.0, tk.END)
            self.timeline_text.insert(tk.END, self.format_timeline(self.algorithm_results['RR']['timeline']))
            
        elif selected == 'Priority (ID)' and self.algorithm_results['PRIORITY_ID']['gantt']:
            self.plot_gantt_chart(self.algorithm_results['PRIORITY_ID']['gantt'], "Priority by ID Gantt Chart")
            self.timeline_text.delete(1.0, tk.END)
            self.timeline_text.insert(tk.END, self.format_timeline(self.algorithm_results['PRIORITY_ID']['timeline']))
            
        elif selected == 'Priority (Age)' and self.algorithm_results['PRIORITY_AGE']['gantt']:
            self.plot_gantt_chart(self.algorithm_results['PRIORITY_AGE']['gantt'], "Priority by Age Gantt Chart")
            self.timeline_text.delete(1.0, tk.END)
            self.timeline_text.insert(tk.END, self.format_timeline(self.algorithm_results['PRIORITY_AGE']['timeline']))
            
        elif selected == 'RR Comparison':
            self.results_notebook.select(self.results_texts['RR_Comparison'])
    
    def run_algorithms(self):
        if not self.processes:
            messagebox.showerror("Error", "Please add at least one process")
            return
        
        self.progress.start()
        
        for widget in self.results_texts.values():
            widget.delete(1.0, tk.END)
        self.timeline_text.delete(1.0, tk.END)
        
        for key in self.algorithm_results:
            self.algorithm_results[key] = {'processes': [], 'gantt': [], 'timeline': []}
        
        thread = threading.Thread(target=self._run_algorithms_thread)
        thread.daemon = True
        thread.start()
    
    def _run_algorithms_thread(self):
        try:
            # FCFS
            if self.algo_vars['FCFS'].get():
                procs = [Process(p.pid, p.arrival_time, p.burst_time) for p in self.processes]
                for i, p in enumerate(procs):
                    p.arrival_order = self.processes[i].arrival_order
                results, gantt, timeline = self.fcfs_scheduling(procs)
                self.algorithm_results['FCFS'] = {'processes': results, 'gantt': gantt, 'timeline': timeline}
                self.root.after(0, lambda: self.results_texts['FCFS'].insert(
                    tk.END, self.format_results(results, "First Come First Serve (FCFS)")))
            
            # Non-preemptive SJF
            if self.algo_vars['SJF_NP'].get():
                procs = [Process(p.pid, p.arrival_time, p.burst_time) for p in self.processes]
                for i, p in enumerate(procs):
                    p.arrival_order = self.processes[i].arrival_order
                results, gantt, timeline = self.non_preemptive_sjf(procs)
                self.algorithm_results['SJF_NP'] = {'processes': results, 'gantt': gantt, 'timeline': timeline}
                self.root.after(0, lambda: self.results_texts['SJF_NP'].insert(
                    tk.END, self.format_results(results, "Non-Preemptive Shortest Job First (SJF)")))
            
            # Preemptive SJF
            if self.algo_vars['SJF_P'].get():
                procs = [Process(p.pid, p.arrival_time, p.burst_time) for p in self.processes]
                for i, p in enumerate(procs):
                    p.arrival_order = self.processes[i].arrival_order
                results, gantt, timeline = self.preemptive_sjf(procs)
                self.algorithm_results['SJF_P'] = {'processes': results, 'gantt': gantt, 'timeline': timeline}
                self.root.after(0, lambda: self.results_texts['SJF_P'].insert(
                    tk.END, self.format_results(results, "Preemptive Shortest Job First (SRTF)")))
            
            # Round Robin
            if self.algo_vars['RR'].get():
                if self.multiple_rr_var.get():
                    quanta = [float(q.strip()) for q in self.rr_quanta_entry.get().split(',')]
                    
                    comparison_text = "\n" + "="*90 + "\n"
                    comparison_text += "ROUND ROBIN COMPARISON\n"
                    comparison_text += "="*90 + "\n\n"
                    comparison_text += f"{'Quantum':<12} {'Avg Turnaround':<18} {'Avg Waiting':<18} {'Avg Response':<18}\n"
                    comparison_text += "-" * 66 + "\n"
                    
                    for i, q in enumerate(quanta):
                        procs = [Process(p.pid, p.arrival_time, p.burst_time) for p in self.processes]
                        for j, p in enumerate(procs):
                            p.arrival_order = self.processes[j].arrival_order
                        results, gantt, timeline = self.round_robin(procs, q)
                        
                        if i == 0:
                            self.algorithm_results['RR'] = {'processes': results, 'gantt': gantt, 'timeline': timeline}
                            self.last_rr_quantum = q
                        
                        n = len(results)
                        avg_tat = sum(p.turnaround_time for p in results) / n
                        avg_wt = sum(p.waiting_time for p in results) / n
                        avg_rt = sum(p.response_time for p in results) / n
                        
                        comparison_text += f"Q = {q:<6} {avg_tat:<18.2f} {avg_wt:<18.2f} {avg_rt:<18.2f}\n"
                        
                        self.root.after(0, lambda t=q, r=results: self.results_texts['RR'].insert(
                            tk.END, self.format_results(r, f"Round Robin (Quantum = {t})")))
                    
                    self.root.after(0, lambda: self.results_texts['RR_Comparison'].insert(tk.END, comparison_text))
                    
                else:
                    q = float(self.rr_quantum_entry.get())
                    self.last_rr_quantum = q
                    procs = [Process(p.pid, p.arrival_time, p.burst_time) for p in self.processes]
                    for i, p in enumerate(procs):
                        p.arrival_order = self.processes[i].arrival_order
                    results, gantt, timeline = self.round_robin(procs, q)
                    self.algorithm_results['RR'] = {'processes': results, 'gantt': gantt, 'timeline': timeline}
                    self.root.after(0, lambda: self.results_texts['RR'].insert(
                        tk.END, self.format_results(results, f"Round Robin (Time Quantum = {q})")))
            
            # Priority by ID
            if self.algo_vars['PRIORITY_ID'].get():
                procs = [Process(p.pid, p.arrival_time, p.burst_time) for p in self.processes]
                for i, p in enumerate(procs):
                    p.arrival_order = self.processes[i].arrival_order
                results, gantt, timeline = self.priority_by_id_scheduling(procs)
                self.algorithm_results['PRIORITY_ID'] = {'processes': results, 'gantt': gantt, 'timeline': timeline}
                self.root.after(0, lambda: self.results_texts['PRIORITY_ID'].insert(
                    tk.END, self.format_results(results, "Priority Scheduling (Smaller ID = Higher Priority)")))
            
            # Priority by Age
            if self.algo_vars['PRIORITY_AGE'].get():
                procs = [Process(p.pid, p.arrival_time, p.burst_time) for p in self.processes]
                for i, p in enumerate(procs):
                    p.arrival_order = self.processes[i].arrival_order
                results, gantt, timeline = self.priority_by_age_scheduling(procs)
                self.algorithm_results['PRIORITY_AGE'] = {'processes': results, 'gantt': gantt, 'timeline': timeline}
                self.root.after(0, lambda: self.results_texts['PRIORITY_AGE'].insert(
                    tk.END, self.format_results(results, "Priority Scheduling (Only ties: newer = higher priority)")))
            
            self.root.after(0, self.update_display)
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", str(e))
        finally:
            self.root.after(0, self.progress.stop)

def main():
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
    
    app = SchedulingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()