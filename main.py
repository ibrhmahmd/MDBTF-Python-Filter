from PIL import Image, ImageOps, ImageDraw
import numpy as np

def create_rounded_rectangle_mask(size, radius):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (size[0]-1, size[1]-1)], radius, fill=255)
    return mask

def pixelate_image(input_path, output_path, pixel_size=(11, 10), upscale_factor=50):
    # Load the image
    image = Image.open(input_path)
    
    # Convert to RGB mode (if not already)
    image = image.convert("RGB")
    
    # Resize the image to pixel_size (10x11) using NEAREST interpolation
    pixelated = image.resize(pixel_size, Image.NEAREST)
    
    # Scale up to an intermediate size
    new_size = (pixel_size[0] * upscale_factor, pixel_size[1] * upscale_factor)
    pixelated_large = pixelated.resize(new_size, Image.NEAREST)
    
    # Create a larger red background (4x the size of pixelated image)
    background_size = (new_size[0] * 3, new_size[1] * 3)
    
    # Create the background with rounded corners
    red_background = Image.new("RGBA", background_size, (0, 0, 0, 0))  # Transparent background
    mask = create_rounded_rectangle_mask(background_size, 25)
    background_draw = ImageDraw.Draw(red_background)
    background_draw.rounded_rectangle([(0, 0), (background_size[0]-1, background_size[1]-1)], 25, fill="#ED2542")
    
    # Add golden border to the pixelated image
    border_size = 10  # Border thickness in pixels
    golden_color = (218, 165, 32)  # RGB for golden color
    bordered_image = Image.new("RGB", (pixelated_large.width + 2*border_size, pixelated_large.height + 2*border_size), golden_color)
    bordered_image.paste(pixelated_large, (border_size, border_size))
    
    # Paste the bordered pixelated image onto the center of the red background
    x_offset = (red_background.width - bordered_image.width) // 2
    y_offset = (red_background.height - bordered_image.height) // 2
    red_background.paste(bordered_image, (x_offset, y_offset), mask=None)
    
    # Save the final image with white background
    final_image = Image.new("RGB", background_size, (255, 255, 255))
    final_image.paste(red_background, (0, 0), mask=red_background.split()[3])
    final_image.save(output_path)
    
    print(f"Pixelated image saved as {output_path}")

# Example usage
input_image = "E:/Users/Ibrahim/Desktop/MDBTF-Python-Filter/tam-al-ta3be2a.jpg"  # Replace with your image path
output_image = "output.jpg"
pixelate_image(input_image, output_image)
