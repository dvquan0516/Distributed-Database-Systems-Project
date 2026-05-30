# Distributed Join Shootout

## Overview

This project evaluates and compares two distributed join strategies in a distributed database environment:

1. **Ship Whole Table Join**
2. **Semi Join**

The experiment measures:

* Query execution time
* Communication cost (bytes transferred)
* Impact of join selectivity
* Relative performance of each strategy

The system simulates two distributed sites communicating through REST APIs.

---

## Project Structure

```text
dDISTRIBUTED-JOIN-SHOOTOUT/
│
├── benchmark/          # Benchmark engine & analysis
├── config/             # Global settings
├── data_generator/     # Synthetic dataset generator
├── node_a/             # Site A service
├── node_b/             # Site B service
├── logs/               # Runtime logs
├── results/            # Benchmark outputs & charts
├── requirements.txt
└── README.md
```

---

## Experimental Setup

### Site A

Stores relation:

```text
Orders(OrderID, CustomerID)
```

Runs on:

```text
http://localhost:5001
```

### Site B

Stores relation:

```text
OrderItems(ItemID, OrderID, ProductID, Qty)
```

Runs on:

```text
http://localhost:5002
```

Communication between sites is performed using REST APIs.

---

## Join Strategies

### Ship Whole Table Join

1. Site A requests the entire OrderItems table from Site B.
2. Site B transfers all tuples.
3. Join is executed locally at Site A.

Communication Cost:

```text
Cost = Size(OrderItems)
```

---

### Semi Join

1. Site A sends only OrderID values.
2. Site B filters matching OrderItems records.
3. Site B returns only matching tuples.
4. Join is executed locally at Site A.

Communication Cost:

```text
Cost = Size(OrderIDs) + Size(Matching OrderItems)
```

---

## Dataset Generation

Generate a dataset with a specific selectivity:

```bash
python data_generator/generate.py
```

Example configuration:

```python
generate_dataset(
    selectivity=0.5
)
```

Meaning:

```text
50% of OrderItems match Orders
50% do not match
```

---

## Installation

Create virtual environment:

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the System

### Terminal 1

Start Site A:

```bash
python node_a/app.py
```

Expected:

```text
NODE A START
Running on http://localhost:5001
```

---

### Terminal 2

Start Site B:

```bash
python node_b/app.py
```

Expected:

```text
NODE B START
Running on http://localhost:5002
```

---

### Terminal 3

Run benchmark:

```bash
python -m benchmark.run_benchmark
```

The benchmark automatically:

* Generates datasets for multiple selectivity levels
* Executes Ship Whole Table Join
* Executes Semi Join
* Repeats experiments multiple times
* Saves raw and aggregated results

---

## Benchmark Scenarios

Default selectivity values:

```python
[
    0.01,
    0.05,
    0.10,
    0.25,
    0.50,
    0.75,
    0.80,
    0.85,
    0.90,
    0.95,
    1.00
]
```

---

## Result Analysis

Generate analysis report:

```bash
python benchmark/analyzer.py
```

Output:

```text
results/report.txt
```

The report contains:

* Average execution time
* Communication cost
* Percentage improvement
* Breakeven point analysis
* Best-performing selectivity range

---

## Output Files

### Aggregated Results

```text
results/benchmark_results.csv
results/benchmark_results.json
```

### Raw Benchmark Runs

```text
results/raw/raw_runs.csv
results/raw/raw_runs.json
```

### Analysis Report

```text
results/report.txt
```

---

## Metrics

### Execution Time

Measured using:

```python
time.perf_counter()
```

### Communication Cost

Measured as:

```text
Bytes Sent + Bytes Received
```

### Join Result Size

Measured as:

```text
Number of rows produced by the join
```

---

## Expected Outcome

Semi Join should reduce communication cost significantly when selectivity is low.

As selectivity increases, the advantage of Semi Join decreases because a larger number of matching tuples must be transferred back to Site A.

The experiment aims to identify the selectivity range where Semi Join becomes more efficient than Ship Whole Table Join.

---

## References

M. Tamer Özsu, Patrick Valduriez
Principles of Distributed Database Systems, 4th Edition, Springer.

This project is based on concepts from:

* Distributed query processing
* Semi-join optimization
* Data shipping strategies
* Cost-based query optimization

---

## Author

Distributed Database Systems Project

Distributed Join Strategy Benchmark:

* Ship Whole Table Join
* Semi Join
