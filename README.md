# Badge Generator

A simple Python script to generate 128x128 black and white PNG badges with:

- Random tiled pixel art patterns (use different seeds to generate new patterns)
- Newline support (each `\n` creates a line break)
- Auto-sizing bold font to fit all text
- Fixed font size option for manual control
- Custom font selection
- White text on black background for readability
- Decorative checkerboard border (disabled by default)

## Usage

```bash
pip install pillow
python badge_generator.py "YOUR TEXT" [-s seed] [-f font_size] [-n font_name]
```

## Pattern Seeds

- **Seed 1** - Vertical lines (16px tiles, alternating columns)
- **Seed 2** - Diagonal lines (16px tiles, positive slope)
- **Seed 3** - Checkerboard (16px tiles, inverted colors)
- **Seed 4** - Diagonal lines (16px tiles, negative slope)
- **Seed 5** - All black
- **Seed 6** - All white (no pattern)
- **No seed** - Random noise pattern

## Available Fonts

Run `python badge_generator.py --list-fonts` to see available fonts.

Some common options:
- `DejaVuSans` - Clean, modern sans-serif
- `DejaVuSansMono` - Monospace variant
- `Helvetica` - Classic sans-serif (macOS)
- `Courier` - Classic monospace

## Examples

```bash
# Generate with random pattern (auto-sizing font)
python badge_generator.py $'CONF\n2026'

# Generate with seed 2 (diagonal lines)
python badge_generator.py $'CONF\n2026' -s 2

# Generate with specific seed and font
python badge_generator.py $'CONF\n2026' -s 3 -n Helvetica

# Generate with fixed font size
python badge_generator.py "TEST" -f 24

# List available fonts
python badge_generator.py --list-fonts
```

## Options

- `-s, --seed` - Pattern seed (1-6 for specific patterns, none for random)
- `-f, --font-size` - Fixed font size (overrides auto-sizing)
- `-n, --font-name` - Font name (default: DejaVuSans)
- `-l, --list-fonts` - List available fonts
- `--no-interpret-escapes` - Don't interpret `\n` as newlines
