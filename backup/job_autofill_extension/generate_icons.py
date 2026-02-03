#!/usr/bin/env python3
"""
Generate icons for Job Application Auto-Fill Chrome Extension
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Create an icon with a form/fill symbol"""
    # Create image with gradient background
    img = Image.new('RGB', (size, size), color='#667eea')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient effect
    for i in range(size):
        color_value = int(118 + (i / size) * 40)  # Gradient from #667eea to #764ba2
        color = (102, 126, color_value)
        draw.line([(0, i), (size, i)], fill=color)
    
    # Draw form/document symbol
    # Document outline
    doc_width = int(size * 0.5)
    doc_height = int(size * 0.6)
    doc_x = int(size * 0.25)
    doc_y = int(size * 0.2)
    
    # White document background
    draw.rectangle([doc_x, doc_y, doc_x + doc_width, doc_y + doc_height], 
                  fill='white', outline='white')
    
    # Draw lines on document (form fields)
    line_spacing = doc_height // 5
    for i in range(1, 5):
        y = doc_y + (line_spacing * i)
        draw.line([(doc_x + 5, y), (doc_x + doc_width - 5, y)], 
                 fill='#667eea', width=2)
    
    # Draw checkmark/fill symbol
    check_size = int(size * 0.15)
    check_x = doc_x + doc_width + 5
    check_y = doc_y + doc_height // 2
    
    # Green checkmark
    draw.ellipse([check_x - check_size//2, check_y - check_size//2,
                  check_x + check_size//2, check_y + check_size//2],
                fill='#28a745', outline='white', width=2)
    
    # Save icon
    img.save(output_path, 'PNG')
    print(f"Created {output_path} ({size}x{size})")

def main():
    # Create icons directory if it doesn't exist
    icons_dir = 'icons'
    os.makedirs(icons_dir, exist_ok=True)
    
    # Generate icons in different sizes
    sizes = [16, 48, 128]
    for size in sizes:
        output_path = os.path.join(icons_dir, f'icon{size}.png')
        create_icon(size, output_path)
    
    print("\n✅ All icons generated successfully!")

if __name__ == '__main__':
    main()



