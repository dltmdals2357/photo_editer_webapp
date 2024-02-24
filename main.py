import cv2
import streamlit as st
from PIL import Image, ImageEnhance
import os

if 'info' not in st.session_state:
    st.session_state.info = {"brightness":1, "sharpness":1, "contrast":1,"color":1}

centered_text_style = """
    <style>
        div {
            text-align: center;
            justify-content: center;
        }
        .highlight {
            font-size: 50px;
            font-weight: light;
        }
    </style>
"""    

st.markdown(centered_text_style, unsafe_allow_html=True)

st.title('사진 에디터')
st.divider()

photo = st.file_uploader("수정할 사진 선택", type=['jpg', 'png'], accept_multiple_files=False)

if photo is not None:
    filename = photo.name
    filepath = f"image/{filename}"
    f = open(filepath, 'wb')
    data = photo.getvalue()
    f.write(data)
    f.close()

    # print(">>>>> filepath #1:", filepath)
  
    # print("st.session_state.photo:", st.session_state.photo)
    img = Image.open(filepath)

    st.divider()

    brightness = st.slider("밝기", 0.0, 2.0, 1.0)
    st.session_state.info["brightness"] = brightness
    contrast = st.slider("대비", 0.0, 5.0, 1.0)
    st.session_state.info["contrast"] = contrast
    sharpness = st.slider("정교함", 0.0, 2.0, 1.0)
    st.session_state.info["sharpness"] = sharpness
    saturation = st.slider("채도", 0.0, 1.0, 1.0)
    st.session_state.info["color"] = saturation

    # st.write(st.session_state.info)
    
    enhancer_b = ImageEnhance.Brightness(img)
    img_brightend = enhancer_b.enhance(st.session_state.info["brightness"])

    enhancer_c = ImageEnhance.Contrast(img_brightend)
    img_contrast = enhancer_c.enhance(st.session_state.info["contrast"])

    enhancer_sh = ImageEnhance.Sharpness(img_contrast)
    img_sharpness = enhancer_sh.enhance(st.session_state.info["sharpness"])

    enhancer_s = ImageEnhance.Color(img_sharpness)
    img_color = enhancer_s.enhance(st.session_state.info["color"])

    empty = st.empty()
    empty.image(img_color, width=400)
    
    img_color.save(filepath)

    st.divider()


    with open(filepath, "rb") as file:
        photo_name = st.text_input('저장할 사진이름을 입력해주세요')
        save_img = f"{photo_name}.{photo.name.split('.')[1]}"
        st.download_button('저장', data=file, file_name=save_img)
