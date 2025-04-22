# Teaching Concurrency

## Overview
This specification demonstrates a simple concurrent system based on Leslie Lamport's paper "Teaching Concurrency" that appeared in ACM SIGACT News Volume 40, Issue 1 (March 2009), 58–62.

The original paper can be found at: http://lamport.azurewebsites.net/pubs/teaching-concurrency.pdf

## Description
The specification models a simple concurrent program where multiple processes execute a short sequence of steps:
1. First, each process adds itself to set `x`
2. Then, each process checks if its successor is in set `x` and if so, adds itself to set `y`

The specification demonstrates basic safety properties, such as ensuring that when all processes have completed, the set `y` is not empty.

## Alloy Model
The Alloy model demonstrates:
- Modeling process state using signatures
- Representing program counters as state transitions
- Using temporal logic to specify properties
- Checking invariants and temporal properties

## Running the Model
To run this model in Alloy Analyzer:
1. Open `Simple.als` in Alloy Analyzer
2. Run the `check Termination` command to verify that all processes eventually reach the "Done" state
3. Run the `check Invariants` command to verify safety properties

## Visualization
_Note: Visualization comparing execution in TLA+ vs Alloy will be added in the future._

## Alloy vs TLA+ Comparison
This specification demonstrates several key differences between Alloy and TLA+:
- Alloy uses a strongly typed system vs TLA+'s untyped approach
- Alloy's relational logic vs TLA+'s temporal logic
- Alloy's bounded model checking vs TLA+'s symbolic model checking with TLC 