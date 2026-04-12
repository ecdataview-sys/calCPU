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

4.1  Python 3.10 or later

4.2  matplotlib

4.3  openpyxl

              
# 5. Installation

5.1  Download the source codes.

5.2  Install dependencies with:

            pip install -r requirements.txt

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


11.1 Main Layout 


<img width="940" height="590" alt="image" src="https://github.com/user-attachments/assets/eb0abfed-c6e6-4013-a66a-17b441616b7d" />

<img width="940" height="826" alt="image" src="https://github.com/user-attachments/assets/58f1b22a-2898-4765-afc0-e113715d1493" />

<img width="940" height="828" alt="image" src="https://github.com/user-attachments/assets/b7cde14b-a184-40ca-999a-7b144205762c" />

<img width="1355" height="826" alt="image" src="https://github.com/user-attachments/assets/d15c1c52-e313-459f-ac65-29ef0fc98327" />

<img width="1363" height="828" alt="image" src="https://github.com/user-attachments/assets/866100c6-6256-4621-aba4-eb682ef9588e" />



11.2 Export to Excel


<img width="799" height="461" alt="image" src="https://github.com/user-attachments/assets/876bd9c9-762d-424f-b71a-88f31553f436" />

<img width="816" height="581" alt="image" src="https://github.com/user-attachments/assets/1e44cbd2-ff75-4d01-b6e8-4b3913ee244c" />

<img width="814" height="454" alt="image" src="https://github.com/user-attachments/assets/c1a265a5-2f28-47c3-a0b4-d6f7a4a30b5d" />



11.3 Export to PDF


<img width="814" height="467" alt="image" src="https://github.com/user-attachments/assets/31c131dd-6ed4-42a1-b0d7-d9422acd17ba" />

<img width="814" height="391" alt="image" src="https://github.com/user-attachments/assets/c834f7a3-4ec4-43ec-866b-07aea36fad7c" />

<img width="814" height="636" alt="image" src="https://github.com/user-attachments/assets/fa67edd0-e673-4975-9522-6cb8221bb968" />

<img width="814" height="398" alt="image" src="https://github.com/user-attachments/assets/8169c0cc-ac34-4726-9137-7c5cb0ab281d" />

<img width="814" height="497" alt="image" src="https://github.com/user-attachments/assets/a60dd096-ed9a-4bc3-bc22-e9ebcec5ec75" />

<img width="814" height="392" alt="image" src="https://github.com/user-attachments/assets/88c74661-520f-424f-a1ca-2426f0df0a14" />




# 12. YouTube Introduction Video

[Watch the demo on YouTube](https://youtu.be/qHGrHQg-ExI)










