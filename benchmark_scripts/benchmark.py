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
        print(f"\n✔️ Model checking time: {finished_time_ms} ms ({finished_time_ms / 1000:.3f} s)")
    else:
        print("⚠️ Could not find 'Finished in ...ms' in output.")

    return finished_time_ms

def run_benchmarks(command, n_runs=10):
    times = []
    command = command.split()

    for i in range(n_runs):
        print(f"\n▶️ Run {i + 1}/{n_runs}")
        time_ms = benchmark(command)
        if time_ms is not None:
            times.append(time_ms)

    return times

def modify_constants(n):
    # Call the Python script to modify the files
    subprocess.run(["python", "changeSimple.py", str(n)], check=True)

def main():
    runs = 3  # Number of runs per N
    n_values = [1, 2, 3, 4, 5]  # X-axis

    alloy_means = []
    tla_means = []

    for n in n_values:
        print(f"\n================== N = {n} ==================")
        modify_constants(n)

        command1 = "java -cp org.alloytools.alloy.dist.jar AlloyRunner.java learning_conc-2.als"
        command2 = "tlc Simple.tla -tool -modelcheck -coverage 1 -config Simple.cfg"

        times1 = run_benchmarks(command1, runs)
        times2 = run_benchmarks(command2, runs)

        if times1:
            alloy_means.append(statistics.mean(times1))
        else:
            alloy_means.append(0)

        if times2:
            tla_means.append(statistics.mean(times2))
        else:
            tla_means.append(0)

    # Plotting
    plt.figure(figsize=(8, 5))
    plt.plot(n_values, alloy_means, marker='o', label="Alloy")
    plt.plot(n_values, tla_means, marker='s', label="TLA+")
    plt.title("Performance vs N")
    plt.xlabel("N (Problem Size)")
    plt.ylabel("Time (ms)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
