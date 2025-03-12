from PIL import Image, ImageOps, ImageDraw
import numpy as np
import os

def create_rounded_rectangle_mask(size, radius):
    """Create a mask for rounded rectangle corners."""
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (size[0]-1, size[1]-1)], radius, fill=255)
    return mask

def create_pixelated_image(image, pixel_size, upscale_factor):
    """Create a pixelated version of the input image."""
    # Resize to small pixel size
    pixelated = image.resize(pixel_size, Image.NEAREST)
    # Scale up to final size
    new_size = (pixel_size[0] * upscale_factor, pixel_size[1] * upscale_factor)
    return pixelated.resize(new_size, Image.NEAREST)

def create_background(size, corner_radius, color):
    """Create a rounded rectangle background."""
    background = Image.new("RGBA", size, (0, 0, 0, 0))
    background_draw = ImageDraw.Draw(background)
    background_draw.rounded_rectangle([(0, 0), (size[0]-1, size[1]-1)], corner_radius, fill=color)
    return background

def add_border(image, border_size, border_color):
    """Add a border around an image."""
    bordered = Image.new("RGB", 
                        (image.width + 2*border_size, image.height + 2*border_size), 
                        border_color)
    bordered.paste(image, (border_size, border_size))
    return bordered

def prepare_advisory_logo(logo_path, target_width):
    """Load and resize the advisory logo."""
    advisory_logo = Image.open(logo_path)
    advisory_logo = advisory_logo.convert("RGBA")
    # Calculate height maintaining aspect ratio
    aspect_ratio = advisory_logo.height / advisory_logo.width
    target_height = int(target_width * aspect_ratio)
    return advisory_logo.resize((target_width, target_height), Image.Resampling.LANCZOS)

def calculate_background_size(image_size, target_ratio=0.4):
    """Calculate background size to make image occupy target_ratio of total area."""
    multiplier = 1 / target_ratio
    return (int(image_size[0] * multiplier), int(image_size[1] * multiplier))

def generate_output_filename(input_path):
    """Generate output filename from input path."""
    base_name = os.path.splitext(input_path)[0]
    return f"{base_name}-output.png"

def pixelate_image(input_path, output_path=None, pixel_size=(20, 20), upscale_factor=50):
    """Main function to create pixelated image with styling."""
    # Load and convert image
    image = Image.open(input_path).convert("RGB")
    
    # Create pixelated version
    pixelated_large = create_pixelated_image(image, pixel_size, upscale_factor)
    
    # Calculate sizes
    background_size = calculate_background_size(pixelated_large.size)
    
    # Create red background
    red_background = create_background(background_size, 40, "#ED2542")
    
    # Add golden border to pixelated image
    bordered_image = add_border(pixelated_large, 10, "#D6963E")
    
    # Center the bordered image
    x_offset = (red_background.width - bordered_image.width) // 2
    y_offset = (red_background.height - bordered_image.height) // 2
    red_background.paste(bordered_image, (x_offset, y_offset), mask=None)
    
    # Prepare and position advisory logo
    logo_width = int(background_size[0] * 0.13)
    advisory_logo = prepare_advisory_logo("1528062162hd-parental-advisory.png", logo_width)
    
    # Calculate logo position
    right_padding = int(background_size[0] * 0.02)
    bottom_padding = int(background_size[1] * 0.01)
    logo_x = background_size[0] - advisory_logo.width - right_padding
    logo_y = background_size[1] - advisory_logo.height - bottom_padding
    
    # Create final composition
    final_image = Image.new("RGB", background_size, (255, 255, 255))
    final_image.paste(red_background, (0, 0), mask=red_background.split()[3])
    final_image.paste(advisory_logo, (logo_x, logo_y), mask=advisory_logo.split()[3])
    
    # Save the result
    if output_path is None:
        output_path = generate_output_filename(input_path)
    final_image.save(output_path)
    print(f"Pixelated image saved as {output_path}")
    return output_path

# Example usage
if __name__ == "__main__":
    input_image = "tam-al-ta3be2a.jpg"
    pixelate_image(input_image)