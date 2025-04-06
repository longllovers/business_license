from paddleocr import PaddleOCR
import cv2
import numpy as np
ocr_det_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/ocr_model/ch_PP-OCRv4_det_infer'
ocr_rec_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/ocr_model/ch_PP-OCRv4_rec_infer'





img_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mytest/data/0539_crops/0539_经营范围_1_93_425_576_539.jpg'
img_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mytest/data/0002_crops/0002_经营范围_0_90_302_430_407.jpg'
img_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mytest/data/0819_crops/0819_地址_8_1114_853_1808_933.jpg'
img_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mytest/data/0002_crops/0002_注册资本_1_436_217_598_240.jpg'
img_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mytest/data/0006.jpg'
img_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mytest/data/0334_crops/0334_法定代表人_7_216_700_435_739.jpg'
img_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mytest/data/0811_crops/0811_经营范围_0_475_1996_2630_2732.jpg'
img_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mytest/data/0826_crops/0826_经营范围_2_155_1194_1439_1417.jpg'
img_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mytest/data/0817_crops/0817_经营范围_0_268_633_821_783.jpg'
img_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/mytest/data/0025_crops/0025_成立日期_3_1216_751_1682_808.jpg'

ocr_model = PaddleOCR(use_angle_cls=True, rec_model_dir=ocr_rec_path, det_model_dir=ocr_det_path,
                      use_space_char = True,use_dilation=False,det_db_unclip_ratio=1.8)
img = cv2.imread(img_path)
border_size = 20  # 增加 20 像素的白色边缘
img_with_border = cv2.copyMakeBorder(img, border_size, border_size, border_size, border_size, 
                                     cv2.BORDER_CONSTANT, value=(255,255,255))
cv2.imwrite("temp_with_border.jpg", img_with_border)  # 保存新的图片
result = ocr_model.ocr("temp_with_border.jpg", cls=True)


cs = []
for one_content in result:
    for one in one_content:
        cs.append(one[1][0])
print(''.join(cs))
        





