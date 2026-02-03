#!/usr/bin/env python3
"""
Generate round icons with label for JD Extractor extension
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_round_icon(size, text="JD", bg_color="#1565c0", text_color="#ffffff"):
    """Create a round icon with text label"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Convert hex color to RGB
    bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
    text_rgb = tuple(int(text_color[i:i+2], 16) for i in (1, 3, 5))
    
    # Draw circle with gradient effect (darker blue)
    margin = int(size * 0.05)  # 5% margin for better visibility
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=bg_rgb,
        outline=(255, 255, 255, 200),  # White outline for contrast
        width=max(1, int(size * 0.03))
    )
    
    # Try to load a bold font for better visibility
    font_size = int(size * 0.55)  # Larger text
    font = None
    
    # Try different font paths (prioritize bold fonts)
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                # Try to load as bold
                font = ImageFont.truetype(font_path, font_size)
                break
        except:
            continue
    
    if font is None:
        # Use default font
        try:
            font = ImageFont.load_default()
        except:
            pass
    
    # Calculate text position (centered)
    if font:
        try:
            # Get text bounding box
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Center the text
            position = ((size - text_width) / 2, (size - text_height) / 2 - bbox[1])
            
            # Draw text with slight shadow for better visibility
            shadow_offset = max(1, int(size * 0.02))
            draw.text(
                (position[0] + shadow_offset, position[1] + shadow_offset),
                text,
                fill=(0, 0, 0, 100),  # Semi-transparent black shadow
                font=font
            )
            draw.text(position, text, fill=text_rgb, font=font)
        except Exception as e:
            # Fallback: simple centered text
            text_x = (size - len(text) * font_size * 0.6) / 2
            text_y = (size - font_size) / 2
            draw.text((text_x, text_y), text, fill=text_rgb, font=font)
    else:
        # No font available, draw simple centered text
        text_x = (size - len(text) * size * 0.3) / 2
        text_y = size // 3
        draw.text((text_x, text_y), text, fill=text_rgb)
    
    return img

def main():
    """Generate all icon sizes"""
    icon_dir = 'icons'
    os.makedirs(icon_dir, exist_ok=True)
    
    sizes = {
        16: 'icon16.png',
        48: 'icon48.png',
        128: 'icon128.png'
    }
    
    for size, filename in sizes.items():
        icon = create_round_icon(size)
        icon_path = os.path.join(icon_dir, filename)
        icon.save(icon_path, 'PNG')
        print(f"✅ Created {icon_path} ({size}x{size})")
    
    print("\n🎉 All icons generated successfully!")

if __name__ == '__main__':
    main()

