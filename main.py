import os
from PIL import Image
import cv2
import fitz  # PyMuPDF
import layoutparser as lp

pdf = fitz.open('IA3.pdf')
for page_num in range(len(pdf)):
    page = pdf[page_num]
    pm = page.get_pixmap()
    img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
    img.save(f'page_{page_num}.png')
image = cv2.imread('page_13.png')
image = image[..., ::-1]



model = lp.Detectron2LayoutModel(
            config_path ='./config.yml', # In model catalog
            label_map  ={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"}, # In model`label_map`
            extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8] # Optional
        )


# 检测
layout = model.detect(image)

# 显示结果
show_img = lp.draw_box(image, layout, box_width=3, show_element_type=True)

print(type(layout))

