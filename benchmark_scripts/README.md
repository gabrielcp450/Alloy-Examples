# Benchmark Scripts

This directory contains Python scripts for benchmarking and comparing the performance of Alloy and TLA+ model checkers across different examples and problem sizes. These scripts are designed to provide detailed performance analysis and visualization of model checking times.

## Overview

The benchmark scripts are designed to:
- Compare execution times between Alloy and TLA+ model checkers
- Generate performance comparison graphs
- Measure model checking times across multiple runs
- Handle different problem sizes (N) to analyze scalability
- Provide statistical analysis of results
- Generate publication-quality visualizations

## Scripts

### 1. `benchmark.py`

This is the main benchmark script that handles the TeachingConcurrency example. It provides the most comprehensive benchmarking capabilities:

#### Key Features
- **Automatic Configuration Discovery**:
  - Scans for directories matching pattern `config_Simple_n*`
  - Extracts problem sizes (N) from directory names
  - Handles multiple TLA+ configurations per problem size

#### Implementation Details
- Uses `subprocess.Popen` for process management
- Implements regex pattern matching for time extraction
- Handles both stdout and stderr streams
- Provides detailed progress output during execution

#### Output Generation
- Creates two distinct plots:
  1. **Performance Comparison**:
     - Side-by-side bars for Alloy vs TLA+
     - Error bars showing standard deviation
     - Time measurements in milliseconds
     - Clear value labels on bars
  2. **Configuration Count**:
     - Shows number of TLA+ configurations per problem size
     - Helps visualize complexity growth

#### Statistical Analysis
- Performs multiple runs (default: 3) per measurement
- Calculates mean and standard deviation
- Handles failed runs gracefully
- Provides detailed progress output

### 2. `benchmark_echo.py`

This script benchmarks the Echo example with enhanced features for handling complex scenarios:

#### Key Features
- **Timeout Handling**:
  - Implements process timeout mechanism
  - Gracefully handles long-running model checks
  - Kills processes that exceed timeout limits

#### Implementation Details
- Uses `subprocess.TimeoutExpired` for timeout management
- Implements subrun handling for TLA+ configurations
- Modifies constants between runs using `change_echo.py`
- Provides detailed progress tracking

#### Special Features
- **Subrun Management**:
  - Handles multiple subruns for TLA+ configurations
  - Aggregates results from multiple subruns
  - Provides detailed progress for each subrun

### 3. `benchmark_TeachingConcurrency.py`

A streamlined version specifically for the TeachingConcurrency example:

#### Key Features
- **Simplified Configuration**:
  - Uses predefined problem sizes (N = 1, 3, 5, 7, 9)
  - Single configuration per problem size
  - Direct constant modification

#### Implementation Details
- Uses `change_TeachingConcurrency.py` for constant modification
- Implements basic benchmarking functionality
- Provides clear progress output
- Generates single performance comparison plot

## Common Features

All scripts share these common features:

### Process Management
- Uses `subprocess.Popen` for process control
- Handles both stdout and stderr streams
- Provides real-time progress output
- Implements proper process cleanup

### Statistical Analysis
- Multiple runs per measurement (default: 3)
- Standard deviation calculation
- Mean time computation
- Error bar generation


## Usage

To run any of the benchmark scripts:

```bash
# For the main benchmark
python benchmark.py

# For the Echo example
python benchmark_echo.py

# For the TeachingConcurrency example
python benchmark_TeachingConcurrency.py
```

### Command Line Arguments
Currently, the scripts use hardcoded values for:
- Number of runs (default: 3)
- Problem sizes
- Timeout values (where applicable)

## Dependencies

The scripts require:
- Python 3
- matplotlib (for visualization)
- numpy (for numerical operations)
- Java (for Alloy model checker)
- TLC (for TLA+ model checker)

### Python Package Requirements
```bash
pip install matplotlib numpy
```

## Output

The scripts generate PNG files with performance comparison graphs:

### `time_comparison.png` (from benchmark.py)
- Performance comparison between Alloy and TLA+
- Error bars showing standard deviation
- Clear value labels
- Grid lines for readability

### `config_count.png` (from benchmark.py)
- Number of TLA+ configurations per problem size
- Clear value labels
- Grid lines for readability

### `teaching_concurrency.png` (from other scripts)
- Performance comparison for specific example
- Error bars showing standard deviation
- Clear value labels
- Grid lines for readability

