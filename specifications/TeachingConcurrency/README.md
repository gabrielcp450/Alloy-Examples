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

## Detailed Comparison: Alloy vs TLA+

### Model Structure

#### TLA+ Structure
```tla
-------------------------------- MODULE SimpleAlgorithm ---------------------------------
EXTENDS Naturals, Sequences, FiniteSets
CONSTANTS N            \* Number of processes
ASSUME N \in Nat \ {0} \* N is a positive integer
Proc == 0..(N-1)       \* The set of processes

VARIABLES x, y, pc     \* pc[i] is the program counter of process i
vars == << x, y, pc >> \* All variables

TypeOK == /\ x \subseteq Proc
          /\ y \subseteq Proc
          /\ pc \in [Proc -> {"a", "b", "Done"}]

Init == /\ x = {}
        /\ y = {}
        /\ pc = [i \in Proc |-> "a"]
        
a(i) == /\ pc[i] = "a"
        /\ x' = x \cup {i}
        /\ pc' = [pc EXCEPT ![i] = "b"]
        /\ y' = y

b(i) == /\ pc[i] = "b"
        /\ IF ((i+1) % N) \in x
             THEN y' = y \cup {i}
             ELSE y' = y
        /\ pc' = [pc EXCEPT ![i] = "Done"]
        /\ x' = x

Next == \E i \in Proc : a(i) \/ b(i) \/ /\ \A j \in Proc : pc[j] = "Done"
                                         /\ UNCHANGED vars

Spec == Init /\ [][Next]_vars

Termination == <>(pc = [i \in Proc |-> "Done"])

PCorrect == [](pc = [i \in Proc |-> "Done"] => y # {})

Inv == /\ \A i \in Proc : (pc[i] \in {"b", "Done"} => i \in x)
       /\ (\E i \in Proc : pc[i] # "Done") \/ (y # {})
===================================================================================
```

#### Alloy Structure
```alloy
module Simple

open util/ordering[Process]

abstract sig PC {}
one sig a, b, Done extends PC {}

sig Process {
    var pc : one PC
}

var sig x, y in Process {}

fun succ : Process -> Process {
    Process <: (next + last->first)
}

pred Init {
    no x
    no y
    pc = Process->a
}

pred a[self: Process] {
    self.pc = a
    x' = x + self
    pc' = pc ++ self->b
    y' = y
}

pred b[self: Process] {
    self.pc = b
    succ.self in x implies y' = y + self else y' = y
    pc' = pc ++ self->Done
    x' = x
}

pred proc[self: Process] {
    a[self] or b[self]
}

pred stuttering {
    x' = x
    y' = y
    pc' = pc
}

pred Terminating {
    Process.pc = Done
    stuttering
}

pred Next {
    (some p : Process | proc[p]) or Terminating
}

fact Spec {
    Init 
    always (Next or stuttering)
}

pred Fairness {
    always eventually Next
}

check Termination {
    Fairness implies eventually Process.pc = Done
} for 3 but 1..steps

pred PCorrect {
    always {
        Process.pc = Done implies some y
    }
} 

pred Inv {
    always {
        all p : Process | (p.pc = b or p.pc = Done) implies (p in x)
        (some p : Process | p.pc != Done) or some y
    }
}

check Invariants {
    PCorrect and Inv
} for 3 but 1..steps
```

### Key Differences

#### Type System
- **TLA+**: Uses untyped set theory, requiring explicit type invariants (`TypeOK`)
- **Alloy**: Uses a strongly typed relational model with signatures defining sets and relationships

#### State Representation
- **TLA+**: Variables are defined individually and the state is represented through tuples
- **Alloy**: State is represented through relations and signature fields with implicit state transitions

#### Process Manipulation
- **TLA+**: Processes are represented as integers (0 to N-1) and manipulated using functions and sets
- **Alloy**: Processes are first-class objects (signatures) with relationships between them

