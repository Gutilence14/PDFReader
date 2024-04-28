import os
import docx
import re
import subprocess
from tqdm import tqdm



# def get_text(word_path):
#     text_res = ""
#     for filename in os.listdir(word_path):
#         filename = os.path.join(word_path, filename)
#         print(filename)
#         if filename.endswith('.doc'):
#             subprocess.call(['soffice', '--headless', '--convert-to', 'docx', '--outdir', word_path,  filename])
#             doc = docx.Document(filename[:-4] + ".docx")
#         else:
#             doc = docx.Document(filename)

#         for para in doc.paragraphs:
#             text_res += para.text
#     text_res = re.sub(r'\s+', '', text_res)
#     return text_res



# def get_figures(word_path, result_path):
#     """
#     图片提取
#     :param word_path: word路径
#     :param result_path: 结果路径
#     :return: 
#     """
#     figure_image_name_res = []
#     doc = docx.Document(word_path)
#     dict_rel = doc.part._rels
#     for rel in dict_rel:
#         rel = dict_rel[rel]
#         if "image" in rel.target_ref:
#             if not os.path.exists(result_path):
#                 os.makedirs(result_path)
#             img_name = re.findall("/(.*)", rel.target_ref)[0]
#             word_name = os.path.splitext(word_path)[0]
#             if os.sep in word_name:
#                 new_name = word_name.split('\\')[-1]
#             else:
#                 new_name = word_name.split('/')[-1]
#             img_name = f'{new_name}_{img_name}'
#             with open(f'{result_path}/{img_name}', "wb") as f:
#                 f.write(rel.target_part.blob)
#             figure_image_name_res.append('{result_path}/{img_name}')



def analysis_word(word_path, out_dir, use_dict=True):

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if word_path.endswith('.doc'):
        folder_path = os.path.dirname(word_path)
        word_path = os.path.basename(word_path)
        # word_path = word_path[:-4] + ".docx"]
        subprocess.call(['soffice', '--headless', '--convert-to', 'docx',  '--outdir', folder_path, word_path])
        word_path = word_path[:-4] + ".docx"
        doc = docx.Document(word_path)
    else:
        doc = docx.Document(word_path)
    res = {
        word_path: {},
    }



analysis_word("BIM/4.doc", "img_folder")


    # for index, filename in enumerate(os.listdir(word_path)):
    #     filename = os.path.join(word_path, filename)
    #     print(filename)
    #     if filename.endswith('.doc'):
    #         subprocess.call(['soffice', '--headless', '--convert-to', 'docx', '--outdir', word_path,  filename])
    #         doc = docx.Document(filename[:-4] + ".docx")
    #     else:
    #         doc = docx.Document(filename)
    #     res = {
    #             filename: {},
    #         }

    #     for index, i in enumerate(tqdm(img)):
    #         if use_dict:
    #             res[pdf_path][index] = {
    #                 "Title": None,
    #                 "Text": None,
    #                 "Table": None,
    #                 "Figure": None,
    #             }
    #         layout = detect_img(i, detect_config)
    #         # text_blocks 排序->ocr
    #         h, w = i.size


    # get_figures('BIM/1.docx', 'extracted_images')