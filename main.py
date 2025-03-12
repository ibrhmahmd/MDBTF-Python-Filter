from PIL import Image, ImageOps, ImageDraw
import numpy as np
import os

def create_rounded_rectangle_mask(size, radius):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (size[0]-1, size[1]-1)], radius, fill=255)
    return mask

def pixelate_image(input_path, output_path, pixel_size=(20, 20), upscale_factor=50):
    # Load the image
    image = Image.open(input_path)
    
    # Convert to RGB mode (if not already)
    image = image.convert("RGB")
    
    # Resize the image to pixel_size using NEAREST interpolation
    pixelated = image.resize(pixel_size, Image.NEAREST)
    
    # Scale up to an intermediate size
    new_size = (pixel_size[0] * upscale_factor, pixel_size[1] * upscale_factor)
    pixelated_large = pixelated.resize(new_size, Image.NEAREST)
    
    # Calculate background size for 40% ratio
    # If pixelated image should be 40% of total, then total should be pixelated/0.4
    bg_multiplier = 1 / 0.4  # This gives us approximately 2.5x size
    background_size = (int(new_size[0] * bg_multiplier), int(new_size[1] * bg_multiplier))
    
    # Create the background with rounded corners
    red_background = Image.new("RGBA", background_size, (0, 0, 0, 0))  # Transparent background
    mask = create_rounded_rectangle_mask(background_size, 0)
    background_draw = ImageDraw.Draw(red_background)
    Red_Color = "#ED2542"
    background_draw.rounded_rectangle([(0, 0), (background_size[0]-1, background_size[1]-1)], 40, fill=Red_Color)
    
    # Add golden border to the pixelated image
    border_size = 10  # Border thickness in pixels
    golden_color = ("#D6963E")  # HEX for golden color
    bordered_image = Image.new("RGB", (pixelated_large.width + 2*border_size, pixelated_large.height + 2*border_size), golden_color)
    bordered_image.paste(pixelated_large, (border_size, border_size))
    
    # Paste the bordered pixelated image onto the center of the red background
    x_offset = (red_background.width - bordered_image.width) // 2
    y_offset = (red_background.height - bordered_image.height) // 2
    red_background.paste(bordered_image, (x_offset, y_offset), mask=None)
    
    # Load and resize the Parental Advisory logo
    advisory_logo = Image.open("1528062162hd-parental-advisory.png")
    # Convert to RGBA if not already
    advisory_logo = advisory_logo.convert("RGBA")
    # Calculate logo size (13% of the background width)
    logo_width = int(background_size[0] * 0.13)
    logo_height = int(logo_width * advisory_logo.height / advisory_logo.width)
    advisory_logo = advisory_logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
    
    # Calculate position for bottom right
    right_padding = int(background_size[0] * 0.02)
    bottom_padding = int(background_size[1] * 0.01)
    logo_x = background_size[0] - logo_width - right_padding
    logo_y = background_size[1] - logo_height - bottom_padding
    
    # Create the final image with white background
    final_image = Image.new("RGB", background_size, (255, 255, 255))
    final_image.paste(red_background, (0, 0), mask=red_background.split()[3])
    
    # Paste the advisory logo
    final_image.paste(advisory_logo, (logo_x, logo_y), mask=advisory_logo.split()[3])
    
    final_image.save(output_path)
    print(f"Pixelated image saved as {output_path}")

# Example usage
input_image = "tam-al-ta3be2a.jpg"  # Replace with your image path

# Get the base name without extension and create output filename
base_name = os.path.splitext(input_image)[0]  # Get filename without extension
output_image = f"{base_name}-output.png"
pixelate_image(input_image, output_image)