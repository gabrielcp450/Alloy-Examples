# TLA+ vs Alloy: Echo Algorithm Comparison

This document provides a detailed comparison between the TLA+ and Alloy specifications of the Echo algorithm.

## Model Structure

### TLA+ Structure
```tla
----------------------------- MODULE Echo -----------------------------
EXTENDS Naturals, FiniteSets
CONSTANTS Node, Initiator, Nbr

ASSUME /\ Initiator \in Node
       /\ Nbr \in [Node -> SUBSET Node]
       /\ \A n \in Node : Nbr[n] \subseteq Node \ {n}
       /\ \A n,m \in Node : n \in Nbr[m] <=> m \in Nbr[n]
       /\ \A n \in Node : Node \ {n} = UNION {ReachableFrom(m, Node \ {n}) : m \in Nbr[n]}

VARIABLES 
  status,     \* status[n] is "active", "idle", or "done"
  parent,     \* parent[n] = m when n received activation from m
  children    \* children[n] = set of nodes that n activated
  
vars == <<status, parent, children>>

TypeOK ==
  /\ status \in [Node -> {"idle", "active", "done"}]
  /\ parent \in [Node -> Node \cup {-1}]
  /\ children \in [Node -> SUBSET Node]
  
Init ==
  /\ status = [n \in Node |-> IF n = Initiator THEN "active" ELSE "idle"]
  /\ parent = [n \in Node |-> -1]
  /\ children = [n \in Node |-> {}]
  
SendMsg(m,n) ==
  /\ status[m] = "active"
  /\ n \in Nbr[m] \ children[m]
  /\ \/ /\ status[n] = "idle"
        /\ status' = [status EXCEPT ![n] = "active"]
        /\ parent' = [parent EXCEPT ![n] = m]
        /\ children' = [children EXCEPT ![m] = @ \cup {n}]
     \/ /\ status[n] # "idle"
        /\ children' = [children EXCEPT ![m] = @ \cup {n}]
        /\ UNCHANGED <<status, parent>>
        
Finish(n) ==
  /\ status[n] = "active"
  /\ \A p \in Nbr[n] : p \in children[n]
  /\ status' = [status EXCEPT ![n] = "done"]
  /\ UNCHANGED <<parent, children>>
  
Next ==
  \/ \E m,n \in Node : SendMsg(m,n)
  \/ \E n \in Node : Finish(n)
  
Spec == Init /\ [][Next]_vars

Termination == <>(\A n \in Node : status[n] = "done")
=======================================================================
```

### Alloy Structure
```alloy
module echo

// Node represents a network node
sig Node {
    neighbors: set Node,       // Neighboring nodes in the network
    var status: one Status,    // Current state of the node
    var parent: lone Node,     // Parent node in the spanning tree
    var children: set Node     // Children nodes in the spanning tree
}

// Status of a node in the algorithm
enum Status { Idle, Active, Done }

// Initiator node that starts the algorithm
one sig Initiator extends Node {}

// Network is connected
fact ConnectedNetwork {
    // Bidirectional links
    all n1, n2: Node | n1 in n2.neighbors iff n2 in n1.neighbors
    
    // No self loops
    all n: Node | n not in n.neighbors
    
    // Network is connected
    all n: Node - Initiator | some path: Initiator->Node | {
        first[path] = Initiator
        last[path] = n
        all i: Int | 0 <= i and i < #path - 1 implies {
            let n1 = path[i], n2 = path[add[i,1]] |
                n2 in n1.neighbors
        }
    }
}

// Initial state
pred Init {
    // Initiator is active, all other nodes are idle
    all n: Node | n.status = (n = Initiator implies Active else Idle)
    
    // No parent relationships
    no n: Node | some n.parent
    
    // No children
    all n: Node | no n.children
}

// Send a message from an active node to a neighbor
pred SendMsg[sender, receiver: Node] {
    // Sender must be active
    sender.status = Active
    
    // Receiver must be a neighbor and not already a child
    receiver in sender.neighbors - sender.children
    
    // If receiver is idle, activate it
    receiver.status = Idle implies {
        receiver.status' = Active
        receiver.parent' = sender
        all n: Node - receiver | n.status' = n.status
        all n: Node - receiver | n.parent' = n.parent
    } else {
        all n: Node | n.status' = n.status
        all n: Node | n.parent' = n.parent
    }
    
    // Add receiver to sender's children
    sender.children' = sender.children + receiver
    all n: Node - sender | n.children' = n.children
}

// Node finishes when all neighbors are children
pred Finish[n: Node] {
    // Node must be active
    n.status = Active
    
    // All neighbors must be children
    n.neighbors in n.children
    
    // Change status to done
    n.status' = Done
    all m: Node - n | m.status' = m.status
    
    // Parent and children relationships remain unchanged
    all m: Node | m.parent' = m.parent
    all m: Node | m.children' = m.children
}

// System transition
pred Next {
    some n, m: Node | SendMsg[n, m] or some n: Node | Finish[n]
}

// System behavior
fact Traces {
    Init
    always Next
}

// Eventually all nodes are done
pred Termination {
    eventually all n: Node | n.status = Done
}

// Check termination property
assert TerminationProperty {
    Termination
}

// Verify with 5 nodes
check TerminationProperty for 5 Node, 15 steps
```

## Key Differences

