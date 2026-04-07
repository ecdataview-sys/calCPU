# CPU Scheduling Algorithms Simulator 

# 1. Purpose of this Simulator

I am a student from the Hong Kong Metropolitan University (HKMU).  

This "CPU Scheduling Algorithms Simulator" is created for the course of "Data Structure, Algorithms, and Problem Solving" (8090SEF).

It help me study my another course, Operating System (OS) (8670SEF). 

In early 2026, the OS course teaches something about different type of CPU scheduling.  As a human, we need to be very careful each step and draw perfect gantt charts so that we could get a meaningful comparsion of the differences of different type of scheduling algorithms.  

In order to save time and do every step well, I prepared this graphical simulator for visualizing and comparing CPU scheduling algorithms. 


# 2. Key Functions

This tool allows users to input processes, run multiple scheduling algorithms simultaneously, and view detailed results including Gantt charts, per-time-unit timelines, and performance metrics.


# 3. Main Features

3.1. Interactive GUI built with Tkinter

3.2. Six Scheduling Algorithms:

    (i)  FCFS (First-Come, First-Served) - Non-preemptive

    (ii)  SJF (NP) (Shortest Job First) - Non-preemptive

    (iii)  SRTF (Shortest Remaining Time First) - Preemptive

    (iv)  Round Robin - Preemptive with configurable time quantum

    (v)  Priority (NP) - Non-preemptive priority-based

    (vi) Priority (Preemptive) - Preemptive priority-based
    
3.3. Key Functionality

    (i) Interactive Process Management - Add, edit, delete, and randomize processes
    
    (ii) CSV Import/Export - Load and save process lists
    
    (iii) Sample Data - One-click load of pre-configured test processes
    
    (iv) Real-time Visualization - Gantt charts with color-coded process execution
    
    (v) Performance Metrics - Waiting time, turnaround time, response time, CPU utilization, throughput
    
    (vi) Algorithm Comparison - Side-by-side bar charts comparing all algorithms
    
    (vii) Execution Logging - Detailed timeline of arrivals, preemptions, and completions
    
    (viii) Export Reports - Excel workbooks and PDF documents with complete results


# 4. Requirements

4.1  I am using Python version 3.7.8.  You may use this version or higher version for running my Simulator.

4.2  Adopted the following packages. You may download and import the same, if applicable:

      (i)  tkinter (usually included with Python)

      (ii)  matplotlib openpyxl

      (iii)  numpy

4.3  Install missing packages using pip:

              pip install matplotlib numpy

              
# 5. Installation

5.1  Download the source codes.

5.2  Ensure all dependencies are installed.

5.3  Run the script via Python
            
            python main.py

            
# 6. How to use the Simulator


6.1. Add Processes
        
        Fill in the form in the left panel:
        •	Arrival Time - When the process arrives (≥ 0)
        •	Burst Time - CPU time needed (positive integer)
        •	Priority - Lower number = higher priority
        
        Click "Add / Update" or press Enter.
        
6.2. Quick Setup Options
        •	Load Sample Set - Loads 5 pre-configured test processes
        •	Random - Generates a random process
        •	Import CSV - Load from CSV file
        
6.3. Select Algorithm & Run
        •	Choose an algorithm from the dropdown
        •	For Round Robin, set the time quantum (default: 2)
        •	Click "Run Simulation"
        
6.4. Explore Results
        Use the notebook tabs:
        •	Dashboard - Gantt chart and metrics for selected algorithm
        •	Comparison - Compare all six algorithms
        •	Execution Log - Timeline view
        •	Result Table - Per-process statistics
        
6.5. Export Reports
        •	Export to Excel - Complete workbook with all results and charts
        •	Export to PDF - Multi-page PDF report



# 7. Algorithms

7.1. Understanding the Metrics
        Metric              Description                                    Ideal
        Waiting Time        Time spent in ready queue	                   Lower
        Response Time	    Time until first CPU allocation	               Lower
        Turnaround Time	    Total time from arrival to completion	       Lower
        CPU Utilization	    Percentage of time CPU is busy	               Higher
        Throughput	        Processes completed per time unit	           Higher

7.2. Algorithm Selection Guide
        Use Case	                                            Recommended Algorithm
        Batch systems, simple implementation	                FCFS
        Minimizing average waiting time	                        SJF / SRTF
        Interactive/Time-sharing systems	                    Round Robin
        Real-time/Urgent tasks	                                Priority (Preemptive)
        Mixed workload analysis	                                Compare all using Comparison tab

             

# 8. Output Interpretation

8.1  Gantt Chart: Horizontal bars show which process occupies the CPU over time.

8.2  Timeline Breakdown: Detailed per-time-unit events including arrivals, queue state, remaining times.

8.3  Results Table: For each process:

      (i)  Start time
      (ii)  completion time
      (iii)  Turnaround time = completion - arrival
      (iv)  Waiting time = turnaround - burst
      (v)  Response time = first start - arrival
      (vi)  Averages: Average turnaround, waiting, and response times for the algorithm.


# 9. Points to Note

9.1  All times can be floating-point numbers.

9.2  Process IDs are assigned sequentially starting from 1.

9.3  The simulator assumes time is discrete in 1-unit steps for timeline granularity.


# 10. License

10.1  This project is open-source and available under the MIT License. Feel free to modify and distribute.


# 11. Examples and Preview

<img width="1914" height="1148" alt="image" src="https://github.com/user-attachments/assets/ed8dd7e8-c5d8-4b2a-af2f-c40281d6fbe7" />

<img width="1917" height="1147" alt="image" src="https://github.com/user-attachments/assets/2c64fa28-4d32-4672-b544-21334554bfe3" />


