#!/usr/bin/env nix-shell
#!nix-shell -i python -p "python3.withPackages(ps: with ps; [ matplotlib ])"

import subprocess
import re
import matplotlib.pyplot as plt
import statistics
import sys
import numpy as np
import os
from pathlib import Path


def benchmark(command, working_dir=None):
    finished_time_ms = None
    pattern = re.compile(r"Finished in (\d+)ms")

    process = subprocess.Popen(command.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               text=True,
                               bufsize=1,
                               cwd=working_dir)

    for line in process.stdout:
        # print(line, end='')  # Stream to terminal
        match = pattern.search(line)
        if match:
            finished_time_ms = int(match.group(1))

    process.wait()

    if finished_time_ms is not None:
        print(
            f"\n✔️ Model checking time: {finished_time_ms} ms ({finished_time_ms / 1000:.3f} s)"
        )
    else:
        print("⚠️ Could not find 'Finished in ...ms' in output.")

    return finished_time_ms


def run_benchmarks(command, n_runs=10, working_dir=None):
    times = []

    for i in range(n_runs):
        print(
            f"\n▶️ Run '{command}' ({i + 1}/{n_runs}) (workdir={working_dir})")
        time_ms = benchmark(command, working_dir)
        if time_ms is not None:
            times.append(time_ms)

    return times


def find_config_directories(base_path):
    """Find all config_Simple_n* directories"""
    return sorted(
        [d for d in os.listdir(base_path) if d.startswith("config_") and os.path.isdir(os.path.join(base_path, d))])


def find_tla_directories(base_dir, config_dir):
    """Find all subdirectories containing TLA+ files for a given config"""
    return sorted(
        [d for d in os.listdir(config_dir) if d.startswith("config_") and os.path.isdir(os.path.join(config_dir, d))])


def main():
    runs = 3  # Number of runs per N

    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = "."  # Base directory where config_Simple_n* directories are located

    # Find all N values from directory names
    config_dirs = find_config_directories(base_dir)
    print(config_dirs)
    n_values = [int(d.split('_')[-1][1:])
                for d in config_dirs]  # Extract n from "config_Simple_nX"

    alloy_means = []
    alloy_stds = []
    tla_means = []
    tla_stds = []
    tla_config_counts = []

    for config_dir, n in zip(config_dirs, n_values):
        print(f"\n================== N = {n} ==================")

        # Path to Alloy file
        alloy_file = "Simple.als"

        s = lambda s: os.path.join(script_dir, s)

        # Benchmark Alloy
        alloy_command = f"java -cp {s('org.alloytools.alloy.dist.jar')} {s('AlloyRunner.java')} {alloy_file}"
        times1 = run_benchmarks(alloy_command, runs,
                                os.path.join(base_dir, config_dir))

        if times1:
            alloy_means.append(statistics.mean(times1))
            alloy_stds.append(
                statistics.stdev(times1) if len(times1) > 1 else 0)
        else:
            alloy_means.append(0)
            alloy_stds.append(0)

        # Find all TLA+ directories for this config
        tla_dirs = find_tla_directories(base_dir,
                                        os.path.join(base_dir, config_dir))
        tla_config_counts.append(len(tla_dirs))  # Store count of TLA configs
        tla_times = []

        for tla_dir in tla_dirs:
            # Benchmark each TLA+ configuration
            tla_command = "tlc Simple.tla -tool -modelcheck -coverage 1 -config Simple.cfg"
            times = run_benchmarks(tla_command, runs,
                                   os.path.join(config_dir, tla_dir))
            if times:
                tla_times.extend(times)

        if tla_times:
            tla_means.append(statistics.mean(tla_times))
            tla_stds.append(
                statistics.stdev(tla_times) if len(tla_times) > 1 else 0)
        else:
            tla_means.append(0)
            tla_stds.append(0)

    # Plot 1: Performance comparison (original plot)
    # Plotting as side-by-side bars
    plt.figure(figsize=(10, 6))

    bar_width = 0.35
    x = np.arange(len(n_values))

    # Use lighter colors - pastel blue and coral
    alloy_color = '#7fbfff'  # Light blue
    tla_color = '#ff7f7f'  # Light red (coral)

    # Plot bars with error bars showing standard deviation
    alloy_bars = plt.bar(x - bar_width / 2,
                         alloy_means,
                         width=bar_width,
                         color=alloy_color,
                         label='Alloy',
                         yerr=alloy_stds,
                         capsize=5)
    tla_bars = plt.bar(x + bar_width / 2,
                       tla_means,
                       width=bar_width,
                       color=tla_color,
                       label='TLA+',
                       yerr=tla_stds,
                       capsize=5)

    plt.title(
        f"Alloy vs TLA+: TeachingConcurrency\n({runs} runs per measurement)")
    plt.xlabel("N (Problem Size)")
    plt.ylabel("Time (ms)")
    plt.xticks(x, n_values)
    plt.legend()

    # Add value labels on top of each bar
    for bars in [alloy_bars, tla_bars]:
        for bar, std in zip(bars,
                            alloy_stds if bars == alloy_bars else tla_stds):
            height = bar.get_height() + std + 5
            plt.text(bar.get_x() + bar.get_width() / 2.,
                     height,
                     f'{height:.0f} ± {std:.0f}',
                     ha='center',
                     va='bottom')

    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('time_comparison.png', dpi=300, bbox_inches='tight')

    # Plot 2: Configuration count (new plot)
    plt.figure(figsize=(10, 6))
    plt.bar(n_values, tla_config_counts, color='#6a9662', width=0.6)

    plt.title("Number of Generated TLA+ Configurations")
    plt.xlabel("Problem Size (N)")
    plt.ylabel("Number of Configurations")
    plt.xticks(n_values)

    # Add value labels on top of each bar
    for n, count in zip(n_values, tla_config_counts):
        plt.text(n, count + 0.001, str(count), ha='center', va='bottom')

    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('config_count.png', dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    main()
