# Badge Generator

A simple Python script to generate 128x128 black and white PNG badges with:

- Random tiled pixel art patterns (use different seeds to generate new patterns)
- Text wrapping with auto-sizing bold font
- White text on black background for readability
- Decorative checkerboard border
- Automatic font size adjustment to fit all text

## Usage

```bash
pip install pillow
python badge_generator.py "YOUR TEXT" [-s seed]
```

## Examples

```bash
# Generate with random pattern
python badge_generator.py "CONF2026"

# Generate with specific seed
python badge_generator.py "CONF" -s 42
```

## Options

- `-s, --seed` - Random seed for pattern generation (use same seed to reproduce pattern)
