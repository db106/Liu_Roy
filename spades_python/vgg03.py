# --- page.91
# coding: utf - 8
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
# 載入 VGG16
model = VGG16(weights='imagenet')
# 顯示出模型摘要
model.summary()


# 辨識
def predict(filename, rank):
    img = image.load_img(filename, target_size=(224, 224))
    x = image.img_to_array(img)
    print(x.shape)   # (224, 224, 3)
# 在x array 的第 0 維新增一個資料(np.expand_dims 用於擴充維度 )
    x = np.expand_dims(x, axis=0)
    print(x.shape)   # (1, 224, 224, 3)
# 預測圖片 # 轉換成 VGG16 可以讀的格式
    preds = model.predict(preprocess_input(x))
    print(preds.shape)   # (1, 1000)
# rank 取前幾名排序
    results = decode_predictions(preds, top=rank)[0]
    return results


# 辨識
filename = "薯條.jpg"
plt.figure()
im = Image.open(filename)
im_list = np.asarray(im)
plt.title("predict")
plt.axis("off")
plt.imshow(im_list)
plt.show()
results = predict(filename, 3)
for result in results:
    print(result)
