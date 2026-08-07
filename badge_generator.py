#!/usr/bin/env python3
"""
Badge Generator - Creates 128x128 black and white PNG badges with text and pixel art.
"""

from PIL import Image, ImageDraw, ImageFont
import random
import sys


def generate_pattern_seed_1(draw, width, height):
    """Vertical lines pattern."""
    tile_size = 8
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            if x // tile_size % 2 == 0:
                draw.rectangle([x, y, x + tile_size - 1, y + tile_size - 1], fill="black")


def generate_pattern_seed_2(draw, width, height):
    """Diagonal lines pattern."""
    tile_size = 8
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
    tile_size = 8
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            if (x // tile_size - y // tile_size) % 2 == 0:
                draw.rectangle([x, y, x + tile_size - 1, y + tile_size - 1], fill="black")


def generate_pattern_seed_5(draw, width, height):
    """Hard-coded black pattern (all pixels black)."""
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                draw.point((x, y), fill="black")


def generate_pattern_seed_6(draw, width, height):
    """Hard-coded white pattern (minimal black pixels for contrast)."""
    tile_size = 32
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            # Draw a single black pixel in the center of each tile
            cx = x + tile_size // 2
            cy = y + tile_size // 2
            if cx < width and cy < height:
                draw.point((cx, cy), fill="black")


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


def draw_border(draw, width, height):
    """Draw a decorative checkerboard border."""
    border_width = 4
    
    for x in range(width):
        for y in range(height):
            if (x < border_width or x >= width - border_width or 
                y < border_width or y >= height - border_width):
                if (x + y) % 2 == 0:
                    draw.point((x, y), fill="black")


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


def get_font(size):
    """Get a bold font at the specified size, falling back to default if needed."""
    font_paths = [
        "/System/Library/Fonts/Supplemental/Courier.ttc",
        "/opt/homebrew/share/fonts/DejaVuSansMono-Bold.ttf",
    ]
    
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    
    # Fallback to default font
    return ImageFont.load_default()


def find_best_font_size(text, max_width, max_height):
    """Find the largest font size that fits the text."""
    for size in range(40, 10, -2):
        font = get_font(size)
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
        
        if max_line_width <= max_width and total_height <= max_height:
            return font, lines
    
    # Fallback if nothing fits
    return get_font(12), [text]


def generate_badge(text, output_path="badge.png", seed=None, font_size=None, interpret_escapes=True):
    """Generate a 128x128 badge.
    
    Args:
        text: Text to display (use \n for newlines if interpret_escapes=True)
        output_path: Output file path
        seed: Random seed for pattern generation
        font_size: Fixed font size (optional, uses auto-sizing if None)
        interpret_escapes: If True, interpret \\n, \\t, etc. as escape sequences
    """
    width, height = 128, 128
    
    img = Image.new('1', (width, height), color=1)
    draw = ImageDraw.Draw(img)
    
    # Generate pattern
    generate_random_pattern(draw, width, height, seed)
    
    # Draw border
    draw_border(draw, width, height)
    
    # Find font and lines
    padding = 8
    max_text_width = width - padding * 2
    max_text_height = height - padding * 2
    
    if font_size is not None:
        font = get_font(font_size)
        lines = parse_text_lines(text, interpret_escapes=interpret_escapes)
    else:
        font, lines = find_best_font_size(text, max_text_width, max_text_height)
    
    # Calculate total height
    total_height = 0
    line_heights = []
    for line in lines:
        bbox = font.getbbox(line)
        line_height = bbox[3] - bbox[1]
        line_heights.append(line_height)
        total_height += line_height + 8
    total_height -= 8  # Remove trailing spacing
    
    # Calculate text position for vertical centering
    y = (height - total_height) // 2
    
    # Draw each line with background box for readability
    for i, line in enumerate(lines):
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        
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
    parser.add_argument("text", help="Text to display on the badge (use \\n for newlines)")
    parser.add_argument("-o", "--output", default="badge.png", help="Output file path")
    parser.add_argument("-s", "--seed", type=int, default=None, help="Pattern seed (1-6 for specific patterns)")
    parser.add_argument("-f", "--font-size", type=int, default=None, help="Fixed font size (overrides auto-sizing)")
    parser.add_argument("--no-interpret-escapes", action="store_true", help="Don't interpret \\n as newlines")
    
    args = parser.parse_args()
    
    interpret_escapes = not args.no_interpret_escapes
    generate_badge(args.text, args.output, seed=args.seed, font_size=args.font_size, interpret_escapes=interpret_escapes)
