#!/usr/bin/env nix-shell
#!nix-shell -i python -p "python3.withPackages(ps: with ps; [ matplotlib ])"

import subprocess
import re
import matplotlib.pyplot as plt
import statistics
import sys
import numpy as np

def benchmark(command, timeout):
    finished_time_ms = None
    pattern = re.compile(r"Finished in (\d+)ms")

    process = subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    try:
        process.wait(timeout)

        for line in process.stdout:
            # print(line, end='')  # Stream to terminal
            match = pattern.search(line)
            if match:
                finished_time_ms = int(match.group(1))

    except subprocess.TimeoutExpired:
        print("Timeout expired!")
        process.kill()

    if finished_time_ms is not None:
        print(f"\n✔️ Model checking time: {finished_time_ms} ms ({finished_time_ms / 1000:.3f} s)")
    else:
        print("⚠️ Could not find 'Finished in ...ms' in output.")

    return finished_time_ms


def run_benchmarks(command, n_runs=10, timeout=None):
    times = []

    for i in range(n_runs):
        print(f"\n▶️ Run {command} ({i + 1}/{n_runs})")
        time_ms = benchmark(command, timeout)
        if not time_ms: return []
        times.append(time_ms)

    return times

def modify_constants(n, i):
    result = subprocess.run(
        ["python", "change_echo.py", str(n), str(i)],
        check=True,
        capture_output=True,
        text=True
    )
    return int(result.stdout.strip())

def sum_arrays(a, b):
    if not a:  # First iteration
        return b
    elif not b:
        return a
    else:
        return [v1+v2 for v1, v2 in zip(a, b)]


def main():
    runs = 3  # Number of runs per N
    n_values = [1, 2, 3, 4]  # X-axis

    alloy_means = []
    alloy_stds = []
    tla_means = []
    tla_stds = []

    for n in n_values:
        print(f"\n================== N = {n} ==================")
        subruns_count = modify_constants(n, 0)

        command1 = "java -cp org.alloytools.alloy.dist.jar AlloyRunner.java echo.als"
        command2 = "tlc MCEcho.tla -tool -modelcheck -coverage 1 -config MCEcho.cfg"

        times1 = run_benchmarks(command1, runs)
        times2 = []
        for i in range(1, subruns_count + 1):
            print(f"\n============= N = {n} (subrun = {i}) ===============")
            modify_constants(n, i)
            times2_add = run_benchmarks(command2, runs)
            if not times2_add:
                times2 = []
                break
            times2 = sum_arrays(times2, times2_add)

        alloy_means.append(statistics.mean(times1) if len(times1) else 0)
        alloy_stds.append(statistics.stdev(times1) if len(times1) else 0)

        tla_means.append(statistics.mean(times2) if len(times2) else 0)
        tla_stds.append(statistics.stdev(times2) if len(times2) else 0)

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
        f"Alloy vs TLA+: Echo\n({runs} runs per measurement)")
    plt.xlabel("N (Problem Size)")
    plt.ylabel("Time (ms)")
    plt.xticks(x, n_values)
    plt.legend()

    # Add value labels on top of each bar
    for bars in [alloy_bars, tla_bars]:
        for bar, std in zip(bars,
                            alloy_stds if bars == alloy_bars else tla_stds):
            if bar.get_height():
                height = bar.get_height() + std + 5
                plt.text(bar.get_x() + bar.get_width() / 2.,
                        height,
                        f'{bar.get_height():.0f} ± {std:.0f}',
                        ha='center',
                        va='bottom')

    plt.grid(True, axis='y')
    plt.tight_layout()
    # plt.show()
    plt.savefig('teaching_concurrency.png', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    main()
