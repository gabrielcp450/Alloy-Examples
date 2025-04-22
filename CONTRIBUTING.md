# Contributing to Alloy Examples

Thank you for your interest in contributing to the Alloy Examples repository! This document provides guidelines and instructions for adding new examples or improving existing ones.

## Table of Contents
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Structure of an Example](#structure-of-an-example)
- [Coding Style](#coding-style)
- [Documentation](#documentation)
- [TLA+ to Alloy Conversion Guidelines](#tla-to-alloy-conversion-guidelines)
- [Submitting Your Contribution](#submitting-your-contribution)

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/Alloy-Examples.git`
3. Create a new branch for your work: `git checkout -b my-new-example`

## How to Contribute

You can contribute in several ways:
1. Adding a new Alloy specification
2. Converting an existing TLA+ specification to Alloy
3. Improving documentation for existing examples
4. Creating visualizations or comparison analysis
5. Fixing errors in existing specifications

## Structure of an Example

Each example should be placed in its own directory under `specifications/` with the following structure:

```
specifications/
└── YourExampleName/
    ├── README.md          # Description and documentation
    ├── YourExample.als    # Alloy specification file
    ├── comparison.md      # (Optional) Comparison with TLA+ version
    └── visualization.png  # (Optional) Example visualization
```

## Coding Style

When writing Alloy specifications:

1. Use meaningful variable and predicate names
2. Add comments to explain complex logic
3. Use proper indentation (2 or 4 spaces)
4. Include a module declaration at the top
5. Group related predicates and functions together
6. Include example runs and assertions to demonstrate properties

## Documentation

Each example should include:

1. A clear description of what the specification models
2. Instructions for running the model
3. Explanation of key properties and assertions
4. Expected results when running the model
5. Credits to original authors if converting from TLA+ or other sources

## TLA+ to Alloy Conversion Guidelines

When converting TLA+ specifications to Alloy:

1. Maintain the same behavior and properties as the original
2. Document key differences in modeling approaches
3. Explain how TLA+ concepts map to Alloy concepts
4. Include a comparison of verification approaches
5. Reference the original TLA+ specification

## Submitting Your Contribution

1. Commit your changes with clear, descriptive commit messages
2. Push your branch to your fork
3. Submit a pull request with a description of your contribution

Your contribution will be reviewed, and you may be asked to make changes before it's accepted.

Thank you for helping to grow the collection of Alloy examples! 