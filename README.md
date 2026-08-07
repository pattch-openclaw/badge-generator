# Badge Generator

A simple Python script to generate 128x128 black and white PNG badges with:

- Random tiled pixel art patterns (use different seeds to generate new patterns)
- Newline support (each `\n` creates a line break)
- Auto-sizing bold font to fit all text
- Fixed font size option for manual control
- White text on black background for readability
- Decorative checkerboard border

## Usage

```bash
pip install pillow
python badge_generator.py "YOUR TEXT" [-s seed] [-f font_size]
```

## Pattern Seeds

- **Seed 1** - Vertical lines (8px tiles, alternating columns)
- **Seed 2** - Diagonal lines (8px tiles, positive slope)
- **Seed 3** - Checkerboard (16px tiles, inverted colors)
- **Seed 4** - Diagonal lines (8px tiles, negative slope)
- **Seed 5** - Hard-coded black pattern (high contrast)
- **Seed 6** - Hard-coded white pattern (minimal dots)
- **No seed** - Random noise pattern

## Examples

```bash
# Generate with random pattern (auto-sizing font)
python badge_generator.py $'CONF\n2026'

# Generate with seed 2 (diagonal lines)
python badge_generator.py $'CONF\n2026' -s 2

# Generate with specific seed
python badge_generator.py "CONF" -s 4

# Generate with fixed font size
python badge_generator.py "TEST" -f 24
```

## Options

- `-s, --seed` - Pattern seed (1-6 for specific patterns, none for random)
- `-f, --font-size` - Fixed font size (overrides auto-sizing)
