# MDBTF Python Image Filter

This script applies a pixelated filter to an image, mimicking the aesthetic of My Beautiful Dark Twisted Fantasy's album cover.


## Requirements

- Python 3.6 or higher
- Pillow 10.2.0
- NumPy 1.26.4

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MDBTF-Python-Filter.git
cd MDBTF-Python-Filter
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from main import pixelate_image

# Basic usage with default settings
pixelate_image("input.jpg")

# Custom settings
pixelate_image(
    input_path="input.jpg",
    output_path="custom_output.png",
    pixel_size=(30, 30),
    upscale_factor=60
)
```

### Customization Options

- `pixel_size`: Tuple of (width, height) for pixelation resolution (default: (20, 20))
- `upscale_factor`: Factor to scale up the pixelated image (default: 50)
- `output_path`: Custom output path (optional, defaults to input_name-output.png)

## Features Details

### Image Processing
- Pixelation using nearest-neighbor interpolation
- High-quality upscaling
- Transparent background support
- Aspect ratio preservation

### Styling
- Rounded corners (40px radius)
- Golden border (10px width)
- Red background (#ED2542)
- Parental Advisory logo (13% of image width)
- White base background
