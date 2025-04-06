from paddleocr import PaddleOCR, draw_ocr
from PIL import Image, ImageOps
import re

ocr_det_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/ocr_model/ch_PP-OCRv4_det_infer'
ocr_rec_path = '/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/ocr_model/ch_PP-OCRv4_rec_infer'
cr_model = PaddleOCR(use_angle_cls=True, rec_model_dir=ocr_rec_path, det_model_dir=ocr_det_path)

ocr = cr_model
img_path="/home/ialover/document/yingyezhizhao/ultralytics/ultralytics/微信图片_20250313001419_经营范围_0_170_575_831_890.jpg"
image = Image.open(img_path).convert('RGB')
image = ImageOps.exif_transpose(image)
image.save(img_path) #由于图片有时识别出来是翻转的，需要进行额外存储处理
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)

# 显示结果
from PIL import Image, ImageOps
result = result[0]
image = Image.open(img_path)
image = ImageOps.exif_transpose(image)
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.show()