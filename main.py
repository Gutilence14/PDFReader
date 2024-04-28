import os
from PIL import Image
from pdf2image import convert_from_path
import layoutparser as lp
from dataclasses import dataclass
from transformers.utils import ModelOutput
from typing import Optional, Tuple
from datetime import datetime
from tqdm import tqdm
import json
import re
from base_output import BasePdfOutput, PdfOutput



def load_img(pdf_path):
    # pdf to image
    pdf_img = convert_from_path(pdf_path, thread_count=2, fmt='png', dpi=100)
    return pdf_img


def detect_img(img, detect_config):
    # detect "Page","Title","Text","Table","Figure" in pdf image

    model = lp.Detectron2LayoutModel(detect_config,
                                     extra_config=[
                                         "MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                     label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"})
    layout = model.detect(img)
    return layout


def analysis_pdf(pdf_path, img, detect_config, ocr_agent, out_dir, use_dict=True):
    # analysisa pdf file

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not use_dict:
        res = PdfOutput(
            Pdf=[]
        )
    else:
        res = {
            pdf_path: {},
        }

    for index, i in enumerate(tqdm(img)):
        if use_dict:
            res[pdf_path][index] = {
                "Title": None,
                "Text": None,
                "Table": None,
                "Figure": None,
            }
        layout = detect_img(i, detect_config)
        # text_blocks 排序->ocr
        h, w = i.size


        text_blocks = lp.Layout([b for b in layout if b.type == 'Text'])
        left_interval = lp.Interval(0, w/2*1.05, axis='x').put_on_canvas(i)
        left_blocks = text_blocks.filter_by(left_interval, center=True)
        left_blocks.sort(key=lambda b: b.coordinates[1], inplace=True)
        right_blocks = lp.Layout([b for b in text_blocks if b not in left_blocks])
        right_blocks.sort(key=lambda b: b.coordinates[1], inplace=True)
        text_blocks = lp.Layout([b.set(id=idx)
                                for idx, b in enumerate(left_blocks + right_blocks)])
        text_res = ""
        for block in text_blocks:
            x_1, y_1, x_2, y_2 = block.pad(left=5, right=5, top=5, bottom=5).block.x_1, block.pad(left=5, right=5, top=5, bottom=5).block.y_1, block.pad(
                left=5, right=5, top=5, bottom=5).block.x_2, block.pad(left=5, right=5, top=5, bottom=5).block.y_2
            segment_image = i.crop((x_1, y_1, x_2, y_2))
            text = ocr_agent.detect(segment_image)
            text_res += text
        text_res = re.sub(r'\s+', '', text_res)


        figure_blocks = lp.Layout([b for b in layout if b.type == 'Figure'])
        figure_image_name_res = []
        for block in figure_blocks:
            x_1, y_1, x_2, y_2 = block.pad(left=5, right=5, top=5, bottom=5).block.x_1, block.pad(left=5, right=5, top=5, bottom=5).block.y_1, block.pad(
                left=5, right=5, top=5, bottom=5).block.x_2, block.pad(left=5, right=5, top=5, bottom=5).block.y_2
            segment_image = i.crop((x_1, y_1, x_2, y_2))
            filename_with_extension = os.path.basename(pdf_path)
            filename, extension = os.path.splitext(filename_with_extension)
            current_time = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S") + '_' + filename + ".png"
            figure_image_name = os.path.join(out_dir, current_time)
            segment_image.save(figure_image_name)
            figure_image_name_res.append(figure_image_name)


        table_blocks = lp.Layout([b for b in layout if b.type == 'Table'])
        table_image_name_res = []
        for block in table_blocks:
            x_1, y_1, x_2, y_2 = block.pad(left=5, right=5, top=5, bottom=5).block.x_1, block.pad(left=5, right=5, top=5, bottom=5).block.y_1, block.pad(
                left=5, right=5, top=5, bottom=5).block.x_2, block.pad(left=5, right=5, top=5, bottom=5).block.y_2
            segment_image = i.crop((x_1, y_1, x_2, y_2))
            filename_with_extension = os.path.basename(pdf_path)
            filename, extension = os.path.splitext(filename_with_extension)
            current_time = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S") + '_' + filename + ".png"
            table_image_name = os.path.join(out_dir, current_time)
            segment_image.save(table_image_name)
            table_image_name_res.append(table_image_name)


        # title_blocks ocr
        title_blocks = lp.Layout([b for b in layout if b.type == 'Title'])
        title_res = ""
        for block in title_blocks:
            x_1, y_1, x_2, y_2 = block.pad(left=5, right=5, top=5, bottom=5).block.x_1, block.pad(left=5, right=5, top=5, bottom=5).block.y_1, block.pad(
                left=5, right=5, top=5, bottom=5).block.x_2, block.pad(left=5, right=5, top=5, bottom=5).block.y_2
            segment_image = i.crop((x_1, y_1, x_2, y_2))
            title = ocr_agent.detect(segment_image)
            title_res += title
        if not use_dict:
            output = BasePdfOutput(
                Page=index,
                Text=text_res,
                Title=title_res,
                Table=table_image_name_res,
                Figure=figure_image_name_res,
            )
            res.Pdf.append(output)
        else:
            res[pdf_path][index]["Title"] = title_res
            res[pdf_path][index]["Text"] = text_res
            res[pdf_path][index]["Table"] = table_image_name_res
            res[pdf_path][index]["Figure"] = figure_image_name_res


    return res

if __name__ == '__main__':
    pdf_path = "BIM/4.pdf"
    detect_config = './config.yml'
    img = load_img(pdf_path=pdf_path)
    ocr_agent = lp.TesseractAgent(languages='chi_sim+eng+spa')
    out_dir = 'img_folder'

    pdf_path, file_extension = os.path.splitext(pdf_path)
    pdf_path = pdf_path + '.json'

    out = analysis_pdf(pdf_path, img, detect_config, ocr_agent, out_dir)
    with open(pdf_path, 'w', encoding='utf-8') as json_file:
        json.dump(out, json_file, ensure_ascii=False)
