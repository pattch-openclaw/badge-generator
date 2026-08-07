#!/usr/bin/env python3
"""
Badge Generator - Creates 128x128 black and white PNG badges with text and pixel art.
"""

from PIL import Image, ImageDraw, ImageFont
import random
import sys


def get_builtin_fonts():
    """Return list of built-in PIL fonts with their paths."""
    return [
        ("DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ("DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("DejaVuSansMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
        ("DejaVuSerif.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
        ("FreeMono.ttf", "/usr/share/fonts/truetype/freefont/FreeMono.ttf"),
        ("FreeMonoBold.ttf", "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"),
        ("FreeSans.ttf", "/usr/share/fonts/truetype/freefont/FreeSans.ttf"),
        ("FreeSansBold.ttf", "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"),
    ]


def get_builtin_fonts_apple():
    """Return list of built-in Apple fonts."""
    return [
        ("Helvetica", "/System/Library/Fonts/Helvetica.ttc"),
        ("Helvetica-Bold", "/System/Library/Fonts/Helvetica.ttc"),
        ("HelveticaNeue", "/System/Library/Fonts/HelveticaNeue.ttc"),
        ("HelveticaNeue-Bold", "/System/Library/Fonts/HelveticaNeue.ttc"),
        ("Courier", "/System/Library/Fonts/Courier.ttc"),
        ("Courier-Bold", "/System/Library/Fonts/Courier.ttc"),
        ("LucidaGrande", "/System/Library/Fonts/LucidaGrande.ttc"),
        ("ZapfDingbats", "/System/Library/Fonts/ZapfDingbats.ttf"),
        ("Zapfino", "/System/Library/Fonts/Zapfino.ttc"),
    ]


def list_fonts():
    """List all available built-in fonts."""
    print("Built-in PIL Fonts:")
    print("-" * 40)
    fonts = get_builtin_fonts()
    for name, path in fonts:
        print(f"  {name}: {path}")
    print()
    print("Apple Fonts (macOS only):")
    print("-" * 40)
    for name, path in get_builtin_fonts_apple():
        print(f"  {name}: {path}")


def get_font(font_name, size):
    """Get a font by name at the specified size.
    
    Args:
        font_name: Font name (e.g., 'DejaVuSans', 'Helvetica', 'Courier')
        size: Font size in points
    
    Returns:
        ImageFont instance
    """
    print(f"DEBUG: get_font called with font_name='{font_name}', size={size}")
    
    # Try standard fonts
    standard_fonts = get_builtin_fonts()
    print(f"DEBUG: Checking {len(standard_fonts)} standard fonts")
    for name, path in standard_fonts:
        print(f"DEBUG:   Checking '{name}' (path: {path})")
        if font_name.lower() in name.lower():
            try:
                print(f"DEBUG:   MATCH - trying to load")
                font = ImageFont.truetype(path, size)
                print(f"DEBUG:   SUCCESS - loaded {font_name} at size {size}")
                return font
            except Exception as e:
                print(f"DEBUG:   FAILED - {e}")
                continue
    
    # Try Apple fonts
    apple_fonts = get_builtin_fonts_apple()
    print(f"DEBUG: Checking {len(apple_fonts)} Apple fonts")
    for name, path in apple_fonts:
        print(f"DEBUG:   Checking '{name}' (path: {path})")
        if font_name.lower() in name.lower():
            try:
                print(f"DEBUG:   MATCH - trying to load")
                font = ImageFont.truetype(path, size)
                print(f"DEBUG:   SUCCESS - loaded {font_name} at size {size}")
                return font
            except Exception as e:
                print(f"DEBUG:   FAILED - {e}")
                continue
    
    print(f"DEBUG: No match found, falling back to default font")
    # Fallback to default font
    return ImageFont.load_default()


def generate_pattern_seed_1(draw, width, height):
    """Vertical lines pattern - wide columns."""
    tile_size = 16
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            if x // tile_size % 2 == 0:
                draw.rectangle([x, y, x + tile_size - 1, y + tile_size - 1], fill="black")


def generate_pattern_seed_2(draw, width, height):
    """Diagonal lines pattern - wide diagonal stripes."""
    tile_size = 16
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            if (x // tile_size + y // tile_size) % 2 == 0:
                draw.rectangle([x, y, x + tile_size - 1, y + tile_size - 1], fill="black")


def generate_pattern_seed_3(draw, width, height):
    """Checkerboard with larger tiles."""
    tile_size = 16
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            if (x // tile_size + y // tile_size) % 2 == 1:
                draw.rectangle([x, y, x + tile_size - 1, y + tile_size - 1], fill="black")


def generate_pattern_seed_4(draw, width, height):
    """Diagonal lines in opposite direction."""
    tile_size = 16
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            if (x // tile_size - y // tile_size) % 2 == 0:
                draw.rectangle([x, y, x + tile_size - 1, y + tile_size - 1], fill="black")


def generate_pattern_seed_5(draw, width, height):
    """Hard-coded black pattern - all black."""
    draw.rectangle([0, 0, width - 1, height - 1], fill="black")


def generate_pattern_seed_6(draw, width, height):
    """Hard-coded white pattern - no black pixels."""
    pass  # Background is already white (color=1)


def generate_random_pattern(draw, width, height, seed=None):
    """Generate a random pixel art pattern as a tiled pattern."""
    if seed is None:
        # Default random pattern
        random.seed()
        tile_size = 16
        pattern = []
        
        for ty in range(tile_size):
            for tx in range(tile_size):
                if random.random() < 0.3:
                    pattern.append((tx, ty))
        
        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                for tx, ty in pattern:
                    px, py = x + tx, y + ty
                    if px < width and py < height:
                        draw.point((px, py), fill="black")
    elif seed == 1:
        generate_pattern_seed_1(draw, width, height)
    elif seed == 2:
        generate_pattern_seed_2(draw, width, height)
    elif seed == 3:
        generate_pattern_seed_3(draw, width, height)
    elif seed == 4:
        generate_pattern_seed_4(draw, width, height)
    elif seed == 5:
        generate_pattern_seed_5(draw, width, height)
    elif seed == 6:
        generate_pattern_seed_6(draw, width, height)
    else:
        # For other seeds, use random pattern
        random.seed(seed)
        tile_size = 16
        pattern = []
        
        for ty in range(tile_size):
            for tx in range(tile_size):
                if random.random() < 0.3:
                    pattern.append((tx, ty))
        
        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                for tx, ty in pattern:
                    px, py = x + tx, y + ty
                    if px < width and py < height:
                        draw.point((px, py), fill="black")


def parse_text_lines(text, interpret_escapes=True):
    """Parse text, respecting newline breaks. Each \n becomes a separate line.
    
    Args:
        text: Input text
        interpret_escapes: If True, interpret \n, \t, etc. as escape sequences
    """
    if interpret_escapes:
        # Interpret common escape sequences
        text = text.encode().decode('unicode_escape')
    return text.split('\n')


def find_best_font_size(font_name, text, max_width, max_height):
    """Find the largest font size that fits the text."""
    for size in range(40, 10, -2):
        print(f"DEBUG: find_best_font_size trying size={size}")
        font = get_font(font_name, size)
        lines = parse_text_lines(text)
        
        # Calculate dimensions for each line
        max_line_width = 0
        total_height = 0
        
        for line in lines:
            bbox = font.getbbox(line)
            max_line_width = max(max_line_width, bbox[2] - bbox[0])
            total_height += bbox[3] - bbox[1] + 8  # Add line spacing
        
        # Remove trailing spacing
        total_height -= 8
        
        print(f"DEBUG:   size={size}, max_line_width={max_line_width}, total_height={total_height}")
        
        if max_line_width <= max_width and total_height <= max_height:
            print(f"DEBUG:   SUCCESS - using size={size}")
            return font, lines
    
    # Fallback if nothing fits
    print(f"DEBUG:   FALLBACK - using size=12")
    return get_font(font_name, 12), [text]


def generate_badge(text, output_path="badge.png", seed=None, font_size=None, 
                   font_name="DejaVuSans", interpret_escapes=True):
    """Generate a 128x128 badge.
    
    Args:
        text: Text to display (use \n for newlines if interpret_escapes=True)
        output_path: Output file path
        seed: Random seed for pattern generation
        font_size: Fixed font size (optional, uses auto-sizing if None)
        font_name: Font name (e.g., 'DejaVuSans', 'Helvetica', 'Courier')
        interpret_escapes: If True, interpret \\n, \\t, etc. as escape sequences
    """
    print(f"DEBUG: generate_badge called with:")
    print(f"DEBUG:   text='{text}'")
    print(f"DEBUG:   output_path='{output_path}'")
    print(f"DEBUG:   seed={seed}")
    print(f"DEBUG:   font_size={font_size}")
    print(f"DEBUG:   font_name='{font_name}'")
    print(f"DEBUG:   interpret_escapes={interpret_escapes}")
    
    width, height = 128, 128
    
    img = Image.new('1', (width, height), color=1)
    draw = ImageDraw.Draw(img)
    
    # Generate pattern
    print(f"DEBUG: Generating pattern with seed={seed}")
    generate_random_pattern(draw, width, height, seed)
    
    # Find font and lines
    padding = 8
    max_text_width = width - padding * 2
    max_text_height = height - padding * 2
    
    print(f"DEBUG: max_text_width={max_text_width}, max_text_height={max_text_height}")
    
    if font_size is not None:
        print(f"DEBUG: Using fixed font_size={font_size}")
        font = get_font(font_name, font_size)
        lines = parse_text_lines(text, interpret_escapes=interpret_escapes)
    else:
        print(f"DEBUG: Finding best font size")
        font, lines = find_best_font_size(font_name, text, max_text_width, max_text_height)
    
    print(f"DEBUG: Using font={font_name} with {len(lines)} lines")
    
    # Calculate total height
    total_height = 0
    line_heights = []
    for line in lines:
        bbox = font.getbbox(line)
        line_height = bbox[3] - bbox[1]
        line_heights.append(line_height)
        total_height += line_height + 8
    total_height -= 8  # Remove trailing spacing
    
    print(f"DEBUG: total_height={total_height}")
    
    # Calculate text position for vertical centering
    y = (height - total_height) // 2
    
    print(f"DEBUG: y={y}")
    
    # Draw each line with background box for readability
    for i, line in enumerate(lines):
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        
        print(f"DEBUG:   Line {i}='{line}', x={x}, y={y}, text_width={text_width}, text_height={text_height}")
        
        # Draw text background box with proper padding (inverted color)
        draw.rectangle([x - 2, y - 2, x + text_width + 2, y + text_height + 2], fill=0)
        
        # Draw text (white on black background)
        draw.text((x, y), line, fill=1, font=font)
        y += line_heights[i] + 8
    
    img.save(output_path, "PNG")
    print(f"Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate 128x128 black and white badges")
    parser.add_argument("text", nargs="?", help="Text to display on the badge (use \\n for newlines)")
    parser.add_argument("-o", "--output", default="badge.png", help="Output file path")
    parser.add_argument("-s", "--seed", type=int, default=None, help="Pattern seed (1-6 for specific patterns)")
    parser.add_argument("-f", "--font-size", type=int, default=None, help="Fixed font size (overrides auto-sizing)")
    parser.add_argument("-n", "--font-name", default="DejaVuSans", 
                        help="Font name (e.g., DejaVuSans, Helvetica, Courier)")
    parser.add_argument("-l", "--list-fonts", action="store_true", 
                        help="List available fonts")
    parser.add_argument("--no-interpret-escapes", action="store_true", 
                        help="Don't interpret \\n as newlines")
    
    args = parser.parse_args()
    
    if args.list_fonts:
        list_fonts()
        sys.exit(0)
    
    if args.text is None:
        parser.print_help()
        sys.exit(1)
    
    interpret_escapes = not args.no_interpret_escapes
    generate_badge(args.text, args.output, seed=args.seed, font_size=args.font_size, 
                   font_name=args.font_name, interpret_escapes=interpret_escapes)
