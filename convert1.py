import struct
import numpy as np
from PIL import Image

def parse_dat_file(dat_file_path, output_folder):
    with open(dat_file_path, 'rb') as f:
        # 读取文件头
        file_header = f.read(2060)

        '''
        \x00 表示两个十六进制数，即二进制的0000 0000，对应的十进制数为0。一个十六进制数为4bit。
        '''

        # 从文件头中提取图像的元数据
        sw_version = struct.unpack('I', file_header[0:4])[0]
        data_format = struct.unpack('H', file_header[4:6])[0]
        image_rows = struct.unpack('H', file_header[6:8])[0]
        image_columns = struct.unpack('H', file_header[8:10])[0]

        # 计算每个像素的字节数
        bytes_per_pixel = data_format

        image_count = 0

        while True:
            # 尝试读取一个帧头
            frame_header = f.read(64) # 64
            if len(frame_header) < 64: # 64
                break

            # 读取图像数据
            raw_image_data = f.read(image_rows * image_columns * bytes_per_pixel)
            if len(raw_image_data) < image_rows * image_columns * bytes_per_pixel:
                break

            # 将原始图像数据转换为NumPy数组
            image_data = np.frombuffer(raw_image_data, dtype=np.uint16).reshape((image_rows, image_columns))

            # 创建并保存图像
            img = Image.fromarray(image_data)
            img.save(f"{output_folder}/image_{image_count}.png")
            image_count += 1

# 使用示例
dat_file_path = '2500-5000-10nm-4.dat'  # 替换为实际的DAT文件路径
output_folder = 'D:\python小工具\data3'  # 替换为实际的输出文件夹路径
parse_dat_file(dat_file_path, output_folder)
