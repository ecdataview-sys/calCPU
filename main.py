import tkinter as tk
from schedulers import Scheduler
from utils import Exporter
from ui import SchedulingGUI


def main():
    root = tk.Tk()
    scheduler = Scheduler()
    exporter = Exporter(None, None, None, None, None) 
    app = SchedulingGUI(root, scheduler, exporter)    
    app.exporter.results = app.results
    app.exporter.algorithms = app.algorithms
    app.exporter.theme = app.theme
    app.exporter.colors = app.colors
    app.exporter.algorithm_descriptions = app.algorithm_descriptions
    root.mainloop()


if __name__ == '__main__':
    main()
