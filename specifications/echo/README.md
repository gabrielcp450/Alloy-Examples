# Echo Algorithm

## Overview
This specification models the Echo algorithm, a simple distributed algorithm for information dissemination in a network. The algorithm was originally specified in TLA+ by Stephan Merz.

## Description
The Echo algorithm works as follows:

1. An initiator node sends a message to all its neighbors
2. When a non-initiator node receives a message for the first time:
   - It marks the sender as its parent
   - It sends messages to all its neighbors except its parent
3. When a node receives messages from all its neighbors, it sends an acknowledgment (echo) back to its parent
4. The algorithm terminates when the initiator receives acknowledgments from all its neighbors

This algorithm is used for:
- Spanning tree construction
- Broadcast with acknowledgment
- Network exploration

## Alloy Model
The Alloy model demonstrates:
- Modeling a network topology as a graph using relations
- Representing message passing between nodes
- Modeling local state at each node
- Verifying termination and correctness properties

## Running the Model
To run this model in Alloy Analyzer:
1. Open the `Echo.als` file in Alloy Analyzer
2. Execute the model to see possible executions
3. Check termination and correctness assertions

## Visualization
_Note: Visualization of the Echo algorithm execution will be added in the future._

## Alloy vs TLA+ Comparison
The Echo algorithm specification highlights several differences between Alloy and TLA+:
- Alloy's graph representation using relations vs TLA+'s set-based encoding
- Alloy's bounded execution exploration vs TLA+'s state space exploration
- Different approaches to modeling asynchronous communication

The Alloy specification makes the network topology more explicit through its relational model, while the TLA+ version focuses more on the algorithmic steps and properties. 