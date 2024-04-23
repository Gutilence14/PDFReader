import os
from PIL import Image
import cv2
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import layoutparser as lp
from dataclasses import dataclass
from transformers.utils import ModelOutput
from typing import Optional, Tuple



@dataclass
class BasePdfOutput(ModelOutput):
    """
    base pdf output
    """
    Page: int = None
    Title: str = None
    Text: str = None
    Table: str = None
    Figure: str = None

@dataclass
class PdfOutput(ModelOutput):
    Pdf: Optional[Tuple[BasePdfOutput, ...]] = None



def load_img(pdf_path):
    pdf_img = convert_from_path(pdf_path, thread_count=10, fmt='png', dpi=300)
    return pdf_img

def detect_img(img):
    model = lp.Detectron2LayoutModel(
            config_path ='./config.yml', # In model catalog
            label_map  ={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"}, # In model`label_map`
            extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8] # Optional
        )
    layout = model.detect(img)
    return layout

pdf_path = "IA3.pdf"
img = load_img(pdf_path=pdf_path)
ocr_agent = lp.TesseractAgent(languages='chi_sim+eng+spa')

for index, i in enumerate(img):
    i
    # print('image shape:{}'.format(i.shape))
    # layout = detect_img(i)
    # text_blocks = lp.Layout([b for b in layout if b.type=='Text'])
    # text_res = ""
    # for block in text_blocks:
    #     segment_image = (block
    #                         .pad(left=5, right=5, top=5, bottom=5)
    #                         .crop_image(i))        
    #     text = ocr_agent.detect(segment_image)
    #     text_res += text

    # figure_blocks = lp.Layout([b for b in layout if b.type=='Figure'])
    # table_blocks = lp.Layout([b for b in layout if b.type=='Table'])

    # title_blocks = lp.Layout([b for b in layout if b.type=='Title'])
    # title_res = ""
    # for block in title_blocks:
    #     segment_image = (block
    #                         .pad(left=5, right=5, top=5, bottom=5)
    #                         .crop_image(i))        
    #     title = ocr_agent.detect(segment_image)
    #     title_res += title

    # output = BasePdfOutput(
    #     Page=index,
    #     Text=text_res,
    #     Title=title_res,
    # )


    # print(output)
    # break
    



# pdf = fitz.open('IA3.pdf')
# for page_num in range(len(pdf)):
#     page = pdf[page_num]
#     pm = page.get_pixmap()
#     img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
#     img.save(f'page_{page_num}.png')
# image = cv2.imread('page_13.png')
# image = image[..., ::-1]



# model = lp.Detectron2LayoutModel(
#             config_path ='./config.yml', # In model catalog
#             label_map  ={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"}, # In model`label_map`
#             extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8] # Optional
#         )


# # 检测
# layout = model.detect(image)

# # 显示结果
# show_img = lp.draw_box(image, layout, box_width=3, show_element_type=True)

# type(layout)