#### Verification Approach
- **TLA+**: Properties verified through explicit temporal logic formulas
- **Alloy**: Properties expressed as predicates to be checked within a bounded scope

#### Successor Relation
- **TLA+**: Uses modular arithmetic `((i+1) % N)` to compute the successor
- **Alloy**: Uses `succ` function defined in terms of the ordering module

#### Syntax for State Changes
- **TLA+**: Uses primed variables and function updates with `EXCEPT`
- **Alloy**: Uses primed variables with relational operators like `+`, `-`, and override `++`

### Detailed Syntax Comparison of Key Predicates

#### Key Action: Process Step A (Adding to Set X)

| Alloy (see below) | TLA+ (see below) | Comments |
|-------------------|------------------|----------|
| See below         | See below        | 1. **Parameter representation**: Alloy uses typed objects (`self: Process`), TLA+ uses integers (`i`)<br>2. **Precondition syntax**: Alloy uses object-field notation (`self.pc = a`), TLA+ uses function application (`pc[i] = "a"`)<br>3. **Conjunction style**: Alloy uses implicit conjunction between lines, TLA+ uses explicit `/\` notation<br>4. **State updates**: Alloy uses relation operators (`+` for addition), TLA+ uses set notation (`\cup`)<br>5. **PC update**: Alloy uses override operator (`++`), TLA+ uses EXCEPT function update |

**Alloy:**
```alloy
pred a[self: Process] {
    self.pc = a
    x' = x + self
    pc' = pc ++ self->b
    y' = y
}
```

**TLA+:**
```tla
a(i) == /\ pc[i] = "a"
        /\ x' = x \cup {i}
        /\ pc' = [pc EXCEPT ![i] = "b"]
        /\ y' = y
```

#### Key Action: Process Step B (Checking Successor and Potentially Adding to Y)

| Alloy (see below) | TLA+ (see below) | Comments |
|-------------------|------------------|----------|
| See below         | See below        | 1. **Conditional syntax**: Alloy uses `implies-else` for conditional expression, TLA+ uses `IF-THEN-ELSE`<br>2. **Successor calculation**: Alloy uses declarative `succ.self` relation, TLA+ uses imperative calculation `(i+1) % N`<br>3. **Variable framing**: Alloy explicitly states unchanged variables, TLA+ does the same but with different syntax<br>4. **Type representation**: Alloy's type system allows direct manipulation of signature instances, TLA+ uses explicit set membership |

**Alloy:**
```alloy
pred b[self: Process] {
    self.pc = b
    succ.self in x implies y' = y + self else y' = y
    pc' = pc ++ self->Done
    x' = x
}
```

**TLA+:**
```tla
b(i) == /\ pc[i] = "b"
        /\ IF ((i+1) % N) \in x
             THEN y' = y \cup {i}
             ELSE y' = y
        /\ pc' = [pc EXCEPT ![i] = "Done"]
        /\ x' = x
```

### Performance Comparison
_Note: Performance comparison data will be added once benchmarks have been conducted._

### Expressiveness

#### Modeling Approach
- **TLA+**: _To be completed with actual comparison data_
- **Alloy**: _To be completed with actual comparison data_

#### Verification Results
- _To be completed with actual verification results_

### Conclusion

The Teaching Concurrency example implementation in both TLA+ and Alloy demonstrates the different modeling approaches of these languages:

- Alloy's relational model provides a different representation of concurrent processes and their interactions
- TLA+'s temporal logic approach provides a different way to specify and verify temporal properties
- Both languages can express the core properties of this concurrent algorithm

The syntax comparison highlights fundamental differences in the languages:
- Alloy's object-oriented and relational approach leads to more concise state manipulation
- TLA+'s mathematical notation provides explicit control over variable framing
- Alloy's type system eliminates the need for explicit type invariants but constrains the modeling approach
- TLA+'s untyped approach provides flexibility but requires more explicit constraints

_Note: This comparison will be updated with more specific insights as benchmarking and detailed analysis are completed._ 