## Future Improvements

Potential enhancements for the benchmark scripts:
1. Command-line argument support for:
   - Number of runs
   - Problem sizes
   - Timeout values
2. Additional statistical analysis
3. Export of raw data for further analysis
4. Support for more examples
5. Automated testing
6. CI/CD integration

# Benchmark Scripts Explanation

This document explains the purpose and functionality of each benchmark script in detail.

## Script Overview

We have three main benchmark scripts, each designed for specific use cases:

1. `benchmark.py` - Main benchmark script for TeachingConcurrency
2. `benchmark_echo.py` - Specialized script for the Echo example
3. `benchmark_TeachingConcurrency.py` - Simplified version for TeachingConcurrency

## Detailed Script Explanations

### 1. `benchmark.py`

This is our most comprehensive benchmark script, designed to compare Alloy and TLA+ performance on the TeachingConcurrency example.

#### How it works:
1. **Directory Scanning**:
   - Automatically finds all directories matching `config_Simple_n*`
   - Each directory represents a different problem size (N)
   - Example: `config_Simple_n1`, `config_Simple_n2`, etc.

2. **Benchmarking Process**:
   - For each problem size:
     - Runs Alloy model checker on `Simple.als`
     - Runs TLA+ model checker on all configurations in that directory
     - Repeats each run 3 times for statistical significance
     - Measures execution time in milliseconds

3. **Time Measurement**:
   - Uses regex to extract "Finished in Xms" from output
   - Captures both stdout and stderr
   - Handles process output in real-time

4. **Data Collection**:
   - Records execution times for both tools
   - Calculates mean and standard deviation
   - Handles failed runs gracefully

### 2. `benchmark_echo.py`

This script is specifically designed for the Echo example, with special handling for complex scenarios.

#### How it works:
1. **Timeout Management**:
   - Implements a timeout mechanism for long-running checks
   - Kills processes that exceed the timeout limit
   - Prevents infinite runs

2. **Subrun Handling**:
   - For each problem size:
     - Runs Alloy on `echo.als`
     - For TLA+:
       - Runs multiple subruns using `change_echo.py`
       - Aggregates results from all subruns
       - Handles failures gracefully

3. **Constant Modification**:
   - Uses `change_echo.py` to modify constants between runs
   - Ensures proper configuration for each test case

4. **Data Collection**:
   - Records execution times for both tools
   - Handles timeout cases
   - Aggregates results from multiple subruns

### 3. `benchmark_TeachingConcurrency.py`

This is a simplified version specifically for the TeachingConcurrency example.

#### How it works:
1. **Fixed Problem Sizes**:
   - Uses predefined values: N = 1, 3, 5, 7, 9
   - No automatic directory scanning
   - Simpler configuration management

2. **Benchmarking Process**:
   - For each N:
     - Modifies constants using `change_TeachingConcurrency.py`
     - Runs Alloy on `Simple.als`
     - Runs TLA+ on `Simple.tla`
     - Repeats 3 times for each

3. **Data Collection**:
   - Records execution times for both tools
   - Calculates mean and standard deviation
   - Handles failed runs gracefully

## Common Implementation Details

All scripts share these core features:

1. **Process Management**:
   ```python
   process = subprocess.Popen(
       command.split(),
       stdout=subprocess.PIPE,
       stderr=subprocess.STDOUT,
       text=True,
       bufsize=1
   )
   ```

2. **Time Extraction**:
   ```python
   pattern = re.compile(r"Finished in (\d+)ms")
   match = pattern.search(line)
   if match:
       finished_time_ms = int(match.group(1))
   ```

3. **Statistical Analysis**:
   ```python
   mean_time = statistics.mean(times)
   std_dev = statistics.stdev(times) if len(times) > 1 else 0
   ```

## Usage Examples

1. Running the main benchmark:
   ```bash
   python benchmark.py
   ```

2. Running the Echo benchmark:
   ```bash
   python benchmark_echo.py
   ```

3. Running the simplified TeachingConcurrency benchmark:
   ```bash
   python benchmark_TeachingConcurrency.py
   ```

## Dependencies

Required software:
- Python 3
- Java (for Alloy)
- TLC (for TLA+)

Install Python dependencies:
```bash
pip install numpy
```
