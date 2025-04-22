# Alloy Style Guide

This document outlines the coding and style conventions used for Alloy specifications in this repository. Following these guidelines ensures consistency across examples and makes specifications more readable.

## Naming Conventions

- **Module names**: Use CamelCase for module names (e.g., `TeachingConcurrency`, `EchoAlgorithm`)
- **Signatures**: Use PascalCase for signature names (e.g., `Process`, `Node`)
- **Fields**: Use camelCase for field names (e.g., `neighbors`, `parent`)
- **Predicates and Functions**: Use camelCase for predicates and functions (e.g., `init`, `sendMsg`)
- **Variables**: Use camelCase for variables (e.g., `someNode`, `nextProcess`)

## Layout and Formatting

- Use 2 spaces for indentation
- Place opening braces on the same line as the declaration
- Group related fields, functions, and predicates together
- Use blank lines to separate logical sections of code
- Limit line length to 80 characters where possible

## Documentation

- Include a module comment at the top of each file explaining its purpose
- Document non-obvious predicates and functions with comments
- Add comments for complex constraints or assertions

## Signature Declarations

- Declare one signature per line
- Group related signatures together
- Use abstract signatures for common properties
- Use the extends keyword for hierarchical relationships
- Declare multiplicity constraints appropriately (one, lone, some, set)

Example:
```alloy
abstract sig Status {}
one sig Idle, Active, Done extends Status {}

sig Node {
  neighbors: set Node,
  var status: one Status
}
```

## Predicate and Function Declarations

- Use descriptive names that indicate what the predicate or function does
- For predicates that change state, use primed variables for post-state values
- Separate parameters with commas and a space

Example:
```alloy
pred sendMessage[sender, receiver: Node] {
  // Conditions
  sender.status = Active
  receiver in sender.neighbors
  
  // Actions
  receiver.status' = Active
  sender.sent' = sender.sent + receiver
}
```

## Fact Declarations

- Use facts to express global constraints
- Name facts to indicate what constraints they enforce
- Group related constraints in the same fact

Example:
```alloy
fact NetworkProperties {
  // Bidirectional links
  all n1, n2: Node | n1 in n2.neighbors iff n2 in n1.neighbors
  
  // No self loops
  no n: Node | n in n.neighbors
}
```

## Assertions and Commands

- Name assertions to express what property is being checked
- Use descriptive run and check commands
- Specify appropriate scopes for signatures and time steps

Example:
```alloy
assert Termination {
  Init and always Next => eventually all n: Node | n.status = Done
}

check Termination for 5 Node, 10 steps
```

## Temporal Logic

When using temporal operators:
- Use `always` for invariants
- Use `eventually` for liveness properties
- Use `until` for ordering properties

## Running Examples

Include example run commands in comments at the end of the file to help others understand how to use the specification.

## Special Conventions for this Repository

- Include a comparison section in each file that points out correlations with TLA+ where applicable
- Use consistent naming across the Alloy and TLA+ versions of the same algorithms
- Add visualization themes for consistent presentation 