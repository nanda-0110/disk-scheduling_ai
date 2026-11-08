# AI-Based Disk Scheduling Simulator

This is my CSE316 (Operating Systems) CA3 project, Problem 42: AI-Based Disk Scheduling Algorithms.

## What it does
When a disk gets a bunch of read/write requests, the order we serve them in changes how much the head has to move. In this project I implemented four scheduling algorithms (FCFS, SSTF, SCAN and C-SCAN) and compared them on total seek time, average seek time and throughput.

I also added a small machine learning part. I generated 3000 random request queues, found out which algorithm was best for each one, and trained a Decision Tree to predict the best algorithm just by looking at the queue.

## How the project is split
- `engine/` has the four algorithms and the metrics code
- `ml/` makes the dataset, trains the model and does predictions
- `gui/` is the Streamlit app where you type requests and see the results

## How to run it
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m ml.dataset
python -m ml.train
streamlit run gui/app.py
```

## What I found
- SSTF gave the lowest seek time in about 93% of my test queues, so it is the best choice most of the time.
- SCAN won in the cases where the requests were spread across both ends of the disk.
- The model got about 93% accuracy. But a model that always says SSTF would score about the same, so the more useful number is how often it correctly spots the SCAN cases (about 74% of them).
- C-SCAN almost never wins here because I count the jump from one end of the disk to the other as head movement.

## Limitations
- It is only a simulation, it does not touch a real disk.
- The disk size is fixed at 200 tracks by default.
- SSTF can starve far away requests, and I did not measure fairness.

## Tools used
Python, NumPy, pandas, scikit-learn, matplotlib, Streamlit, Git and GitHub.