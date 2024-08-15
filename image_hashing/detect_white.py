from PIL import Image
import numpy as np
from collections import Counter
import colorsys

def is_almost_white_page(image_path, intensity_threshold=250, non_white_pixel_threshold=0.01):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    pixels = np.array(img)
    avg_intensity = np.mean(pixels)
    non_white_pixels = np.sum(pixels < intensity_threshold)  # Pixels that are not white
    non_white_ratio = non_white_pixels / pixels.size

    return avg_intensity > intensity_threshold and non_white_ratio < non_white_pixel_threshold

def is_almost_single_color(image_path, color_tolerance=10, color_ratio_threshold=0.95):
    """
    Detect if an image is almost a single color.
    
    :param image_path: Path to the image file
    :param color_tolerance: Maximum allowed difference between colors to be considered the same (0-255)
    :param color_ratio_threshold: Minimum ratio of pixels that must be similar to the dominant color
    :return: True if the image is almost a single color, False otherwise
    """
    img = Image.open(image_path).convert('RGB')  # Convert to RGB
    pixels = np.array(img)
    
    # Flatten the image array to a list of RGB tuples
    pixels_list = pixels.reshape(-1, 3)
    
    # Convert RGB to HSV to work with hue, saturation, and value
    pixels_hsv = np.array([colorsys.rgb_to_hsv(*pixel) for pixel in pixels_list / 255.0])
    
    # Determine the most common hue
    hue_values = pixels_hsv[:, 0]  # Extract hue values
    hue_counts = Counter(hue_values)
    dominant_hue = hue_counts.most_common(1)[0][0]
    
    # Find pixels within the color tolerance
    hue_tolerance = color_tolerance / 360.0  # Convert tolerance to hue range
    similar_pixels = np.sum(np.abs(hue_values - dominant_hue) < hue_tolerance)
    
    # Calculate the ratio of similar pixels to total pixels
    similar_pixel_ratio = similar_pixels / len(pixels_list)
    
    return similar_pixel_ratio >= color_ratio_threshold
