# Distributed Join Algorithm Shootout: "Orders & Items" 
Distributed Join Strategy Benchmark: Ship Whole Table Join vs Semi Join

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

## Scope

This project is not a complete Distributed Database Management System (DDBMS).

It is a benchmark framework designed to evaluate distributed join strategies under controlled experimental conditions.

---

## Project Structure

```text
DISTRIBUTED-JOIN-SHOOTOUT/
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

## Data Distribution

The dataset is distributed across two sites:

Site A:
Orders(OrderID, CustomerID)

Site B:
OrderItems(ItemID, OrderID, ProductID, Qty)

The join key is OrderID.

This setup simulates a distributed database where related relations are stored on different sites and must be combined through distributed query processing.

---

## Join Strategies

### Ship Whole Table Join

1. Site A requests the entire OrderItems table from Site B.
2. Site B transfers all tuples.
3. Join is executed locally at Site A.

Communication Cost:

```text
Communication Cost = Size(OrderItems)
```

---

### Semi Join

1. Site A sends only OrderID values.
2. Site B filters matching OrderItems records.
3. Site B returns only matching tuples.
4. Join is executed locally at Site A.

Communication Cost:

```text
Communication Cost = Size(OrderIDs) + Size(Matching OrderItems)
```

---

## Cost Model

According to Özsu and Valduriez:

```text
Total Cost = CPU Cost + I/O Cost + Communication Cost
```

Communication Cost can be modeled as:

```text
Communication = TMSG × Number_of_Messages + TTR × Number_of_Bytes
```

This benchmark focuses primarily on Communication Cost because distributed join performance is often dominated by data transfer between sites.

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

## Selectivity

Join selectivity represents the fraction of tuples from the participating relations that satisfy the join predicate.

In this benchmark, selectivity is controlled through the percentage of OrderItems tuples whose OrderID exists in Orders.

Examples:

Selectivity = 0.10

- 10% of OrderItems participate in the join
- 90% do not participate

Selectivity = 1.00

- All OrderItems participate in the join

Lower selectivity generally favors Semi Join because fewer tuples need to be transferred between sites.

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

## Research Goal

The primary objective of this benchmark is to identify the breakeven selectivity at which Semi Join and Ship Whole Table Join exhibit similar execution performance.

Below the breakeven point:

```text
Semi Join is expected to perform better.
```

Above the breakeven point:

```text
Ship Whole Table Join may become more efficient because Semi Join introduces additional processing overhead.
```

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

### Mean Execution Time

The middle value after sorting all execution times.

Less sensitive to outliers than the mean.

Measured using:

```python
time.perf_counter()
```

### Median Execution Time

Median execution time across all benchmark runs.

Used to reduce the influence of outliers and occasional system fluctuations.

### P99 Latency

Measures tail latency.

P99 means 99% of executions complete faster than this value.

This metric helps evaluate worst-case performance and system stability.

For example, if 100 benchmark runs are sorted by execution time, P99 corresponds approximately to the 99th percentile observation.

### Communication Cost

Measured as:

```text
Communication Cost = Total Bytes Sent + Total Bytes Received
between Site A and Site B.
```

Represents the total amount of data transferred between Site A and Site B during query execution.

### Join Result Size

Measured as:

```text
Number of rows produced by the join
```

Used to verify that both join strategies produce equivalent logical results.

---

## Expected Outcome

Semi Join should reduce communication cost significantly when selectivity is low.

As selectivity increases, the advantage of Semi Join decreases because a larger number of matching tuples must be transferred back to Site A.

The experiment aims to identify the selectivity range where Semi Join becomes more efficient than Ship Whole Table Join.

---

## Failure Scenario

The benchmark can simulate Site B unavailability during query execution.

Possible outcomes include:

- Timeout
- Connection failure
- Missing response

This demonstrates one of the key challenges of distributed database systems: dependency on remote node availability.

---

## Limitations

This benchmark is intentionally simplified.

The experiment:

- Runs on localhost
- Uses REST communication
- Uses two sites only
- Does not simulate WAN latency
- Does not include distributed query optimizers

Therefore, the results should be interpreted as comparative observations rather than absolute performance measurements for production distributed database systems.

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
