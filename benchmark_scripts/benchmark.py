import subprocess
import re
import matplotlib.pyplot as plt
import statistics
import sys

def benchmark(command):
    finished_time_ms = None
    pattern = re.compile(r"Finished in (\d+)ms")

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        print(line, end='')  # Stream to terminal
        match = pattern.search(line)
        if match:
            finished_time_ms = int(match.group(1))

    process.wait()

    if finished_time_ms is not None:
        print(f"\n:white_check_mark: Model checking time: {finished_time_ms} ms ({finished_time_ms / 1000:.3f} s)")
    else:
        print(":warning: Could not find 'Finished in ...ms' in output.")

    return finished_time_ms

def run_benchmarks(command, n_runs=10):
    times = []
    command =  command.split()

    for i in range(n_runs):
        print(f"\n:arrow_forward: Run {i + 1}/{n_runs}")
        time_ms = benchmark(command)
        if time_ms is not None:
            times.append(time_ms)

    return times

def plot_results(times1, times2):
    mean_time1 = statistics.mean(times1)
    std_dev1 = statistics.stdev(times1) if len(times1) > 1 else 0
    mean_time2 = statistics.mean(times2)
    std_dev2 = statistics.stdev(times2) if len(times2) > 1 else 0

    plt.figure(figsize=(6, 4))
    plt.bar('Alloy', mean_time1, yerr=std_dev1, capsize=5, color='b', alpha=0.7)
    plt.bar('TLA+', mean_time2, yerr=std_dev2, capsize=5, color='b', alpha=0.7)
    plt.title('Alloy vs TLA+ (Teaching Concurrency N=10)')
    plt.ylabel('Time (ms)')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":

    # if len(sys.argv) != 2:
    #     print("Invalid Arguments:")
    #     sys.exit()

    runs = 3  # You can change this
    command = "java -cp org.alloytools.alloy.dist.jar AlloyRunner.java learning_conc-2.als"
    #sys.argv[1]
    times1 = run_benchmarks(command, runs)
    #sys.argv[2]
    command ="tlc Simple.tla -tool -modelcheck -coverage 1 -config Simple.cfg"
    times2 = run_benchmarks(command, runs)

    if times1 and times2:
        print(f"\n:bar_chart: Mean time over {len(times1)} runs: {statistics.mean(times1):.2f} ms")
        print(f"\n:bar_chart: Mean time over {len(times2)} runs: {statistics.mean(times2):.2f} ms")
        plot_results(times1, times2)
    else:
        print(":x: No valid results to plot.")
