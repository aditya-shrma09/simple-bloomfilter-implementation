# Static Bloom Filter Implementation in Python

A from-scratch implementation of a **Bloom Filter** in Python, benchmarked using IP addresses extracted from the CIC-IDS2017 network traffic dataset. The project evaluates memory usage, insertion time, query performance, and false-positive rate, with Python's built-in `set` as a baseline.

## Overview

A Bloom Filter is a space-efficient probabilistic data structure used to test whether an element might belong to a set.

It supports two possible query outcomes:

- **Definitely not present:** At least one required bit is unset.
- **Possibly present:** All required bits are set.

A standard Bloom Filter can produce false positives but does not produce false negatives for correctly inserted elements, assuming the filter has not been corrupted or cleared.

This project implements a Bloom Filter from scratch using Python's `hashlib`, `math`, and `bytearray` modules.

## Features

- Custom Bloom Filter implementation
- SHA-256-based hash position generation
- Configurable bit-array size and number of hash functions
- Automatic parameter calculation based on expected element count and target false-positive probability
- IP address insertion and membership queries
- False-positive rate measurement
- Insertion and query timing
- Memory comparison against Python's built-in `set`

## Project Structure

```text
simple-bloomfilter-implementation/
├── bloom_filter.py       # Bloom Filter implementation
├── main.py               # Dataset loading and benchmarks
├── ip__bf_data.csv       # Extracted source IP addresses
└── README.md
```

The dataset file is local input data and does not need to be committed to the repository.

## Dataset

The experiment uses the `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv` file from the CIC-IDS2017 dataset.

Dataset source: https://www.unb.ca/cic/datasets/ids-2017.html

For this experiment, only the `Source IP` column is extracted. Timestamps, destination IPs, and other traffic features are not used.

| Dataset statistic | Value |
|---|---:|
| Total CSV records | 286,467 |
| Unique source IP addresses | 3,667 |
| Missing source IP addresses | 0 |

The Bloom Filter is populated with unique IP addresses because repeated insertions do not introduce additional distinct elements.

## How It Works

### 1. Bit Array

The Bloom Filter stores a compact array of bits, initially set to zero.

### 2. Hashing

Each IP address is processed using SHA-256-based hashing to calculate multiple bit positions.

### 3. Insertion

The bits at the calculated positions are set to one.

### 4. Membership Query

The filter checks the same positions:

- If any bit is zero, the IP is definitely absent.
- If all bits are one, the IP might have been inserted.

### 5. False-Positive Testing

The implementation queries 10,000 randomly generated IPv4 addresses that were not inserted into the filter and measures how many return a possible match.

## Bloom Filter Configuration

The bit-array size and number of hash functions are calculated using the standard Bloom Filter sizing formulas.

For expected element count \(n\) and target false-positive probability \(p\):

\[
m=\left\lceil\frac{-n\ln(p)}{(\ln 2)^2}\right\rceil
\]

The approximate optimal number of hash functions is:

\[
k=\operatorname{round}\left(\frac{m}{n}\ln 2\right)
\]

Where:

- \(m\) is the number of bits.
- \(n\) is the expected number of unique elements.
- \(p\) is the target false-positive probability.
- \(k\) is the number of hash functions.

For this experiment, the target false-positive probability is 0.01 (1%).

## Benchmark Results

The following measurements were obtained from one run on the local Python environment.

### Bloom Filter Results

| Metric | Measured value |
|---|---:|
| Unique IP addresses inserted | 3,667 |
| Bit-array size | 35,149 bits |
| Number of hash functions | 7 |
| Bit-array storage | 4,394 bytes |
| Insertion time | 0.038839 seconds |
| False negatives | 0 |
| Absent-IP test queries | 10,000 |
| False positives | 107 |
| Measured false-positive rate | 1.07% |
| Total absent-query time | 0.121997 seconds |
| Average query time | 12.2 microseconds |

The measured false-positive rate is close to the 1% design target. Small deviations are expected due to the filter's probabilistic nature and the finite test sample.

### Comparison with Python `set`

| Metric | Custom Bloom Filter | Python `set` |
|---|---:|---:|
| Build/insertion time | 38.839 ms | 0.115 ms |
| Average absent-query time | 12.2 µs | 0.155 µs |
| False positives in 10,000 absent queries | 107 | 0 |
| False negatives | 0 | 0 |
| Reported memory | 4,394 bytes | 358,178 bytes |

**Memory comparison:** The Bloom Filter's bit array uses approximately 81.5 times less memory than the reported Python set measurement.

The memory figures are not a complete like-for-like comparison: the Bloom Filter measurement includes only the bit array, whereas the Python set measurement includes the set object and the stored IP strings.

**Query performance:** The Python set is substantially faster in this implementation. The Bloom Filter performs seven SHA-256-based hash calculations per query, so its current hashing approach has significant overhead.

These are preliminary results from a single run, not a comprehensive performance evaluation.

## Limitations

- The benchmark uses one CIC-IDS2017 CSV file rather than the complete dataset.
- The experiment uses source IP addresses only.
- The false-positive test uses randomly generated IPv4 addresses, which may not represent real network traffic distributions.
- Timings come from a single run and may vary across environments.
- The Bloom Filter's full Python object memory has not yet been measured.
- The current implementation prioritizes clarity and correctness over hashing optimization.
- The filter is static: its configuration does not automatically adapt to changing data streams.

## Future Improvements

- Repeat benchmarks and report average performance.
- Measure complete memory usage for both data structures.
- Optimize hash-position generation.
- Evaluate performance with larger datasets.
- Add visualizations of memory, latency, and false-positive rate.
- Extend the static implementation into an adaptive Bloom Filter for dynamic data streams.

## Technologies Used

- Python
- Pandas
- SHA-256 (`hashlib`)
- `bytearray`
- `time` and `sys` for performance measurements
- CIC-IDS2017 dataset

## Purpose

This project serves as a baseline implementation and benchmark for studying the trade-offs between memory usage, query performance, and probabilistic accuracy in Bloom Filters.

It is also the starting point for a larger project exploring a **Deep Learning Driven Adaptive Bloom Filter for Dynamic Data Streams**.
