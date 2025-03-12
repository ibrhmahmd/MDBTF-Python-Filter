from PIL import Image, ImageOps
import numpy as np

def pixelate_image(input_path, output_path, pixel_size=(10, 11), upscale_factor=50):
    # Load the image
    image = Image.open(input_path)
    
    # Convert to RGB mode (if not already)
    image = image.convert("RGB")
    
    # Resize the image to pixel_size (10x11) using NEAREST interpolation
    pixelated = image.resize(pixel_size, Image.NEAREST)
    
    # Scale back up to a larger size
    new_size = (pixel_size[0] * upscale_factor, pixel_size[1] * upscale_factor)
    pixelated_large = pixelated.resize(new_size, Image.NEAREST)
    
    # Create a solid red background (similar to the album cover)
    red_background = Image.new("RGB", (new_size[0] + 100, new_size[1] + 100), (220, 0, 0))
    
    # Paste the pixelated image onto the center of the red background
    x_offset = (red_background.width - pixelated_large.width) // 2
    y_offset = (red_background.height - pixelated_large.height) // 2
    red_background.paste(pixelated_large, (x_offset, y_offset))
    
    # Save the final image
    red_background.save(output_path)
    
    print(f"Pixelated image saved as {output_path}")

# Example usage
input_image = "input.jpg"  # Replace with your image path
output_image = "output.jpg"
pixelate_image(input_image, output_image)
