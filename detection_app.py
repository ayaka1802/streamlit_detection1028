from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os
from PIL import Image
import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont



KEY = os.environ["VISION_KEY_1027"]
ENDPOINT = os.environ["VISION_ENDPOINT_1027"]

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_tags(filepath):
    local_image = open(filepath, "rb")

    tags_result = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
        
    return tags_name

def detect_objects(filepath):
    local_image = open(filepath, "rb")

    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results.objects
    return objects


st.title('物体検出アプリ')

uploaded_file = st.file_uploader('Choose an image...', type=['jpg','png'])
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)
    objects = detect_objects(img_path)

    # 描画
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property

        #フォント情報作成
        font = ImageFont.truetype(font='./Helvetica 400.ttf', size=50)
        #text_w, text_h = draw.textsize(caption, font=font)

        draw.rectangle([(x, y), (x+w, y+h)], fill=None, outline='red', width=5)

        tl = (x,y)
        #文字の四点の座標取得
        a,b,c,d= draw.textbbox(tl,caption,font=font)
        #文字の背景描画
        draw.rectangle([(x, y), (c,d)], fill='red')
        #文字描画
        draw.text((x, y), caption, fill='white', font=font)


    st.image(img)

    tags_name = get_tags(img_path)
    tags_name = ', '.join(tags_name)
    st.markdown('**認識されたコンテンツタグ**')
    st.markdown(f'> {tags_name}')    