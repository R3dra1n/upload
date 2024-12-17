import json
import os
import streamlit as st

def save_to_json(case_data, output_dir="output_json"):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{case_data['case_id']}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(case_data, f, indent=4, ensure_ascii=False)
    return file_path

# Streamlit 前端界面
st.title("JSON 文件生成工具")
st.write("请填写以下字段，点击按钮生成 JSON 文件。")

# 用户输入字段
case_id = st.text_input("案例编号 (case_id)", "case_001")
original_image = st.text_input("原始图片名称 (original_image)", "case_001_original.jpg")
disputed_image = st.text_input("纠纷图片名称 (disputed_image)", "case_001_disputed.jpg")
label = st.selectbox("是否侵权 (label)", ["侵权", "不侵权"])
modification_type = st.text_input("修改类型 (modification_type)", "")
visual_similarity_score = st.slider("视觉相似度评分 (visual_similarity_score)", 0.0, 1.0, 0.5)
court = st.text_input("审理法院 (court)", "")
judgment_date = st.date_input("判决日期 (judgment_date)")
description = st.text_area("描述信息 (description)", "")
source = st.text_input("数据来源 (source)", "")

# 按钮生成 JSON 文件
if st.button("生成 JSON 文件"):
    case_data = {
        "case_id": case_id,
        "original_image": original_image,
        "disputed_image": disputed_image,
        "label": label,
        "modification_type": modification_type,
        "visual_similarity_score": visual_similarity_score,
        "court": court,
        "judgment_date": str(judgment_date),
        "description": description,
        "source": source
    }
    file_path = save_to_json(case_data)
    st.success(f"JSON 文件已生成：{file_path}")
    st.json(case_data)  # 在界面显示 JSON 数据