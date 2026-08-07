# Badge Generator

A simple Python script to generate 128x128 black and white PNG badges with:

- Random tiled pixel art patterns (use different seeds to generate new patterns)
- Newline support (each `\\n` creates a line break)
- Auto-sizing bold font to fit all text
- Fixed font size option for manual control
- White text on black background for readability
- Decorative checkerboard border

## Usage

```bash
pip install pillow
python badge_generator.py "YOUR TEXT" [-s seed] [-f font_size]
```

## Examples

```bash
# Generate with random pattern (auto-sizing font)
python badge_generator.py $'CONF\\n2026'  # Use $'...' in bash/zsh for escape sequences
python badge_generator.py "CONF\\\\n2026"  # Or double backslash

# Generate with specific seed
python badge_generator.py "CONF" -s 42

# Generate with fixed font size
python badge_generator.py "TEST" -f 24
```

## Options

- `-s, --seed` - Random seed for pattern generation (use same seed to reproduce pattern)
- `-f, --font-size` - Fixed font size (overrides auto-sizing)
- `--no-interpret-escapes` - Don't interpret escape sequences (use literal \\n)
