# Alloy Examples

This is a repository of Alloy specifications and models covering applications in a variety of fields.
It serves as:
- a comprehensive example library demonstrating how to specify an algorithm in Alloy
- a diverse corpus facilitating development & testing of Alloy language tools
- a collection of case studies in the application of formal specification in Alloy
- a comparison between TLA+ and Alloy specifications for similar algorithms and systems

All Alloy specs can be found in the `specifications` directory.

## About Alloy and TLA+

[Alloy](https://alloytools.org/) is a language for describing structures and a tool for exploring them. It has been used in a wide range of applications from finding holes in security mechanisms to designing telephone switching networks.

[TLA+](https://lamport.azurewebsites.net/tla/tla.html) is a formal specification language developed by Leslie Lamport. It's used for designing, modeling, documenting, and verifying concurrent systems.

This repository contains examples of specifications written in Alloy, some of which are conversions from original TLA+ specifications. The purpose is to demonstrate how similar problems can be approached using both languages and to provide a comparative analysis.

## Examples Included Here

Here is a list of specifications included in this repository, with links to the relevant directory:

| Name                                                      | Original Author | TLA+ Conversion | Description                                       |
| --------------------------------------------------------- | --------------- | :-------------: | ------------------------------------------------- |
| [Teaching Concurrency](specifications/TeachingConcurrency)| Leslie Lamport  | ✓               | Simple example of concurrency specification       |
| [Echo Algorithm](specifications/echo)                     | Stephan Merz    | ✓               | A simple distributed algorithm for information dissemination |

## Directory Structure

Each specification directory typically contains:

- `*.als` - Alloy specification file(s)
- `README.md` - Description of the specification
- `comparison.md` - Comparison between Alloy and TLA+ for this specification
- Screenshots or visualizations of the Alloy instance/counterexample

## Running the Examples

To run these examples, you need the [Alloy Analyzer](https://alloytools.org/download.html).

1. Download and install Alloy Analyzer
2. Open the .als file in the Alloy Analyzer
3. Click "Execute" to run the predicate or assertion specified

## Alloy Code Style and Visualization

This repository follows consistent conventions for writing and visualizing Alloy specifications:

- [Alloy Style Guide](ALLOY_STYLE_GUIDE.md) - Conventions for writing Alloy code
- [Alloy Theme Guide](ALLOY_THEME_GUIDE.md) - Guidelines for visualizing Alloy models
- [Themes](themes/) - Standard visualization themes for Alloy Analyzer

Using these styles and themes ensures consistency across examples and makes it easier to understand and compare different specifications.

## Contributing

We welcome contributions of new Alloy specifications or conversions of existing TLA+ specifications. Please follow these guidelines:

1. Create a new directory for your specification under `specifications/`
2. Include a README.md with a description of the problem and specification
3. If converting from TLA+, include a comparison analysis
4. Include example visualizations or execution results

## License

This repository is under the MIT license.