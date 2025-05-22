import cv2
import numpy as np

def pixel_art_generator(image_path, pixel_size=16, k_colors=8, output_path='pixel_art.png'):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image not found, please check the path.")

    original_shape = img.shape[:2]

    # Resize to small resolution (pixelate)
    small_img = cv2.resize(img, (pixel_size, pixel_size), interpolation=cv2.INTER_LINEAR)

    # Reshape to (num_pixels, 3)
    data = small_img.reshape((-1, 3))
    data = np.float32(data)

    # Define kmeans criteria and apply
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(data, k_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Map each pixel to nearest color center
    centers = np.uint8(centers)
    quantized_data = centers[labels.flatten()]
    quantized_img = quantized_data.reshape(small_img.shape)

    # Resize back to original size with nearest interpolation for pixel look
    pixel_art = cv2.resize(quantized_img, (original_shape[1], original_shape[0]), interpolation=cv2.INTER_NEAREST)

    # Save the result
    cv2.imwrite(output_path, pixel_art)

    return output_path