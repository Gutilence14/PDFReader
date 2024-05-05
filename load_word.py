from spire.doc import *
from spire.doc.common import *
from base_output import *
import json
import queue
from datetime import datetime
import re



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

    document = Document()
    document.LoadFromFile(word_path)
    text = document.GetText()
    text = re.sub(r'\s+', '', text)
    res[word_path]["Text"] = text


    #document elements, each of them has child elements
    nodes = queue.Queue()
    nodes.put(document)

    #embedded images list.

    images = []
    image_res = []

    #traverse
    while nodes.qsize() > 0:
        node = nodes.get()
        for i in range(node.ChildObjects.Count):
            child = node.ChildObjects.get_Item(i)
            if child.DocumentObjectType == DocumentObjectType.Picture:
                picture = child if isinstance(child, DocPicture) else None
                dataBytes = picture.ImageBytes
                images.append(dataBytes)
            elif isinstance(child, ICompositeObject):
                nodes.put(child if isinstance(child, ICompositeObject) else None)
    for i, item in enumerate(images):
        filename_with_extension = os.path.basename(word_path)
        filename, extension = os.path.splitext(filename_with_extension)
        current_time = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S") + '_' + filename + ".png"
        table_image_name = os.path.join(out_dir, current_time)
        image_res.append(table_image_name)
        with open(table_image_name,'wb') as imageFile:
            imageFile.write(item)
    res[word_path]["Figure"] = image_res
    document.Close()

    return res





if __name__ == '__main__':
    word_path = "BIM/2.docx"
    out_dir = 'img_folder'

    out = analysis_word(word_path, out_dir)
    print(out)
    # with open(word_path, 'w', encoding='utf-8') as json_file:
    #     json.dump(out, json_file, ensure_ascii=False)
