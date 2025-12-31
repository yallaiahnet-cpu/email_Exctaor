#!/usr/bin/env python3
"""
Simple script to generate icon files for the Chrome extension
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create an icon with the specified size"""
    # Create a new image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background (blue to cyan)
    for i in range(size):
        # Calculate gradient color
        ratio = i / size
        r = int(79 + (0 - 79) * ratio)  # 4facfe to 00f2fe
        g = int(172 + (242 - 172) * ratio)
        b = int(254 + (254 - 254) * ratio)
        
        # Draw vertical line
        draw.rectangle([(i, 0), (i+1, size)], fill=(r, g, b, 255))
    
    # Draw a simple note icon (white rectangle with lines)
    margin = size // 4
    note_width = size - 2 * margin
    note_height = size - 2 * margin
    
    # Note background (white with slight transparency)
    draw.rectangle(
        [(margin, margin), (margin + note_width, margin + note_height)],
        fill=(255, 255, 255, 230),
        outline=(255, 255, 255, 255),
        width=2
    )
    
    # Draw lines on the note (to represent text)
    line_spacing = note_height // 4
    for i in range(3):
        y = margin + (line_spacing * (i + 1))
        line_margin = margin + note_width // 8
        draw.line(
            [(line_margin, y), (margin + note_width - note_width // 8, y)],
            fill=(79, 172, 254, 200),
            width=max(1, size // 32)
        )
    
    # Save the image
    img.save(filename, 'PNG')
    print(f"Created {filename} ({size}x{size})")

def main():
    # Create icons directory if it doesn't exist
    icons_dir = 'icons'
    os.makedirs(icons_dir, exist_ok=True)
    
    # Generate icons
    sizes = [16, 48, 128]
    for size in sizes:
        filename = os.path.join(icons_dir, f'icon{size}.png')
        create_icon(size, filename)
    
    print("\n✅ All icons generated successfully!")
    print("You can now load the extension in Chrome.")

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print("Error: PIL (Pillow) is required to generate icons.")
        print("Install it with: pip install Pillow")
        print("\nAlternatively, you can:")
        print("1. Open create_icons.html in your browser")
        print("2. Generate and download the icons manually")
    except Exception as e:
        print(f"Error generating icons: {e}")

