# import cv2
# import numpy as np


# def resize_image(image, scale_factor, interpolation_method):
#     # 读取原始图像
#     if isinstance(image, str):
#         image = cv2.imread(image)
#         if image is None:
#             print(f"Error: Unable to read image file {image}")
#             return

#     # 获取原始图像的尺寸
#     original_height, original_width = image.shape[:2]

#     # 计算放大后的尺寸
#     new_width = int(original_width * scale_factor)
#     new_height = int(original_height * scale_factor)

#     # 根据指定的插值方法进行图像缩放
#     resized_image = cv2.resize(image, (new_width, new_height), interpolation=interpolation_method)

#     return resized_image


# def deal_image(cropped_img):
#     # 定义图像路径和放大倍数
#     scale_factor = 20  # 放大2倍

#     # 定义插值方法
#     methods = {
#         'Nearest-neighbor': cv2.INTER_NEAREST,
#         'Bilinear': cv2.INTER_LINEAR,
#         'Bicubic': cv2.INTER_CUBIC
#     }
#     print(f"处理和增强图像中！")

#     # 读取并放大图像
#     count=1
#     for method_name, method_value in methods.items():
#         method_name=count
#         count+=1
#         resized_image = resize_image(cropped_img, scale_factor, method_value)
    
#     print(f"处理图片完毕！")
#     return resize_image


from PIL import Image
import numpy as np

def resize_image(image, scale_factor, interpolation_method):
    # 如果传入的是路径而不是数组，则读取图像
    if isinstance(image, str):
        image = Image.open(image)
    elif isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    # 获取原始图像的尺寸
    original_width, original_height = image.size

    # 计算放大后的尺寸
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)

    # 根据指定的插值方法进行图像缩放
    resized_image = image.resize((new_width, new_height), interpolation_method)

    return resized_image


def deal_image(cropped_img,method_name,scale_factor=10):

    # 定义插值方法（PIL中的方法）
    methods = {
        'Nearest-neighbor': Image.NEAREST,
        'Bilinear': Image.BILINEAR,
        'Bicubic': Image.BICUBIC
    }
    print("处理和增强图像中！")
    method_value = methods[method_name]
    # 读取并放大图像
    resized_image = resize_image(cropped_img, scale_factor, method_value)
    print(f"方法 {method_name} 处理完成")


    print("处理图片完毕！")
    return resized_image
