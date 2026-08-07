#!/usr/bin/env python3
"""
Badge Generator - Creates 128x128 black and white PNG badges with text and pixel art.
"""

from PIL import Image, ImageDraw, ImageFont
import random
import sys


def parse_text_lines(text):
    """Parse text, respecting newline breaks."""
    # Split on newlines - each \n becomes a separate line
    return text.split('\n')


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
        
        lines = parse_text_lines(text)
        line_height = font.getbbox('M')[3] - font.getbbox('M')[1]
        total_height = line_height * len(lines) + 8 * (len(lines) - 1)
        
        if total_height <= max_height:
            return font, lines
    
    # Fallback if nothing fits
    return ImageFont.load_default(), [text]


def generate_badge(text, output_path="badge.png", seed=None, font_size=None):
    """Generate a 128x128 badge.
    
    Args:
        text: Text to display (newlines \n create line breaks)
        output_path: Output file path
        seed: Random seed for pattern generation
        font_size: Fixed font size (optional, uses auto-sizing if None)
    """
    width, height = 128, 128
    
    img = Image.new('1', (width, height), color=1)
    draw = ImageDraw.Draw(img)
    
    # Generate pattern
    generate_random_pattern(draw, width, height, seed)
    
    # Draw border
    draw_border(draw, width, height)
    
    # Find best font size or use specified size
    padding = 8
    max_text_width = width - padding * 2
    max_text_height = height - padding * 2
    
    if font_size is not None:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier.ttc", font_size)
        except:
            try:
                font = ImageFont.truetype("/opt/homebrew/share/fonts/DejaVuSansMono-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
        lines = parse_text_lines(text)
    else:
        font, lines = find_best_font_size(draw, text, max_text_width, max_text_height)
    
    # Calculate total height
    line_height = font.getbbox('M')[3] - font.getbbox('M')[1]
    total_height = line_height * len(lines) + 8 * (len(lines) - 1)
    
    # If text doesn't fit with auto-sizing, try smaller font
    if font_size is None and total_height > max_text_height:
        for size in range(30, 10, -2):
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier.ttc", size)
            except:
                try:
                    font = ImageFont.truetype("/opt/homebrew/share/fonts/DejaVuSansMono-Bold.ttf", size)
                except:
                    continue
            lines = parse_text_lines(text)
            line_height = font.getbbox('M')[3] - font.getbbox('M')[1]
            total_height = line_height * len(lines) + 8 * (len(lines) - 1)
            if total_height <= max_text_height:
                break
    
    # Calculate text position for vertical centering
    y = (height - total_height) // 2
    
    # Draw each line with background box for readability
    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (width - text_width) // 2
        
        # Draw text background box with proper padding (inverted color)
        draw.rectangle([x - 2, y - 2, x + text_width + 2, y + text_height + 2], fill=0)
        
        # Draw text (white on black background)
        draw.text((x, y), line, fill=1, font=font)
        y += text_height + 8
    
    img.save(output_path, "PNG")
    print(f"Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate 128x128 black and white badges")
    parser.add_argument("text", help="Text to display on the badge")
    parser.add_argument("-o", "--output", default="badge.png", help="Output file path")
    parser.add_argument("-s", "--seed", type=int, default=None, help="Random seed for pattern generation")
    parser.add_argument("-f", "--font-size", type=int, default=None, help="Fixed font size (overrides auto-sizing)")
    
    args = parser.parse_args()
    
    generate_badge(args.text, args.output, seed=args.seed, font_size=args.font_size)
