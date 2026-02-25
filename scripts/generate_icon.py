#!/usr/bin/env python3
"""
Generate Calcora application icon (calcora.ico)

Creates a professional calculator-themed icon with mathematical symbols.
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Generate a professional icon for Calcora."""
    # Create multiple sizes for .ico format (Windows standard)
    sizes = [256, 128, 64, 48, 32, 16]
    images = []
    
    for size in sizes:
        # Create image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Color scheme: Modern blue gradient
        primary_color = (37, 99, 235)    # Blue-600
        secondary_color = (59, 130, 246)  # Blue-500
        text_color = (255, 255, 255)      # White
        
        # Draw rounded rectangle background
        margin = size // 8
        corner_radius = size // 6
        
        # Draw background with rounded corners (simulate with circle + rectangles)
        draw.rounded_rectangle(
            [margin, margin, size - margin, size - margin],
            radius=corner_radius,
            fill=primary_color
        )
        
        # Draw mathematical symbol (integral sign ∫ or calculator symbol)
        # For larger icons, draw a stylized "∫" symbol
        if size >= 32:
            # Draw stylized ∫ symbol
            font_size = int(size * 0.6)
            try:
                # Try to use a nice font
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Fallback to default
                font = ImageFont.load_default()
            
            # Draw ∫ symbol (or 'f(x)' for calculator aesthetic)
            text = "∫"
            
            # Get text bounding box for centering
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Center the text
            x = (size - text_width) // 2 - bbox[0]
            y = (size - text_height) // 2 - bbox[1]
            
            # Draw text with slight shadow for depth
            shadow_offset = max(1, size // 64)
            draw.text((x + shadow_offset, y + shadow_offset), text, 
                     fill=(0, 0, 0, 128), font=font)
            draw.text((x, y), text, fill=text_color, font=font)
        else:
            # For small icons, draw simple dot grid pattern
            grid_margin = size // 3
            dot_size = max(1, size // 10)
            
            for i in range(2):
                for j in range(2):
                    if size >= 16:
                        x = grid_margin + j * (size - 2 * grid_margin)
                        y = grid_margin + i * (size - 2 * grid_margin)
                        draw.ellipse([x, y, x + dot_size, y + dot_size], fill=text_color)
        
        images.append(img)
    
    # Save as .ico file
    output_path = os.path.join('media', 'calcora-icon.ico')
    os.makedirs('media', exist_ok=True)
    
    # Save with multiple resolutions
    images[0].save(
        output_path,
        format='ICO',
        sizes=[(s, s) for s in sizes]
    )
    
    print(f"✓ Created icon: {output_path}")
    print(f"  Sizes: {', '.join(f'{s}x{s}' for s in sizes)}")
    
    # Also save a PNG version for documentation
    images[0].save(output_path.replace('.ico', '.png'), format='PNG')
    print(f"✓ Created PNG: {output_path.replace('.ico', '.png')}")

if __name__ == '__main__':
    create_icon()
