import os
import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from ultralytics import YOLO
from paddleocr import PaddleOCR
from myre import AdvancedTextCleaner

# 设置显示中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class MyModel():
    def __init__(self, img_path):
        self.model_weights = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/runs/detect/train2/weights/best.pt'
        self.img_path = img_path
        self.ocr_det_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/ocr_model/ch_PP-OCRv4_det_infer'
        self.ocr_rec_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/ocr_model/ch_PP-OCRv4_rec_infer'
        self.yolo_model = YOLO(self.model_weights)
        self.ocr_model = PaddleOCR(use_angle_cls=True, rec_model_dir=self.ocr_rec_path, det_model_dir=self.ocr_det_path)
        self.contents = None
        self.del_re = AdvancedTextCleaner()
        self.cs = None
        self.cropped_images = []
        
    def predict(self, save_crops=False):
        results = self.yolo_model(self.img_path)
        image = Image.open(self.img_path)
        self.contents = {}
        self.cs = []
        self.cropped_images = []  # 清空上一次的裁剪图像
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                top_left_x, top_left_y, bottom_right_x, bottom_right_y = box.xyxy[0].tolist()
                class_name = result.names[box.cls[0].item()]
                cropped_img = image.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))
                
                # 保存裁剪的图像信息，包括图像对象和类别名称
                self.cropped_images.append({
                    'image': cropped_img,
                    'class_name': class_name,
                    'coords': (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
                })
                
                cropped_img_array = np.array(cropped_img)
                ocr_results = self.ocr_model.ocr(cropped_img_array, cls=False)
                self.contents[class_name] = []
                
                for one_content in ocr_results:
                    for one in one_content:
                        self.cs.append(one[1][0])
                
                single_result_content = [one[1][0] for one_content in ocr_results for one in one_content]
                single_result_content = ''.join(single_result_content)
                print('单个结果')
                print(single_result_content)
                self.contents[class_name] = single_result_content
        
        print('ocr 结果:')
        print(f'\n\n{self.cs}\n')
        return self.contents
    
    def save_cropped_images(self):
        """保存所有裁剪的图像"""
        if not self.cropped_images:
            print("没有裁剪的图像可以保存")
            return
        
        # 创建保存目录
        base_filename = os.path.basename(self.img_path)
        base_name = os.path.splitext(base_filename)[0]
        save_dir = os.path.join(os.path.dirname(self.img_path), f"{base_name}_crops")
        os.makedirs(save_dir, exist_ok=True)
        
        print(f"保存裁剪图像到: {save_dir}")
        
        # 保存每个裁剪的图像
        for i, crop_info in enumerate(self.cropped_images):
            class_name = crop_info['class_name']
            crop_image = crop_info['image']
            coords = crop_info['coords']
            
            # 构建文件名，包含类别和坐标信息
            filename = f"{base_name}_{class_name}_{i}_{int(coords[0])}_{int(coords[1])}_{int(coords[2])}_{int(coords[3])}.jpg"
            save_path = os.path.join(save_dir, filename)
            
            # 保存图像
            crop_image.save(save_path)
            print(f"已保存: {save_path}")
        
    def return_result(self):
        contents = self.predict()
        results = self.del_re.process(contents)
        print(self.cs)
        return results

def process_images():
    dir_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mytest/data'
    
    # 读取目录中的所有jpg文件
    try:
        img_files = [f for f in os.listdir(dir_path) if f.lower().endswith('.jpg')]
        print(f"找到 {len(img_files)} 个JPG文件")
        
        for filename in img_files:
            # 构建绝对路径
            full_path = os.path.abspath(os.path.join(dir_path, filename))
            print(f"处理文件: {full_path}")
            
            # 使用MyModel处理图像
            model = MyModel(full_path)
            result = model.return_result()
            print('\n\n\n\n')
            print(result)
            
            # 等待用户输入
            while True:
                user_input = input("输入1继续处理下一张图片，输入2保存裁剪图像后继续: ")
                if user_input == '1':
                    plt.close()  # 关闭当前图像
                    break
                elif user_input == '2':
                    model.save_cropped_images()  # 保存裁剪的图像
                    plt.close()  # 关闭当前图像
                    break
                else:
                    print("输入无效，请输入1或2")
            
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == '__main__':
    process_images()

