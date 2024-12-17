import json
import os
import zipfile
import streamlit as st

def generate_json(case_data, json_path):
    """生成 JSON 数据并保存到文件"""
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(case_data, f, indent=4, ensure_ascii=False)

def create_zip_file(file_list, zip_path):
    """将多个文件打包成 ZIP 文件"""
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in file_list:
            if file:  # 确保文件路径存在
                zipf.write(file, os.path.basename(file))
    return zip_path

# 创建保存图片的目录
UPLOAD_DIR = "uploaded_images"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Streamlit 前端界面
st.title("文件打包下载工具")
st.write("请填写以下字段，上传图片并点击按钮生成 ZIP 文件。")

# 用户输入字段
case_id = st.text_input("案例编号 (case_id)", "001")
type = st.selectbox("什么类型作品 (type)", ["文字作品", "美术作品", "摄影作品"])
label = st.selectbox("是否侵权 (label)", ["侵权", "不侵权", "其它"])
modification_type = st.text_input("侵权类型/方式 (modification_type)", "实质性相似")
visual_similarity_score = st.slider("视觉相似度评分", 0.0, 1.0, 0.5)
court = st.text_input("审理法院 (court)", "")
judgment_date = st.text_input("判决日期 (judgment_date)", "2013")
description = st.text_area("描述信息 (description)", "")
source = st.text_input("数据来源 (source)", "")

# 图片上传
uploaded_original_image = st.file_uploader("上传原始图片", type=["jpg", "png", "jpeg"])
uploaded_disputed_image = st.file_uploader("上传纠纷图片", type=["jpg", "png", "jpeg"])

# 按钮生成 ZIP 文件
if st.button("生成 ZIP 文件"):
    # 确保有上传文件
    if uploaded_original_image and uploaded_disputed_image:
        # 保存图片到指定路径
        original_image_path = os.path.join(UPLOAD_DIR, f"case_{case_id}_original.jpg")
        disputed_image_path = os.path.join(UPLOAD_DIR, f"case_{case_id}_disputed.jpg")

        with open(original_image_path, "wb") as f:
            f.write(uploaded_original_image.read())
        with open(disputed_image_path, "wb") as f:
            f.write(uploaded_disputed_image.read())

        # 生成 JSON 文件
        json_file_path = os.path.join(OUTPUT_DIR, f"case_{case_id}.json")
        case_data = {
            "case_id": f"case_{case_id}",
            "original_image": os.path.basename(original_image_path),
            "disputed_image": os.path.basename(disputed_image_path),
            "type": type,
            "label": label,
            "modification_type": modification_type,
            "visual_similarity_score": visual_similarity_score,
            "court": court,
            "judgment_date": str(judgment_date),
            "description": description,
            "source": source
        }
        generate_json(case_data, json_file_path)

        # 打包成 ZIP 文件
        zip_file_path = os.path.join(OUTPUT_DIR, f"case_{case_id}.zip")
        create_zip_file([original_image_path, disputed_image_path, json_file_path], zip_file_path)

        # 提供下载按钮
        st.success("ZIP 文件已生成！点击下面按钮下载。")
        with open(zip_file_path, "rb") as zipf:
            st.download_button(
                label="下载 ZIP 文件",
                data=zipf,
                file_name=f"case_{case_id}.zip",
                mime="application/zip"
            )
    else:
        st.error("请上传两张图片！")
