from ultralytics import YOLO
from PIL import Image
import matplotlib.pyplot as plt
from paddleocr import PaddleOCR
import numpy as np
from myre import AdvancedTextCleaner
import os
import json
from improve_image import deal_image
from deal_miss_line import miss_line
from date_re import extract_time_period

class MyModel():
    def __init__(self,img_path):
        self.model_weights = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/runs/detect/train2/weights/best.pt'
        self.img_path = img_path
        self.ocr_det_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/ocr_model/ch_PP-OCRv4_det_infer'
        self.ocr_rec_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/ocr_model/ch_PP-OCRv4_rec_infer'
        self.yolo_model = YOLO(self.model_weights)
        self.ocr_model = PaddleOCR(use_angle_cls=True, 
                                   rec_model_dir=self.ocr_rec_path,
                                    det_model_dir=self.ocr_det_path,
                                    use_space_char = True,
                                    use_dilation=False,
                                    det_db_unclip_ratio=2.0)
        # self.ocr_model = PaddleOCR(use_angle_cls=True)
        self.contents = None
        self.del_re = AdvancedTextCleaner()
        self.cs = None
    
    def predict(self):
        results = self.yolo_model(self.img_path)
        image = Image.open(self.img_path)
        self.contents = {}
        self.cs  = []
        self.methods = ['Nearest-neighbor','Bilinear','Bicubic']
        for result in results:
            boxes = result.boxes
            for box in boxes:
                top_left_x, top_left_y, bottom_right_x, bottom_right_y = box.xyxy[0].tolist()
                class_name = result.names[box.cls[0].item()]
                cropped_img = image.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))
                cropped_img = np.array(cropped_img)
                # 图像增强处理
                # cropped_img = deal_image(cropped_img)
                # cropped_img = np.array(cropped_img)
                ocr_results = self.ocr_model.ocr(cropped_img,cls = False)
                self.contents[class_name] = []
                
                for one_content in ocr_results:
                    for one in one_content:
                        self.cs.append(one[1][0]) 
                single_result_content = [one[1][0] for one_content in ocr_results for one in one_content]
                single_result_content = ''.join(single_result_content)
                if class_name == '经营范围':
                    for method in self.methods:
                        cropped_img = deal_image(cropped_img,method,scale_factor=3)
                        cropped_img = np.array(cropped_img)
                        cropped_img = miss_line(cropped_img)
                        ocr_results = self.ocr_model.ocr(cropped_img,cls = False)
                        single_result_content = [one[1][0] for one_content in ocr_results for one in one_content]
                        single_result_content = ''.join(single_result_content)
                        print('\n\n\n\n')
                        print(f'特殊处理的图片结果：{single_result_content}')
                        print('\n\n\n\n')
                        if len(single_result_content) > 3:
                            break
                if len(single_result_content) <= 3:
                    for method in self.methods:
                        cropped_img = deal_image(cropped_img,method)
                        cropped_img = np.array(cropped_img)
                        ocr_results = self.ocr_model.ocr(cropped_img,cls = False)
                        single_result_content = [one[1][0] for one_content in ocr_results for one in one_content]
                        single_result_content = ''.join(single_result_content)
                        print('\n\n\n\n')
                        print(f'特殊处理的图片结果：{single_result_content}')
                        print('\n\n\n\n')
                        if len(single_result_content) > 3:
                            break
                print('单个结果')
                print(single_result_content)
                self.contents[class_name] = single_result_content
        print('ocr 结果:')
        print(f'\n\n{self.cs}\n')
        return self.contents
    
    def return_result(self):
        contents = self.predict()
        results = self.del_re.process(contents)
        print(self.cs)
        return results
                


if __name__ == '__main__':
    img_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mydata/images/val/0034.jpg'
    # results = []
    # img_dir = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mydata/images/val'
    # for img_path in os.listdir(img_dir)[:5]:
    #     img_path = os.path.join(img_dir,img_path)
    #     mymodel = MyModel(img_path)
    #     result  = mymodel.return_result()
    #     results.append(result)
    # for result in results:
    #     print(results)
    #     print('\n\n')
    mymodel = MyModel(img_path)
    result  = mymodel.predict()
