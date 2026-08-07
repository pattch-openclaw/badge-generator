#!/usr/bin/env python3
"""
Badge Generator - Creates 128x128 black and white PNG badges with text and pixel art.
"""

from PIL import Image, ImageDraw, ImageFont
import random
import sys


def generate_random_pattern(draw, width, height, seed=None):
    """Generate a random pixel art pattern as a tiled pattern."""
    if seed is not None:
        random.seed(seed)
    
    tile_size = 16
    pattern = []
    
    # Generate a single tile pattern
    for ty in range(tile_size):
        for tx in range(tile_size):
            if random.random() < 0.3:
                pattern.append((tx, ty))
    
    # Repeat the pattern across the image
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


def wrap_text(draw, text, font, max_width):
    """Wrap text to fit within max_width, breaking on whitespace."""
    words = text.split()
    if not words:
        return []
    
    lines = []
    current_line = words[0]
    
    for word in words[1:]:
        test_line = current_line + " " + word
        test_width = draw.textlength(test_line, font=font)
        if test_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    lines.append(current_line)
    return lines


def find_best_font_size(draw, text, max_width, max_height):
    """Find the largest font size that fits the text with proper wrapping."""
    for size in range(40, 10, -2):
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier.ttc", size)
        except:
            try:
                font = ImageFont.truetype("/opt/homebrew/share/fonts/DejaVuSansMono-Bold.ttf", size)
            except:
                continue
        
        lines = wrap_text(draw, text, font, max_width)
        line_height = font.getbbox('M')[3] - font.getbbox('M')[1]
        total_height = line_height * len(lines) + 8 * (len(lines) - 1)
        
        if total_height <= max_height:
            return font, lines
    
    # Fallback if nothing fits
    return ImageFont.load_default(), [text]


def generate_badge(text, output_path="badge.png", seed=None):
    """Generate a 128x128 badge."""
    width, height = 128, 128
    
    img = Image.new('1', (width, height), color=1)
    draw = ImageDraw.Draw(img)
    
    # Generate pattern
    generate_random_pattern(draw, width, height, seed)
    
    # Draw border
    draw_border(draw, width, height)
    
    # Find best font size
    padding = 8
    max_text_width = width - padding * 2
    max_text_height = height - padding * 2
    
    font, lines = find_best_font_size(draw, text, max_text_width, max_text_height)
    
    # Wrap and center text
    line_height = font.getbbox('M')[3] - font.getbbox('M')[1]
    total_height = line_height * len(lines) + 8 * (len(lines) - 1)
    
    # Calculate text position for vertical centering
    y = (height - total_height) // 2
    
    # Draw each line with background box for readability
    for line in lines:
        text_width = draw.textlength(line, font=font)
        x = (width - text_width) // 2
        
        # Draw text background box (inverted color)
        text_height = line_height
        draw.rectangle([x - 2, y - 2, x + text_width + 2, y + text_height + 2], fill=0)
        
        # Draw text (white on black background)
        draw.text((x, y), line, fill=1, font=font)
        y += line_height + 8
    
    img.save(output_path, "PNG")
    print(f"Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python badge_generator.py 'YOUR TEXT' [-s seed]")
        sys.exit(1)
    
    text = sys.argv[1]
    seed = None
    
    if len(sys.argv) >= 4 and sys.argv[2] == "-s":
        seed = int(sys.argv[3])
    
    generate_badge(text, seed=seed)
