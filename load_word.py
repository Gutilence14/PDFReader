# from spire.doc import *
# from spire.doc.common import *
from base_output import *
from docx import Document
import json
import queue
from datetime import datetime
import re
import os


def analysis_word(word_path, out_dir, use_dict=True):
    # analysisa pdf file

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not use_dict:
        res = BaseWordOutput(
            Word=[]
        )
    else:
        res = {
            word_path: {
                "Text": None,
                "Table": None,
                "Figure": None,
            },
        }
    doc = Document(word_path)
    text_res = ""
    for para in doc.paragraphs:
        text_res += para.text
    text_res = re.sub(r'\s+', '', text_res)
    res[word_path]["Text"] = text_res

    table_res = ""
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                table_res += cell.text
    table_res = re.sub(r'\s+', '', table_res)
    res[word_path]["Table"] = table_res

    images = []
    dict_rel = doc.part._rels
    for rel in dict_rel:
        rel = dict_rel[rel]
        if "image" in rel.target_ref:
            print(rel.target_ref)
            filename_with_extension = os.path.basename(word_path)
            filename, extension = os.path.splitext(filename_with_extension)
            current_time = datetime.now().strftime("%Y%m%d%H%M%S%f") + '_' + filename + ".png"
            figure_image_name = os.path.join(out_dir, current_time)
            images.append(figure_image_name)
            with open(figure_image_name, "wb") as f:
                f.write(rel.target_part.blob)
    res[word_path]["Figure"] = images

    # #document elements, each of them has child elements
    # nodes = queue.Queue()
    # nodes.put(document)

    # #embedded images list.

    # images = []
    # image_res = []

    # #traverse
    # while nodes.qsize() > 0:
    #     node = nodes.get()
    #     for i in range(node.ChildObjects.Count):
    #         child = node.ChildObjects.get_Item(i)
    #         if child.DocumentObjectType == DocumentObjectType.Picture:
    #             picture = child if isinstance(child, DocPicture) else None
    #             dataBytes = picture.ImageBytes
    #             images.append(dataBytes)
    #         elif isinstance(child, ICompositeObject):
    #             nodes.put(child if isinstance(child, ICompositeObject) else None)
    # for i, item in enumerate(images):
    #     filename_with_extension = os.path.basename(word_path)
    #     filename, extension = os.path.splitext(filename_with_extension)
    #     current_time = datetime.now().strftime(
    #             "%Y-%m-%d_%H-%M-%S") + '_' + filename + ".png"
    #     table_image_name = os.path.join(out_dir, current_time)
    #     image_res.append(table_image_name)
    #     with open(table_image_name,'wb') as imageFile:
    #         imageFile.write(item)
    # res[word_path]["Figure"] = image_res
    # document.Close()

    return res


if __name__ == '__main__':
    word_path = "BIM/no_heading.docx"
    out_dir = 'img_folder'

    out = analysis_word(word_path, out_dir)
    print(out)
    # with open(word_path, 'w', encoding='utf-8') as json_file:
    #     json.dump(out, json_file, ensure_ascii=False)
