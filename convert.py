import struct
import numpy as np
from PIL import Image

# 文件路径
file_path = '2500-5000-10nm-4.dat'

# 读取文件头
def read_file_header(file):
    file_header = file.read(2060)
    return file_header

# 读取帧头
def read_frame_header(file):
    frame_header = file.read(64)
    fifo_status, frame_number, ten_us_counter = struct.unpack('3I', frame_header[:12])
    return frame_header, fifo_status, frame_number, ten_us_counter

# 读取图像数据
def read_image_data(file, image_size):
    image_data = file.read(image_size)
    return image_data

# 保存图像
def save_image(image_data, rows, cols, filename):
    image_array = np.frombuffer(image_data, dtype=np.uint16).reshape((rows, cols))
    image = Image.fromarray(image_array)
    image.save(filename)

# 解析DAT文件
def parse_dat_file(file_path):
    with open(file_path, 'rb') as file:
        # 读取文件头
        file_header = read_file_header(file)

        # 提取文件头中的图像参数
        data_format = struct.unpack('H', file_header[4:6])[0]
        rows = struct.unpack('H', file_header[6:8])[0]
        cols = struct.unpack('H', file_header[8:10])[0]

        # 计算每个图像的大小
        pixel_size = 2
        image_size = rows * cols * pixel_size

        # 读取并保存每个图像
        frame_index = 0
        while True:
            frame_header, fifo_status, frame_number, ten_us_counter = read_frame_header(file)
            if not frame_header:
                break
            image_data = read_image_data(file, image_size)
            if not image_data:
                break
            save_image(image_data, rows, cols, f'image_{frame_index}.png')
            frame_index += 1

# 调用解析函数
parse_dat_file(file_path)
