"""
Script to create test images for digit recognition testing
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont


def create_digit_image(digit, size=(28, 28)):
    """Create a test image with a specific digit"""
    img = Image.new("L", size, color=0)  # Black background
    draw = ImageDraw.Draw(img)

    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None

    # Calculate position to center the digit
    text = str(digit)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2

    # Draw the digit in white
    draw.text((x, y), text, fill=255, font=font)

    return img


def create_noisy_image(base_img):
    """Add noise to an image"""
    pixels = list(base_img.getdata())
    noisy_pixels = []

    for pixel in pixels:
        # Add random noise
        noise = random.randint(-30, 30)
        new_pixel = max(0, min(255, pixel + noise))
        noisy_pixels.append(new_pixel)

    noisy_img = Image.new("L", base_img.size)
    noisy_img.putdata(noisy_pixels)
    return noisy_img


def create_test_images():
    """Create test images for digits 0-9"""
    test_dir = os.path.join(os.path.dirname(__file__), "pictures")
    os.makedirs(test_dir, exist_ok=True)

    for digit in range(10):
        img = create_digit_image(digit)
        filename = f"digit_{digit}.png"
        filepath = os.path.join(test_dir, filename)
        img.save(filepath)
        print(f"Created {filepath}")

    # Create some additional test images
    # Create a noisy digit
    img = create_digit_image(5)
    noisy_img = create_noisy_image(img)
    noisy_img.save(os.path.join(test_dir, "digit_5_noisy.png"))
    print(f"Created {os.path.join(test_dir, 'digit_5_noisy.png')}")

    # Create a rotated digit
    img = create_digit_image(3)
    rotated_img = img.rotate(15, fillcolor=0)
    rotated_img.save(os.path.join(test_dir, "digit_3_rotated.png"))
    print(f"Created {os.path.join(test_dir, 'digit_3_rotated.png')}")


if __name__ == "__main__":
    create_test_images()
