# --coding:utf-8--

from keras.preprocessing import image
import glob
import numpy as np
from PIL import Image
import os
from keras.models import load_model


def read_image(img_path):
    try:
        img = image.load_img(img_path, target_size=(299, 299))
    except Exception as e:
        print(img_path, e)

    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img/255


def draw_save(img_path, label, img_test, out='tmp/'):
    img = Image.open(img_path)
    os.makedirs(os.path.join(out, label), exist_ok=True)
    if img is None: return None

    img.save(os.path.join(out, label, img_test))


labels = {'古蹟': 0, '台北101': 1, '海岸': 2, '淡水漁人碼頭': 3, '瀑布': 4, '燈塔': 5, '登山': 6, '紅毛城': 7, '遊樂園': 8}

labels = {str(v): k for k, v in labels.items()}
print(labels)
# 隨意選一個照片
files = glob.glob("righ\\try\\*.jpg")
# print(files)
# print(len(files))
model = load_model('mode_iv3LeafFinetune_15.h5')   # 辨識景點

for i in range(0, len(files)):
    # print(i)
    print(files[i].split("\\")[2])

    img = read_image(files[i])

    pred = model.predict(img)[0]
    print(pred)

    # 推論出機率最高的分類, 取得所在位置
    index = np.argmax(pred)

    print('照片 :', files[i].split("\\")[2], ',類別 :', labels[str(index)], ',信心度 :', pred[index])
    a = files[i].split("\\")[2]
    draw_save(files[i], labels[str(index)], img_test=a, out='tmp/')

