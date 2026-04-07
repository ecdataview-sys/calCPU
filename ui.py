import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
import random
import copy


class SchedulingGUI:
    # initialize
    def __init__(self, root, scheduler, exporter):
        self.root = root
        self.scheduler = scheduler
        self.exporter = exporter
        self.root.title("CPU Scheduling Algorithms Simulator")
        self.root.geometry("1580x960")
        self.root.minsize(1360, 800)
        self.processes = []
        self.next_pid = 1
        self.selected_pid = None
        self.editing_pid = None
        
        # six algorithms learned from the OS courses
        self.algorithms = [
            'FCFS',
            'SJF (NP)',
            'SRTF (Preemptive)',
            'Round Robin',
            'Priority (NP)',
            'Priority (Preemptive)'
        ]
        
        self.results = {algo: {} for algo in self.algorithms}
        self.colors = ['#2563eb', '#0f766e', '#7c3aed', '#dc2626', '#d97706', '#0891b2', '#65a30d', '#be185d']
        
        # short description of the algorithms for third party's easy understanding of what i am doing
        self.algorithm_descriptions = {
            'FCFS': 'First-Come, First-Served executes processes strictly in arrival order. It is simple and fair by arrival time, but long jobs can delay short jobs.',
            'SJF (NP)': 'Shortest Job First (Non-preemptive) chooses the ready process with the smallest burst time. It reduces average waiting time well, but can starve long jobs if short jobs keep arriving.',
            'SRTF (Preemptive)': 'Shortest Remaining Time First is the preemptive version of SJF. A newly arrived shorter job can interrupt the current one, which usually improves response for short tasks.',
            'Round Robin': 'Round Robin shares CPU time fairly using a fixed time quantum. It is widely used in time-sharing systems because each process gets repeated turns.',
            'Priority (NP)': 'Non-preemptive Priority scheduling selects the highest-priority ready process and lets it finish. It is useful when urgent work must be favored over normal work.',
            'Priority (Preemptive)': 'Preemptive Priority scheduling allows a higher-priority arrival to interrupt the running process. It is responsive for critical work, but low-priority jobs may wait much longer.'
        }
        
        # centralize for easy update of the color
        self.theme = {
            'bg': '#eef2f7',
            'surface': '#ffffff',
            'surface_alt': '#f8fafc',
            'border': '#dbe3ef',
            'text': '#0f172a',
            'muted': '#64748b',
            'accent': '#2563eb',
            'accent_2': '#0f766e',
            'danger': '#dc2626',
            'warning': '#d97706',
            'success': '#16a34a',
            'idle': '#e5e7eb'
        }

        self.setup_theme()
        self.setup_ui()

    def setup_theme(self):
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')

        T = self.theme
        style.configure('.', font=('Segoe UI', 10), background=T['bg'], foreground=T['text'])
        style.configure('TFrame', background=T['bg'])
        style.configure('Surface.TFrame', background=T['surface'])
        style.configure('TLabelframe', background=T['surface'], bordercolor=T['border'], relief='solid')
        style.configure('TLabelframe.Label', background=T['surface'], foreground=T['text'], font=('Segoe UI Semibold', 11))
        style.configure('TLabel', background=T['bg'], foreground=T['text'])
        style.configure('Title.TLabel', background=T['bg'], foreground=T['text'], font=('Segoe UI Semibold', 20))
        style.configure('Subtitle.TLabel', background=T['bg'], foreground=T['muted'], font=('Segoe UI', 10))
        style.configure('CardTitle.TLabel', background=T['surface'], foreground=T['muted'], font=('Segoe UI Semibold', 10))
        style.configure('CardValue.TLabel', background=T['surface'], foreground=T['text'], font=('Segoe UI Semibold', 18))
        style.configure('Desc.TLabel', background=T['surface'], foreground=T['text'], font=('Segoe UI', 10), wraplength=1000, justify='left')
        style.configure('TButton', font=('Segoe UI', 10), padding=7)
        style.configure('Primary.TButton', background=T['accent'], foreground='white', font=('Segoe UI Semibold', 10), padding=9)
        style.map('Primary.TButton', background=[('active', '#1d4ed8')])
        style.configure('Accent.TButton', background=T['accent_2'], foreground='white', font=('Segoe UI Semibold', 10), padding=8)
        style.map('Accent.TButton', background=[('active', '#115e59')])
        style.configure('Treeview', rowheight=28, font=('Consolas', 10), background='white', fieldbackground='white', bordercolor=T['border'])
        style.configure('Treeview.Heading', font=('Segoe UI Semibold', 10), background='#e2e8f0', foreground=T['text'])
        style.configure('TNotebook', background=T['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', font=('Segoe UI Semibold', 10), padding=(14, 8))
        style.map('TNotebook.Tab', background=[('selected', T['surface'])], foreground=[('selected', T['accent'])])

    def setup_ui(self):
        # Header Section
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=16, pady=(12, 6))
        
        title_container = ttk.Frame(header)
        title_container.pack(side=tk.LEFT, fill=tk.Y)
        ttk.Label(title_container, text='CPU Scheduling Algorithms Simulator', style='Title.TLabel').pack(anchor='w')
        ttk.Label(title_container, text='Dashboard for scheduling analysis, algorithm comparison, and exportable reports.\nApply the knowledge gain from the course of "Data Structure, Algorithms, and Problem Solving" (8090SEF) to help my study of another course, Operating System (OS) (8670SEF).', style='Subtitle.TLabel').pack(anchor='w', pady=(2, 0))

        action_box = ttk.Frame(header)
        action_box.pack(side=tk.RIGHT, pady=5)
        
        ttk.Button(action_box, text='▶ Run Simulation', style='Primary.TButton', command=self.run_algorithms).pack(side=tk.LEFT, padx=4)
        ttk.Button(action_box, text='📊 Export Results to Excel', command=self.export_results_excel).pack(side=tk.LEFT, padx=4)
        ttk.Button(action_box, text='🧾 Export Results to PDF', command=self.export_results_pdf).pack(side=tk.LEFT, padx=4)

        # Stats Bar
        stats_bar = ttk.Frame(self.root, style='Surface.TFrame', padding=10)
        stats_bar.pack(fill=tk.X, padx=16, pady=(0, 10))

        self.kpi_algo = self.create_kpi_card(stats_bar, 0, 'Selected Algorithm', 'FCFS')
        self.kpi_util = self.create_kpi_card(stats_bar, 1, 'CPU Utilization', '0.0%')
        self.kpi_thr = self.create_kpi_card(stats_bar, 2, 'Throughput', '0.000')
        self.kpi_tat = self.create_kpi_card(stats_bar, 3, 'Avg Turnaround Time', '0.00')
        self.kpi_wt = self.create_kpi_card(stats_bar, 4, 'Avg Waiting Time', '0.00')
        self.kpi_rt = self.create_kpi_card(stats_bar, 5, 'Avg Response Time', '0.00')

        for i in range(6):
            stats_bar.columnconfigure(i, weight=1)

        # Main Content
        main = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        left = ttk.Frame(main, width=430)
        right = ttk.Frame(main)
        main.add(left, weight=1)
        main.add(right, weight=3)

        self.setup_left_panel(left)
        self.setup_right_panel(right)
        
    # kpi card for easy review of the key points - align tutuorial's final results
    def create_kpi_card(self, parent, col, title, value):
        frame = ttk.Frame(parent, style='Surface.TFrame', padding=12)
        frame.grid(row=0, column=col, sticky='nsew', padx=6)
        ttk.Label(frame, text=title, style='CardTitle.TLabel').pack(anchor='w')
        lbl = ttk.Label(frame, text=value, style='CardValue.TLabel')
        lbl.pack(anchor='w', pady=(6, 0))
        return lbl

    def setup_left_panel(self, parent):
        panel = ttk.LabelFrame(parent, text='Process Manager', padding=14)
        panel.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        form = ttk.Frame(panel)
        form.pack(fill=tk.X, pady=(2, 10))

        ttk.Label(form, text='Arrival Time').grid(row=0, column=0, sticky='w', pady=5)
        self.arrival_entry = ttk.Entry(form, width=16)
        self.arrival_entry.grid(row=0, column=1, sticky='ew', padx=8, pady=5)

        ttk.Label(form, text='Burst Time').grid(row=1, column=0, sticky='w', pady=5)
        self.burst_entry = ttk.Entry(form, width=16)
        self.burst_entry.grid(row=1, column=1, sticky='ew', padx=8, pady=5)

        ttk.Label(form, text='Priority').grid(row=2, column=0, sticky='w', pady=5)
        self.priority_entry = ttk.Entry(form, width=16)
        self.priority_entry.grid(row=2, column=1, sticky='ew', padx=8, pady=5)
        self.priority_entry.insert(0, '0')
        form.columnconfigure(1, weight=1)

        for entry in (self.arrival_entry, self.burst_entry, self.priority_entry):
            entry.bind('<Return>', lambda e: self.add_or_update_process())

        quick = ttk.Frame(panel)
        quick.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(quick, text='➕ Add / Update', style='Primary.TButton', command=self.add_or_update_process).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(quick, text='🎲 Random', command=self.add_random_process).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        edit = ttk.Frame(panel)
        edit.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(edit, text='✏️ Edit Selected', command=self.load_selected_for_edit).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(edit, text='🧹 Clear Form', command=self.clear_form).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        io = ttk.Frame(panel)
        io.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(io, text='📂 Import CSV', command=self.import_csv).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(io, text='💾 Export CSV', command=self.export_csv).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        sample = ttk.Frame(panel)
        sample.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(sample, text='📚 Load Sample Set', style='Accent.TButton', command=self.load_sample_processes).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(sample, text='🧨 Clear All', command=self.clear_all_processes).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        columns = ('PID', 'Arrival', 'Burst', 'Priority')
        self.process_tree = ttk.Treeview(panel, columns=columns, show='headings', height=14)
        for col, width in [('PID', 60), ('Arrival', 95), ('Burst', 90), ('Priority', 90)]:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=width, anchor='center')
        self.process_tree.pack(fill=tk.BOTH, expand=True)
        self.process_tree.bind('<<TreeviewSelect>>', self.on_process_select)
        self.process_tree.bind('<Double-1>', lambda e: self.load_selected_for_edit())

        bottom = ttk.Frame(panel)
        bottom.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(bottom, text='🗑️ Delete Selected', command=self.delete_selected).pack(fill=tk.X)

    def setup_right_panel(self, parent):
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook = notebook

        dash = ttk.Frame(notebook, padding=10)
        compare = ttk.Frame(notebook, padding=10)
        logf = ttk.Frame(notebook, padding=10)
        resultf = ttk.Frame(notebook, padding=10)
        notebook.add(dash, text='Dashboard')
        notebook.add(compare, text='Comparison')
        notebook.add(logf, text='Execution Log')
        notebook.add(resultf, text='Result Table')

        desc_frame = ttk.LabelFrame(dash, text='Algorithm Description', padding=10)
        desc_frame.pack(fill=tk.X, pady=(0, 10))
        self.desc_title = ttk.Label(desc_frame, text='FCFS', style='CardValue.TLabel')
        self.desc_title.pack(anchor='w')
        self.desc_label = ttk.Label(desc_frame, text=self.algorithm_descriptions['FCFS'], style='Desc.TLabel')
        self.desc_label.pack(anchor='w', pady=(4, 0))

        self.algo_var = tk.StringVar(value='FCFS')
        ctrl = ttk.Frame(dash)
        ctrl.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(ctrl, text='Algorithm:').pack(side=tk.LEFT)
        algo_box = ttk.Combobox(ctrl, textvariable=self.algo_var, values=self.algorithms, state='readonly', width=24)
        algo_box.pack(side=tk.LEFT, padx=6)
        algo_box.bind('<<ComboboxSelected>>', lambda e: self.on_algorithm_change())

        ttk.Label(ctrl, text='Round Robin Quantum:').pack(side=tk.LEFT, padx=(18, 6))
        self.rr_quantum_entry = ttk.Entry(ctrl, width=6)
        self.rr_quantum_entry.pack(side=tk.LEFT)
        self.rr_quantum_entry.insert(0, '2')

        gantt_frame = ttk.LabelFrame(dash, text='Gantt Chart', padding=8)
        gantt_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.fig_gantt, self.ax_gantt = plt.subplots(figsize=(11.5, 3.0))
        self.fig_gantt.patch.set_facecolor('#ffffff')
        self.canvas_gantt = FigureCanvasTkAgg(self.fig_gantt, master=gantt_frame)
        self.canvas_gantt.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        metrics_frame = ttk.LabelFrame(dash, text='Performance Summary', padding=8)
        metrics_frame.pack(fill=tk.BOTH, expand=True)
        self.metrics_text = tk.Text(metrics_frame, wrap=tk.NONE, font=('Consolas', 10), height=12, bg='#f8fafc', relief='flat', bd=0)
        self.metrics_text.pack(fill=tk.BOTH, expand=True)

        self.fig_comp, axes = plt.subplots(2, 2, figsize=(12, 7))
        self.ax_awt, self.ax_art = axes[0]
        self.ax_atat, self.ax_util = axes[1]
        self.fig_comp.patch.set_facecolor('#ffffff')
        self.canvas_comp = FigureCanvasTkAgg(self.fig_comp, master=compare)
        self.canvas_comp.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.log_tree = ttk.Treeview(logf, columns=('Time', 'Event', 'Running', 'Ready Queue'), show='headings')
        for col, width, anchor in [('Time', 90, 'center'), ('Event', 190, 'w'), ('Running', 110, 'center'), ('Ready Queue', 450, 'w')]:
            self.log_tree.heading(col, text=col)
            self.log_tree.column(col, width=width, anchor=anchor)
        scroll1 = ttk.Scrollbar(logf, orient=tk.VERTICAL, command=self.log_tree.yview)
        self.log_tree.configure(yscrollcommand=scroll1.set)
        self.log_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll1.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_tree = ttk.Treeview(resultf, columns=('PID', 'Arrival', 'Burst', 'Priority', 'Start', 'Completion', 'TAT', 'WT', 'RT'), show='headings')
        for col, width in [('PID', 60), ('Arrival', 85), ('Burst', 80), ('Priority', 80), ('Start', 80), ('Completion', 95), ('TAT', 80), ('WT', 80), ('RT', 80)]:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=width, anchor='center')
        scroll2 = ttk.Scrollbar(resultf, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scroll2.set)
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll2.pack(side=tk.RIGHT, fill=tk.Y)

    def on_algorithm_change(self):
        algo = self.algo_var.get()
        self.desc_title.config(text=algo)
        self.desc_label.config(text=self.algorithm_descriptions.get(algo, ''))
        self.update_display()
        
    # clear the form for new input
    def clear_form(self):
        self.arrival_entry.delete(0, tk.END)
        self.burst_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.priority_entry.insert(0, '0')
        self.editing_pid = None
        self.arrival_entry.focus()

    def add_or_update_process(self):
        try:
            arrival = float(self.arrival_entry.get())
            burst = int(float(self.burst_entry.get()))
            priority = int(self.priority_entry.get())
            if arrival < 0 or burst <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror('Invalid Input', 'Arrival must be >= 0, burst must be a positive integer, and priority must be an integer.')
            return

        from models import Process
        if self.editing_pid is None:
            p = Process(self.next_pid, arrival, burst, priority)
            self.processes.append(p)
            self.next_pid += 1
        else:
            p = self.find_process_by_pid(self.editing_pid)
            if p is None:
                messagebox.showerror('Error', 'Selected process was not found.')
                self.editing_pid = None
                return
            p.arrival_time = arrival
            p.burst_time = burst
            p.priority = priority
            p.reset()

        self.refresh_process_tree()
        self.clear_form()

    def add_random_process(self):
        self.arrival_entry.delete(0, tk.END)
        self.arrival_entry.insert(0, str(random.randint(0, 12)))
        self.burst_entry.delete(0, tk.END)
        self.burst_entry.insert(0, str(random.randint(1, 10)))
        self.priority_entry.delete(0, tk.END)
        self.priority_entry.insert(0, str(random.randint(0, 5)))
        self.add_or_update_process()

    def load_sample_processes(self):
        from models import Process
        self.processes = [
            Process(1, 0, 12, 0),
            Process(2, 4, 6, 0),
            Process(3, 10, 2, 0)
        ]
        self.next_pid = 4
        self.refresh_process_tree()
        self.clear_form()

    def on_process_select(self, event=None):
        selected = self.process_tree.selection()
        self.selected_pid = self.process_tree.item(selected[0])['values'][0] if selected else None

    def load_selected_for_edit(self):
        self.on_process_select()
        if not self.selected_pid:
            messagebox.showinfo('Edit Process', 'Select a process first.')
            return
        p = self.find_process_by_pid(self.selected_pid)
        if p is None:
            return
        self.editing_pid = p.pid
        self.arrival_entry.delete(0, tk.END)
        self.arrival_entry.insert(0, str(p.arrival_time))
        self.burst_entry.delete(0, tk.END)
        self.burst_entry.insert(0, str(p.burst_time))
        self.priority_entry.delete(0, tk.END)
        self.priority_entry.insert(0, str(p.priority))
        self.arrival_entry.focus()

    def delete_selected(self):
        self.on_process_select()
        if not self.selected_pid:
            messagebox.showinfo('Delete', 'Select a process first.')
            return
        self.processes = [p for p in self.processes if p.pid != self.selected_pid]
        if self.editing_pid == self.selected_pid:
            self.clear_form()
        self.selected_pid = None
        self.refresh_process_tree()

    def clear_all_processes(self):
        if messagebox.askyesno('Clear All', 'Clear all processes?'):
            self.processes.clear()
            self.next_pid = 1
            self.selected_pid = None
            self.editing_pid = None
            self.refresh_process_tree()
            self.clear_form()

    def refresh_process_tree(self):
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        for p in sorted(self.processes, key=lambda x: x.pid):
            self.process_tree.insert('', 'end', values=(p.pid, f'{p.arrival_time:.1f}', p.burst_time, p.priority))

    def find_process_by_pid(self, pid):
        for p in self.processes:
            if p.pid == pid:
                return p
        return None

    def export_csv(self):
        if not self.processes:
            messagebox.showwarning('Warning', 'No processes to export.')
            return
        filepath = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
        if not filepath:
            return
        from utils import export_csv
        export_csv(filepath, self.processes)
        messagebox.showinfo('Success', 'Input data exported successfully.')

    def import_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        if not filepath:
            return
        try:
            from utils import import_csv
            self.processes = import_csv(filepath)
            self.next_pid = len(self.processes) + 1
            self.refresh_process_tree()
            self.clear_form()
            messagebox.showinfo('Success', 'CSV imported successfully.')
        except Exception as e:
            messagebox.showerror('Import Error', f'Failed to read CSV: {e}')

    def get_deep_copy(self):
        return copy.deepcopy(self.processes)

    def run_algorithms(self):
        if not self.processes:
            messagebox.showwarning('Warning', 'Add processes to simulate.')
            return
        try:
            quantum = int(self.rr_quantum_entry.get())
            if quantum <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning('Warning', 'RR quantum must be a positive integer. Using 2.')
            quantum = 2
            self.rr_quantum_entry.delete(0, tk.END)
            self.rr_quantum_entry.insert(0, '2')

        self.results['FCFS'] = self.scheduler(self.get_deep_copy(), 'FCFS')
        self.results['SJF (NP)'] = self.scheduler(self.get_deep_copy(), 'SJF_NP')
        self.results['SRTF (Preemptive)'] = self.scheduler(self.get_deep_copy(), 'SRTF')
        self.results['Round Robin'] = self.scheduler(self.get_deep_copy(), 'RR', quantum=quantum)
        self.results['Priority (NP)'] = self.scheduler(self.get_deep_copy(), 'PRIORITY_NP')
        self.results['Priority (Preemptive)'] = self.scheduler(self.get_deep_copy(), 'PRIORITY_P')

        self.update_display()
        self.update_comparison_chart()

    def update_display(self):
        algo = self.algo_var.get()
        self.desc_title.config(text=algo)
        self.desc_label.config(text=self.algorithm_descriptions.get(algo, ''))
        if algo not in self.results or not self.results[algo]:
            return
        data = self.results[algo]

        self.kpi_algo.config(text=algo)
        self.kpi_util.config(text=f"{data['util']:.1f}%")
        self.kpi_thr.config(text=f"{data['thr']:.3f}")
        self.kpi_tat.config(text=f"{data['atat']:.2f}")
        self.kpi_wt.config(text=f"{data['awt']:.2f}")
        self.kpi_rt.config(text=f"{data['art']:.2f}")

        stats = []
        stats.append(f'Algorithm: {algo}')
        stats.append('─' * 112)
        stats.append(f"{'PID':<5} | {'Arrival':<8} | {'Burst':<6} | {'Priority':<8} | {'Start':<6} | {'Comp':<6} | {'TAT':<6} | {'WT':<6} | {'RT':<6}")
        stats.append('─' * 112)
        for p in data['procs']:
            stats.append(f"P{p.pid:<4} | {p.arrival_time:<8.1f} | {p.burst_time:<6d} | {p.priority:<8d} | {p.start_time:<6.1f} | {p.completion_time:<6.1f} | {p.turnaround_time:<6.1f} | {p.waiting_time:<6.1f} | {p.response_time:<6.1f}")
        stats.append('─' * 112)
        
        stats.append(
            f"{'AVG':<5} | {'-':<8} | {'-':<6} | {'-':<8} | {'-':<6} | {'-':<6} | "
            f"{data['atat']:<6.2f} | {data['awt']:<6.2f} | {data['art']:<6.2f}"
        )
        stats.append('─' * 112)
        
        stats.append(f"Average Turnaround Time:     {data['atat']:.2f}")
        stats.append(f"Average Waiting Time:        {data['awt']:.2f}")
        stats.append(f"Average Response Time:       {data['art']:.2f}")
        stats.append(f"Busy Time:                   {data['busy_time']:.1f}")
        stats.append(f"Idle Time:                   {data['idle_time']:.1f}")
        stats.append(f"Active Span:                 {data['active_span']:.1f}")
        stats.append(f"CPU Utilization:             {data['util']:.1f}%")
        stats.append(f"System Throughput:           {data['thr']:.3f} processes/unit time")

        self.metrics_text.delete('1.0', tk.END)
        self.metrics_text.insert(tk.END, '\n'.join(stats))


        self.metrics_text.tag_configure(
            'avg_row',
            background='#dbeafe',
            foreground='#1e3a8a',
            font=('Consolas', 10, 'bold')
        )
        lines = self.metrics_text.get('1.0', tk.END).splitlines()
        for i, line in enumerate(lines, start=1):
            if line.strip().startswith('AVG'):
                self.metrics_text.tag_add('avg_row', f'{i}.0', f'{i}.end')
                break
            
            
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)
        for t, event, running, rq in data['log']:
            self.log_tree.insert('', 'end', values=(f'{t:.1f}', event, running, rq))

        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        for p in data['procs']:
            self.result_tree.insert('', 'end', values=(p.pid, f'{p.arrival_time:.1f}', p.burst_time, p.priority, f'{p.start_time:.1f}', f'{p.completion_time:.1f}', f'{p.turnaround_time:.1f}', f'{p.waiting_time:.1f}', f'{p.response_time:.1f}'))

        self.result_tree.tag_configure(
            'avg_row',
            background='#dbeafe',
            foreground='#1e3a8a',
            font=('Consolas', 10, 'bold')
        )
        
        self.result_tree.insert(
            '', 'end',
            values=('AVG', '-', '-', '-', '-', '-', f"{data['atat']:.2f}", f"{data['awt']:.2f}", f"{data['art']:.2f}"),
            tags=('avg_row',)
        )


        self.ax_gantt.clear()
        self.ax_gantt.set_title(f'Gantt Chart - {algo}', pad=12, fontsize=12, fontweight='bold')
        self.ax_gantt.set_xlabel('Time Units')
        self.ax_gantt.set_yticks([5])
        self.ax_gantt.set_yticklabels(['CPU'])
        self.ax_gantt.grid(True, alpha=0.25, axis='x')
        self.ax_gantt.set_facecolor('#ffffff')

        for entry in data['gantt']:
            duration = entry.end_time - entry.start_time
            if entry.pid == -1:
                self.ax_gantt.broken_barh([(entry.start_time, duration)], (0, 10), facecolors=self.theme['idle'], hatch='//', edgecolor='#94a3b8')
                self.ax_gantt.text(entry.start_time + duration / 2, 5, 'IDLE', ha='center', va='center', fontsize=8, color='#334155')
            else:
                color = self.colors[(entry.pid - 1) % len(self.colors)]
                self.ax_gantt.broken_barh([(entry.start_time, duration)], (0, 10), facecolors=color, edgecolor='white', linewidth=1.2, alpha=0.95)
                self.ax_gantt.text(entry.start_time + duration / 2, 5, f'P{entry.pid}', ha='center', va='center', color='white', fontweight='bold')

        self.ax_gantt.set_xlim(0, max(1, data['total_time'] + 1))
        self.ax_gantt.xaxis.set_major_locator(MultipleLocator(1))
        self.fig_gantt.tight_layout()
        self.canvas_gantt.draw()

    def update_comparison_chart(self):
        if not self.results.get('FCFS'):
            return
        algos = list(self.results.keys())
        x = list(range(len(algos)))
        atat = [self.results[a]['atat'] for a in algos]
        awt = [self.results[a]['awt'] for a in algos]
        art = [self.results[a]['art'] for a in algos]
        util = [self.results[a]['util'] for a in algos]

        charts = [
            (self.ax_atat, atat, 'Average Turnaround Time', '#16a34a'),
            (self.ax_awt, awt, 'Average Waiting Time', '#2563eb'),
            (self.ax_art, art, 'Average Response Time', '#d97706'),
            (self.ax_util, util, 'CPU Utilization (%)', '#7c3aed')
        ]

        for ax, values, title, color in charts:
            ax.clear()
            bars = ax.bar(x, values, color=color, alpha=0.88, width=0.62)
            ax.set_title(title, fontsize=11, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(algos, rotation=30, ha='right')
            ax.grid(axis='y', alpha=0.25)
            ax.set_facecolor('#ffffff')
            ax.bar_label(bars, fmt='%.1f', padding=3, fontsize=9)
            for spine in ax.spines.values():
                spine.set_color('#dbe3ef')

        self.fig_comp.tight_layout()
        self.canvas_comp.draw()

    def _ensure_results(self):
        if not any(self.results[a] for a in self.algorithms):
            self.run_algorithms()
        return any(self.results[a] for a in self.algorithms)

    def export_results_excel(self):
        if not self._ensure_results():
            return
        filepath = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel Workbook', '*.xlsx')])
        if not filepath:
            return
        self.exporter.export_to_excel(filepath, self.fig_comp)
        messagebox.showinfo('Export Complete', 'Results exported to Excel successfully.')

    def export_results_pdf(self):
        if not self._ensure_results():
            return
        filepath = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF files', '*.pdf')], title="Save Simulation Report")
        if not filepath:
            return
        try:
            self.exporter.export_to_pdf(filepath, self.fig_comp)
            messagebox.showinfo('Success', f'Report saved to:\n{filepath}')
        except Exception as e:
            messagebox.showerror('Export Error', f'An error occurred during export: {str(e)}')
    
