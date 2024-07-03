import struct
import numpy as np
from PIL import Image
import csv
from pathlib import Path

def read_dat_file(file_path):
    with open(file_path, 'rb') as f:
        # Read the file header
        header = f.read(2060)

        # Extract image dimensions from the header
        sw_version = struct.unpack('4s', header[0:4])[0]
        data_format = struct.unpack('H', header[4:6])[0]
        image_rows = struct.unpack('H', header[6:8])[0]
        image_cols = struct.unpack('H', header[8:10])[0]

        # Calculate the number of pixels
        num_pixels = image_rows * image_cols

        # Initialize an empty list to store images
        images = []

        while True:
            # Read the image header
            image_header = f.read(12)
            if len(image_header) < 12:
                break

            fifo_status = struct.unpack('I', image_header[0:4])[0]
            frame_number = struct.unpack('I', image_header[4:8])[0]
            ten_us_counter = struct.unpack('I', image_header[8:12])[0]

            # Read the raw image data
            raw_image_data = f.read(num_pixels * 2)
            if len(raw_image_data) < num_pixels * 2:
                break

            # Convert the raw image data to a numpy array
            image_data = np.frombuffer(raw_image_data, dtype=np.uint16).reshape((image_rows, image_cols))
            images.append(image_data)

    return images, sw_version, data_format, image_rows, image_cols

def save_images(images, image_rows, image_cols):
    for i, image_data in enumerate(images):
        image = Image.fromarray(image_data)
        # image = image.convert("L")  # Convert to grayscale
        image.save(f'{output_folder}/image_{i}.png')


def save_images_to_csv(images, image_rows, image_cols, output_folder):
    """
    Save list of images to CSV files.

    :param images: List of numpy arrays representing images
    :param image_rows: Number of rows in each image
    :param image_cols: Number of columns in each image
    :param output_folder: Folder path where CSV files will be saved
    """
    Path(output_folder).mkdir(parents=True, exist_ok=True)  # Ensure output folder exists

    for i, image_data in enumerate(images):
        # Define the CSV filename
        csv_filename = f'{output_folder}/image_{i}.csv'

        # Open a CSV file for writing
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write each pixel value row by row
            for row in image_data:
                writer.writerow(row)

# After calling read_dat_file and getting images, you can use this function like so:
# save_images_to_csv(images, image_rows, image_cols, 'path/to/csv/output/folder')

def save_all_images_to_single_csv(images, image_rows, image_cols, output_file):
    """
    Save all images into a single CSV file.

    :param images: List of numpy arrays representing images
    :param image_rows: Number of rows in each image
    :param image_cols: Number of columns in each image
    :param output_file: Filename for the combined CSV output
    """
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Iterate over each image
        for i, image_data in enumerate(images):
            # Prefix each image with a unique identifier or index (optional)
            writer.writerow([f"Image_{i}"])

            # Flatten the 2D image array into a single list of pixel values for each row
            flat_image = image_data.astype(np.int16).flatten().tolist()
            writer.writerow(flat_image)  # Write pixel values

            # Optionally, add an empty row to separate images in the CSV (optional)
            writer.writerow([])

# Usage example:
# save_all_images_to_single_csv(images, image_rows, image_cols, 'all_images.csv')

# Example usage
file_path = '2500-5000-10nm-4.dat'  # 替换为你的DAT文件路径
output_folder = 'D:\python小工具'  # 替换为实际的输出文件夹路径
images, sw_version, data_format, image_rows, image_cols = read_dat_file(file_path)
print(f"Found {len(images)} images in the file.")
save_all_images_to_single_csv(images, image_rows, image_cols, 'all_images.csv')
# save_images_to_csv(images, image_rows, image_cols, f'{output_folder}/csv')
# save_images(images, image_rows, image_cols)
