# Alloy Theme Guide

This document provides guidelines for creating and using themes for Alloy visualizations. Consistent visualization themes help make examples easier to understand and compare.

## Theme Basics

Themes in the Alloy Analyzer control the visual appearance of instances, including:
- Node shapes, colors, and sizes
- Edge styles and colors
- Label formatting and placement
- Layout algorithms
- Projection controls

## Standard Themes

This repository provides several standard themes:

1. **standard.thm** - Default theme for general visualizations
2. **trace.thm** - Optimized for visualizing execution traces and state transitions
3. **comparison.thm** - Designed for side-by-side comparison between models

## Theme Selection

Choose the appropriate theme based on your model's purpose:

- Use **standard.thm** for most examples and basic visualizations
- Use **trace.thm** when visualizing states in a dynamic execution
- Use **comparison.thm** when comparing different specifications or implementations

## Visual Elements

### Signatures

- Primary signatures: Use rectangles or ovals with distinct colors
- Abstract signatures: Use lighter shades of the same color
- Singleton signatures: Use smaller shapes with darker borders

### Relations

- Core relations: Bold arrows with solid lines
- Derived relations: Thinner arrows with dashed or dotted lines
- Time-related relations: Use special colors (e.g., red for "next")

### States and Transitions

For dynamic/temporal models:
- States/Time points: Use consistent shapes (squares/circles)
- Transitions: Use directed arrows with special styling
- Initial states: Mark with distinctive colors or borders

### Layout

- Group related atoms together
- Use consistent layout for sequences and time steps
- Avoid overlapping edges where possible

## Creating Custom Themes

To create a custom theme:

1. Start with one of the standard themes
2. Open an instance visualization in Alloy Analyzer
3. Use "Theme" > "Customize..." to modify visual settings
4. Save your theme using "Theme" > "Save Theme..."

## Theme File Format

Theme files are XML-based with the following key sections:

```xml
<view>
  <defaultnode/>  <!-- Default settings for nodes -->
  <defaultedge/>  <!-- Default settings for edges -->
  
  <node>          <!-- Specific node settings -->
    <type name="SomeType"/>
    <shape name="Rectangle"/>
    <color name="Blue"/>
  </node>
  
  <edge>          <!-- Specific edge settings -->
    <relation name="someRelation"/>
    <style name="Solid"/>
    <color name="Black"/>
  </edge>
</view>
```

## Example-Specific Themes

For complex examples, you may need to create custom themes. When doing so:

1. Name the theme file descriptively (e.g., `echo_visualization.thm`)
2. Include comments in the XML explaining special visualization choices
3. Reference the theme in your example's README file

## Best Practices

- Maintain consistent coloring schemes across related examples
- Use distinct visual styles for different types of elements
- Keep visualizations clean and uncluttered
- Consider colorblind-friendly color palettes
- Use projections to focus on relevant parts of large instances

## Visualization Screenshots

When including visualization screenshots in documentation:

1. Apply the appropriate theme
2. Adjust the layout for clarity
3. Capture the visualization at a readable size
4. Include captions explaining key elements
5. Save in PNG format in the `img/` directory with descriptive names 