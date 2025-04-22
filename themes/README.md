# Alloy Analyzer Themes

This directory contains theme files for the Alloy Analyzer that can be used to maintain consistent visualization across all examples in this repository.

## Available Themes

- `standard.thm` - The default theme recommended for most visualizations
- `trace.thm` - A theme optimized for visualizing execution traces and state transitions
- `comparison.thm` - A theme designed for side-by-side comparison visualizations

## How to Use These Themes

1. Open your Alloy specification in the Alloy Analyzer
2. Run a command to generate an instance
3. In the visualization window, click "Theme" → "Load Theme..."
4. Navigate to and select one of the theme files from this directory
5. The theme will be applied to your visualization

## Customizing Themes

If you need to customize a theme:

1. Start with one of the provided themes
2. Modify the settings as needed in the Alloy Analyzer
3. Save your modified theme using "Theme" → "Save Theme..."
4. If your customization would be useful for other examples, consider contributing it back to this repository

## Theme Settings

### Standard Theme

The standard theme uses these key settings:
- Signature shapes: Rectangle
- Atom labels: Shown
- Relation arrows: Solid lines with arrows
- Colors: Default palette with blue/green signatures

### Trace Theme

The trace theme is optimized for showing sequences:
- Time/state atoms highlighted with special colors
- Consistent layout between states
- Emphasized transitions between states

### Comparison Theme

The comparison theme is designed for comparing models:
- Higher contrast colors
- Simplified relationship display
- Emphasized differences

## Creating New Themes

When creating new themes for specific examples, follow these guidelines:

1. Start with the closest existing theme
2. Make minimal necessary changes
3. Document any significant departures from standard themes
4. Name themes descriptively, indicating their purpose

All theme files should use the `.thm` extension and include a brief comment at the top describing their purpose and any special settings. 