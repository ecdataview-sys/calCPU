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

3.2. Four scheduling algorithms:

    (i)  First Come First Serve (FCFS)

    (ii)  Non-Preemptive Shortest Job First (SJF)

    (iii)  Preemptive Shortest Job First (SRTF)

    (iv)  Round Robin (with single or multiple quantum comparison)
    
3.3. Per-time-unit timeline showing arrivals, context switches, and remaining burst times

3.4. Gantt chart visualization for each algorithm

3.5. Process management: add, edit, delete, and clear processes

3.6. Comparison mode for Round Robin with multiple quantum values

3.7. Detailed results including turnaround time, waiting time, response time, and averages


# 4. Requirements

4.1  I am using Python version 3.7.8.  You may use this version or higher version for running my Simulator.

4.2  Adopted the following packages. You may download and import the same, if applicable:

      (i)  tkinter (usually included with Python)

      (ii)  matplotlib

      (iii)  numpy

4.3  Install missing packages using pip:

              pip install matplotlib numpy

              
# 5. Installation

5.1  Download the source code.

5.2  Ensure all dependencies are installed.

5.3  Run the script via Python
            
            python calCPU_Lam2.py

            
# 6. How to use the Simulator

6.1. Add Processes

      (i)  Enter Arrival Time and Burst Time for each process.
      (ii)  Click Add Process to add it to the list.
      (iii)  Processes appear in the table with a unique Process ID (PID).


6.2.  Edit/Delete Processes

      (i)  Select a process in the table.
      (ii)  Use Load Selected to populate the entry fields.
            (a)  Modify values and click Update Process to save changes;
            (b)  Click Delete Selected to remove a process; or
            (c)  Use Clear All to remove all processes.


6.3. Select Algorithms

      (i)  Check the boxes for the algorithms you want to run.
      (ii)  For Round Robin, set the time quantum.
      (iii)  Enable Compare multiple RR quanta to run Round Robin with several quantum values (comma-separated).


6.4. Run Algorithms

      (i)  Click Run Selected Algorithms.
      (ii)  Progress bar indicates execution.
      (iii) Results appear in the tabs on the right:
              (a)  Gantt Chart (top right)
              (b)  Timeline Breakdown (middle right)
              (c)  Algorithm result tables (bottom right, organized by tabs)

6.5. View Different Algorithms

      (i)  Use the listbox in the left panel to select which algorithm's Gantt chart and timeline to display.
      (ii)  The corresponding tab in the results area will be highlighted.


# 7. Algorithms

7.1  First Come First Serve (FCFS)

      (i)  Non-preemptive.
      (ii)  Processes are executed in order of arrival.
      (iii)  Once a process starts, it runs to completion.

7.2  Non-Preemptive Shortest Job First (SJF)

      (i)  At each arrival, the ready queue is sorted by burst time.
      (ii)  The shortest job is selected next.
      (iii)  Running process is not preempted by a new shorter job.

7.3  Preemptive Shortest Job First (SRTF)
   
      (i)  At each time unit, the process with the smallest remaining time is selected.
      (ii)  A newly arrived process may preempt the currently running one if it has a shorter remaining time.

7.4  Round Robin (RR)

      (i)  Each process gets a fixed time quantum.
      (ii)  If a process does not finish within its quantum, it is moved to the back of the ready queue.
      (iii)  Supports single quantum or multiple quantum comparison.

7.5  Other functions
      (i)  Priority by Process (ID Smaller PID = higher priority)
      (ii)  Preemptive (a higher priority process arriving will preempt the current one)
      (iii) Priority by Age 
             

# 8. Output Interpretation

8.1  Gantt Chart: Horizontal bars show which process occupies the CPU over time.

8.2  Timeline Breakdown: Detailed per-time-unit events including arrivals, queue state, remaining times, and context switches.

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

9.3  Arrival order is tracked for age-based priority; it increments each time you add a process.

9.4  The simulator assumes time is discrete in 1-unit steps for timeline granularity.


# 10. License

10.1  This project is open-source and available under the MIT License. Feel free to modify and distribute.


# 11. Examples and Preview

<img width="1914" height="1148" alt="image" src="https://github.com/user-attachments/assets/ed8dd7e8-c5d8-4b2a-af2f-c40281d6fbe7" />

<img width="1917" height="1147" alt="image" src="https://github.com/user-attachments/assets/2c64fa28-4d32-4672-b544-21334554bfe3" />