### Type System
- **TLA+**: Uses sets and functions to model the network structure and state
- **Alloy**: Uses signatures and relations to model the network in a more object-oriented style

### State Representation
- **TLA+**: Represents state as functions mapping nodes to their values
- **Alloy**: Represents state using variable fields in signatures

### Network Structure
- **TLA+**: Uses a function `Nbr` to map each node to its set of neighbors
- **Alloy**: Uses a relation `neighbors` directly within the Node signature

### Connectivity Verification
- **TLA+**: Uses an ASSUME statement with a complex predicate to ensure network connectivity
- **Alloy**: Uses a path-based approach to verify connectivity through transitive closure

### Message Passing
- **TLA+**: Represents message passing implicitly through state changes
- **Alloy**: Models message passing as explicit operations between nodes

### Verification Approach
- **TLA+**: Uses unbounded verification with TLC
- **Alloy**: Uses bounded verification within a specified scope

## Detailed Syntax Comparison of Key Predicates

### Key Action: Sending a Message (SendMsg)

| Alloy | TLA+ | Comments |
|-------|------|------------|
| ```alloy
pred SendMsg[sender, receiver: Node] {
    // Sender must be active
    sender.status = Active
    
    // Receiver must be a neighbor and not already a child
    receiver in sender.neighbors - sender.children
    
    // If receiver is idle, activate it
    receiver.status = Idle implies {
        receiver.status' = Active
        receiver.parent' = sender
        all n: Node - receiver | n.status' = n.status
        all n: Node - receiver | n.parent' = n.parent
    } else {
        all n: Node | n.status' = n.status
        all n: Node | n.parent' = n.parent
    }
    
    // Add receiver to sender's children
    sender.children' = sender.children + receiver
    all n: Node - sender | n.children' = n.children
}
``` | ```tla
SendMsg(m,n) ==
  /\ status[m] = "active"
  /\ n \in Nbr[m] \ children[m]
  /\ \/ /\ status[n] = "idle"
        /\ status' = [status EXCEPT ![n] = "active"]
        /\ parent' = [parent EXCEPT ![n] = m]
        /\ children' = [children EXCEPT ![m] = @ \cup {n}]
     \/ /\ status[n] # "idle"
        /\ children' = [children EXCEPT ![m] = @ \cup {n}]
        /\ UNCHANGED <<status, parent>>
``` | 1. **Parameter naming**: Alloy uses descriptive names (`sender`, `receiver`), TLA+ uses brief identifiers (`m`, `n`)
2. **State access**: Alloy uses object-field notation (`sender.status`), TLA+ uses function application (`status[m]`)
3. **Conditional structure**: Alloy uses `implies` for conditional logic, TLA+ uses disjunction (`\/`) of conjunctions
4. **Frame problem**: Alloy explicitly states what doesn't change for each element, TLA+ uses `EXCEPT` and `UNCHANGED` operators
5. **Type handling**: Alloy uses enumerated type (`Active`), TLA+ uses string literals (`"active"`) |

### Key Action: Finishing a Node (Finish)

| Alloy | TLA+ | Comments |
|-------|------|------------|
| ```alloy
pred Finish[n: Node] {
    // Node must be active
    n.status = Active
    
    // All neighbors must be children
    n.neighbors in n.children
    
    // Change status to done
    n.status' = Done
    all m: Node - n | m.status' = m.status
    
    // Parent and children relationships remain unchanged
    all m: Node | m.parent' = m.parent
    all m: Node | m.children' = m.children
}
``` | ```tla
Finish(n) ==
  /\ status[n] = "active"
  /\ \A p \in Nbr[n] : p \in children[n]
  /\ status' = [status EXCEPT ![n] = "done"]
  /\ UNCHANGED <<parent, children>>
``` | 1. **Condition expression**: Alloy uses subset relation (`in`), TLA+ uses universal quantification (`\A`)
2. **Status update**: Alloy assigns enumerated value (`Done`), TLA+ updates function with string literal (`"done"`)
3. **Frame axioms**: Alloy uses explicit statements about what remains unchanged, TLA+ uses the more concise `UNCHANGED` macro
4. **Quantification**: Alloy uses `all` quantifier, TLA+ uses the mathematical `\A` notation |

## Performance Comparison

_Note: Performance comparison data will be added once benchmarks have been conducted._

## Expressiveness

### Modeling Approach
- **TLA+**: _To be completed with actual comparison data_
- **Alloy**: _To be completed with actual comparison data_

### Verification Results
- _To be completed with actual verification results_

## Conclusion

The Echo algorithm implementation in both TLA+ and Alloy demonstrates the different modeling approaches of these languages:

- Alloy's relational model provides a different representation of network structures
- TLA+'s mathematical foundation offers a different verification approach
- Both languages can express the algorithm's core properties

The syntax comparison highlights fundamental differences in the languages:
- Alloy's object-oriented model leads to more verbose frame conditions but clearer object relationships
- TLA+'s function-based approach enables more concise state updates through the `EXCEPT` and `UNCHANGED` constructs
- Alloy requires explicit framings for each relation, while TLA+ has built-in mechanisms for this
- Alloy's type system provides better static guarantees, while TLA+'s approach offers more flexibility

_Note: This comparison will be updated with more specific insights as benchmarking and detailed analysis are completed._ 